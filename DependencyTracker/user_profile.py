import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
import uuid
import streamlit as st
from database import get_database

class UserProfileManager:
    def __init__(self):
        """
        Initialize user profile management system
        """
        # Get database instance
        self.db = get_database()
        
        # Make sure the demo user exists
        self._ensure_demo_user()
    
    def _ensure_demo_user(self):
        """
        Ensures a demo user exists in the database
        """
        if not self.db.get_user_by_username('demo_user'):
            # Create demo user
            self.db.create_user(
                username='demo_user',
                email='demo@example.com',
                password_hash=self._hash_password('password123')
            )
    
    def _hash_password(self, password: str) -> str:
        """
        Hash a password for secure storage
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        # In a real application, you would use a proper password hashing algorithm
        # with salt, such as bcrypt or Argon2
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user with username and password
        
        Args:
            username (str): User's username
            password (str): User's password
            
        Returns:
            User profile or None if authentication fails
        """
        # Get user from database
        user = self.db.get_user_by_username(username)
        
        if user and user['password_hash'] == self._hash_password(password):
            # Update last login
            self.db.update_last_login(user['id'])
            
            # Return a copy without the password hash
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'join_date': user['join_date']
            }
        
        return None
    
    def create_profile(self, username: str, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Create a new user profile
        
        Args:
            username (str): User's chosen username
            email (str): User's email address
            password (str): User's password
            
        Returns:
            Created user profile or None if creation fails
        """
        # Hash password
        password_hash = self._hash_password(password)
        
        # Create user in database
        user = self.db.create_user(username, email, password_hash)
        
        if user:
            # Return a copy without the password hash
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'join_date': user['join_date']
            }
        
        return None
    
    def update_profile(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update user profile information
        
        Args:
            user_id (int): Unique user identifier
            updates (Dict): Profile updates
            
        Returns:
            Boolean indicating successful update
        """
        db_updates = {}
        
        # Handle email update
        if 'email' in updates:
            db_updates['email'] = updates['email']
        
        # Handle password update
        if 'password' in updates:
            db_updates['password_hash'] = self._hash_password(updates['password'])
        
        # Update user in database
        return self.db.update_user(user_id, db_updates)
    
    def get_saved_papers(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get a user's saved papers
        
        Args:
            user_id (int): Unique user identifier
            
        Returns:
            List of saved papers
        """
        return self.db.get_user_saved_papers(user_id)
    
    def save_paper(self, user_id: int, paper: Dict[str, Any]) -> bool:
        """
        Save a paper to a user's collection
        
        Args:
            user_id (int): Unique user identifier
            paper (Dict): Paper to save
            
        Returns:
            Boolean indicating successful save
        """
        return self.db.save_paper_for_user(user_id, paper)
    
    def remove_saved_paper(self, user_id: int, paper_id: int) -> bool:
        """
        Remove a paper from a user's collection
        
        Args:
            user_id (int): Unique user identifier
            paper_id (int): ID of paper to remove
            
        Returns:
            Boolean indicating successful removal
        """
        return self.db.remove_saved_paper(user_id, paper_id)
    
    def get_user_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's research history
        
        Args:
            user_id (int): Unique user identifier
            limit (int): Maximum number of history items to return
            
        Returns:
            List of history items
        """
        return self.db.get_user_history(user_id, limit)
