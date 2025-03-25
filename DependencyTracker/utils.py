import streamlit as st
from datetime import datetime
from typing import List, Dict, Any
from database import get_database

def add_to_history(activity_type: str, title: str, description: str):
    """
    Add an activity to the user's research history
    
    Args:
        activity_type (str): Type of activity (search, analysis, chat)
        title (str): Title of the activity
        description (str): Description of the activity
    """
    # Always maintain in-memory history for current session
    if 'research_history' not in st.session_state:
        st.session_state.research_history = []
    
    activity = {
        'type': activity_type,
        'title': title,
        'description': description,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    
    st.session_state.research_history.append(activity)
    
    # Limit history size in session
    if len(st.session_state.research_history) > 100:
        st.session_state.research_history = st.session_state.research_history[-100:]
    
    # If user is logged in, also save to database
    if st.session_state.get('current_user'):
        db = get_database()
        db.add_history_item(
            user_id=st.session_state.current_user['id'],
            activity_type=activity_type,
            title=title,
            description=description
        )

def format_authors(authors: List[str], max_display: int = 3) -> str:
    """
    Format author list for display, limiting the number shown
    
    Args:
        authors (List[str]): List of author names
        max_display (int): Maximum number of authors to display
        
    Returns:
        Formatted author string
    """
    if not authors:
        return ""
    
    if len(authors) <= max_display:
        return ", ".join(authors)
    else:
        return ", ".join(authors[:max_display]) + f" et al. (+{len(authors) - max_display})"

def format_date(date_str: str) -> str:
    """
    Format date string for consistent display
    
    Args:
        date_str (str): Date string in various formats
        
    Returns:
        Formatted date string
    """
    try:
        # Try to parse various date formats
        formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%m/%d/%Y']
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%B %d, %Y')
            except ValueError:
                continue
        
        # If no format works, return the original
        return date_str
    except:
        return date_str
