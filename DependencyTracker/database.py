import sqlite3
import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import streamlit as st

DATABASE_PATH = "research_assistant.db"

class Database:
    def __init__(self):
        """Initialize the database connection and create tables if they don't exist"""
        self.conn = self._get_connection()
        self._create_tables()
    
    def _get_connection(self):
        """Get a database connection, creating the database file if it doesn't exist"""
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        # Make sqlite return dictionaries instead of tuples
        conn.row_factory = sqlite3.Row
        return conn
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            join_date TEXT NOT NULL,
            last_login TEXT,
            preferences TEXT
        )
        ''')
        
        # Create papers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paper_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            authors TEXT NOT NULL,
            year TEXT,
            source TEXT,
            abstract TEXT,
            citation_count INTEGER DEFAULT 0,
            url TEXT,
            metadata TEXT,
            date_added TEXT NOT NULL
        )
        ''')
        
        # Create user_papers (saved papers) table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            paper_id INTEGER NOT NULL,
            date_saved TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (paper_id) REFERENCES papers (id) ON DELETE CASCADE,
            UNIQUE(user_id, paper_id)
        )
        ''')
        
        # Create research_history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS research_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            activity_type TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
        ''')
        
        # Create paper_analysis table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS paper_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paper_id INTEGER NOT NULL,
            summary TEXT,
            key_findings TEXT,
            methodology TEXT,
            implications TEXT,
            date_analyzed TEXT NOT NULL,
            FOREIGN KEY (paper_id) REFERENCES papers (id) ON DELETE CASCADE
        )
        ''')
        
        self.conn.commit()
    
    # User Management Methods
    
    def create_user(self, username: str, email: str, password_hash: str) -> Optional[Dict[str, Any]]:
        """Create a new user and return the user data if successful"""
        cursor = self.conn.cursor()
        try:
            join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, join_date) VALUES (?, ?, ?, ?)",
                (username, email, password_hash, join_date)
            )
            self.conn.commit()
            return self.get_user_by_username(username)
        except sqlite3.IntegrityError:
            # Username or email already exists
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            # Convert Row to dict
            return dict(user)
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return dict(user)
        return None
    
    def update_user(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """Update user data"""
        if not updates:
            return False
        
        cursor = self.conn.cursor()
        set_values = []
        params = []
        
        for key, value in updates.items():
            if key in ['username', 'email', 'password_hash', 'preferences']:
                set_values.append(f"{key} = ?")
                params.append(value)
        
        if not set_values:
            return False
        
        sql = f"UPDATE users SET {', '.join(set_values)} WHERE id = ?"
        params.append(user_id)
        
        try:
            cursor.execute(sql, params)
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            # Username or email already exists
            return False
    
    def update_last_login(self, user_id: int) -> bool:
        """Update user's last login time"""
        cursor = self.conn.cursor()
        last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (last_login, user_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # Paper Management Methods
    
    def add_paper(self, paper_data: Dict[str, Any]) -> Optional[int]:
        """Add a paper to the database and return its ID"""
        # Generate a unique paper_id if not provided
        if 'paper_id' not in paper_data:
            paper_data['paper_id'] = f"{paper_data['source']}_{paper_data['title'][:50]}"
        
        # Convert authors list to JSON string
        if 'authors' in paper_data and isinstance(paper_data['authors'], list):
            paper_data['authors'] = json.dumps(paper_data['authors'])
        
        # Extract metadata
        metadata = {}
        for key in list(paper_data.keys()):
            if key not in ['paper_id', 'title', 'authors', 'year', 'source', 'abstract', 'citation_count', 'url']:
                metadata[key] = paper_data.pop(key)
        
        paper_data['metadata'] = json.dumps(metadata)
        paper_data['date_added'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO papers 
            (paper_id, title, authors, year, source, abstract, citation_count, url, metadata, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                paper_data['paper_id'],
                paper_data['title'],
                paper_data['authors'],
                paper_data.get('year', ''),
                paper_data.get('source', ''),
                paper_data.get('abstract', ''),
                paper_data.get('citation_count', 0),
                paper_data.get('url', ''),
                paper_data['metadata'],
                paper_data['date_added']
            ))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Paper already exists, find and return its ID
            cursor.execute("SELECT id FROM papers WHERE paper_id = ?", (paper_data['paper_id'],))
            result = cursor.fetchone()
            if result:
                return result['id']
            return None
    
    def get_paper_by_id(self, paper_id: int) -> Optional[Dict[str, Any]]:
        """Get paper by its database ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
        paper = cursor.fetchone()
        if paper:
            paper_dict = dict(paper)
            # Convert authors JSON to list
            paper_dict['authors'] = json.loads(paper_dict['authors'])
            # Convert metadata JSON to dict
            paper_dict['metadata'] = json.loads(paper_dict['metadata'])
            return paper_dict
        return None
    
    def save_paper_for_user(self, user_id: int, paper_data: Dict[str, Any]) -> bool:
        """Save a paper to a user's collection"""
        # First add or get the paper
        paper_id = self.add_paper(paper_data)
        if not paper_id:
            return False
        
        # Then associate it with the user
        cursor = self.conn.cursor()
        try:
            date_saved = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO user_papers (user_id, paper_id, date_saved) VALUES (?, ?, ?)",
                (user_id, paper_id, date_saved)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Already saved
            return True
    
    def get_user_saved_papers(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all papers saved by a user"""
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT p.*, up.date_saved, up.notes
        FROM papers p
        JOIN user_papers up ON p.id = up.paper_id
        WHERE up.user_id = ?
        ORDER BY up.date_saved DESC
        ''', (user_id,))
        
        papers = []
        for row in cursor.fetchall():
            paper_dict = dict(row)
            # Convert authors JSON to list
            paper_dict['authors'] = json.loads(paper_dict['authors'])
            # Convert metadata JSON to dict
            paper_dict['metadata'] = json.loads(paper_dict['metadata'])
            papers.append(paper_dict)
        
        return papers
    
    def remove_saved_paper(self, user_id: int, paper_id: int) -> bool:
        """Remove a paper from a user's saved collection"""
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM user_papers WHERE user_id = ? AND paper_id = ?",
            (user_id, paper_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    # Research History Methods
    
    def add_history_item(self, user_id: int, activity_type: str, title: str, description: str) -> bool:
        """Add an item to the user's research history"""
        cursor = self.conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO research_history (user_id, activity_type, title, description, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, activity_type, title, description, date)
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_user_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get a user's research history"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM research_history WHERE user_id = ? ORDER BY date DESC LIMIT ?",
            (user_id, limit)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    # Paper Analysis Methods
    
    def save_paper_analysis(self, paper_id: int, analysis_data: Dict[str, Any]) -> bool:
        """Save analysis for a paper"""
        cursor = self.conn.cursor()
        date_analyzed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Convert complex objects to JSON
        summary = analysis_data.get('summary', '')
        key_findings = json.dumps(analysis_data.get('key_findings', []))
        methodology = json.dumps(analysis_data.get('methodology', {}))
        implications = json.dumps(analysis_data.get('implications', {}))
        
        try:
            cursor.execute('''
            INSERT INTO paper_analysis 
            (paper_id, summary, key_findings, methodology, implications, date_analyzed)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (paper_id, summary, key_findings, methodology, implications, date_analyzed))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Update existing analysis
            cursor.execute('''
            UPDATE paper_analysis 
            SET summary = ?, key_findings = ?, methodology = ?, implications = ?, date_analyzed = ?
            WHERE paper_id = ?
            ''', (summary, key_findings, methodology, implications, date_analyzed, paper_id))
            self.conn.commit()
            return cursor.rowcount > 0
    
    def get_paper_analysis(self, paper_id: int) -> Optional[Dict[str, Any]]:
        """Get analysis for a paper"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM paper_analysis WHERE paper_id = ?", (paper_id,))
        analysis = cursor.fetchone()
        if analysis:
            analysis_dict = dict(analysis)
            # Convert JSON strings back to objects
            analysis_dict['key_findings'] = json.loads(analysis_dict['key_findings'])
            analysis_dict['methodology'] = json.loads(analysis_dict['methodology'])
            analysis_dict['implications'] = json.loads(analysis_dict['implications'])
            return analysis_dict
        return None
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

# Create a database instance in Streamlit's session state
def get_database():
    """Get or create a database instance in Streamlit's session state"""
    if 'database' not in st.session_state:
        st.session_state.database = Database()
    return st.session_state.database