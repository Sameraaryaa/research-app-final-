import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from paper_manager import ResearchPaperManager
from chat_bot import ResearchChatBot
from user_profile import UserProfileManager
import utils

class ResearchAssistantApp:
    def __init__(self):
        """
        Initialize the Research Assistant Application
        - Set up session state
        - Configure main app components
        """
        # Initialize session state variables
        if 'current_user' not in st.session_state:
            st.session_state.current_user = None
        if 'research_history' not in st.session_state:
            st.session_state.research_history = []
        if 'search_results' not in st.session_state:
            st.session_state.search_results = []
        if 'selected_papers' not in st.session_state:
            st.session_state.selected_papers = []
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'paper_analysis' not in st.session_state:
            st.session_state.paper_analysis = {}
        if 'app_page' not in st.session_state:
            st.session_state.app_page = 'Home'
        if 'tutorial_step' not in st.session_state:
            st.session_state.tutorial_step = 0
        if 'trending_topics' not in st.session_state:
            st.session_state.trending_topics = [
                "Machine Learning", "Quantum Computing", 
                "Climate Science", "Genomics", 
                "Renewable Energy", "Artificial Intelligence"
            ]

        # App configuration
        st.set_page_config(
            page_title="Research Assistant",
            page_icon=":microscope:",
            layout="wide"
        )

        # Initialize component managers
        self.paper_manager = ResearchPaperManager()
        self.user_manager = UserProfileManager()
        self.chat_bot = ResearchChatBot([])

    def run(self):
        """
        Run the main Streamlit application interface
        """
        st.title("🔬 Advanced Research Assistant")
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            font-weight: 500;
            margin-bottom: 0.75rem;
        }
        .card {
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }
        .highlight {
            background-color: #f0f7ff;
        }
        .sidebar .css-1d391kg {
            padding-top: 2rem;
        }
        .bottom-menu {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #ffffff;
            box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.1);
            padding: 12px 0;
            z-index: 999;
            display: flex;
            justify-content: center;
            border-top: 1px solid #e5e7eb;
        }
        .bottom-menu-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 8px 24px;
            margin: 0 8px;
            text-decoration: none;
            color: #64748b;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .bottom-menu-item:hover {
            color: #2563eb;
            background-color: #f8fafc;
        }
        .bottom-menu-item.active-nav-item {
            color: #2563eb;
            font-weight: 600;
        }
        .nav-icon {
            font-size: 1.25rem;
            margin-bottom: 4px;
        }
        .interactive-tag {
            display: inline-block;
            padding: 5px 15px;
            margin: 5px;
            background-color: #f0f7ff;
            border-radius: 20px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .interactive-tag:hover {
            background-color: #e1efff;
        }
        .demo-paper {
            border: 1px solid #eee;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            cursor: pointer;
        }
        .demo-paper:hover {
            border-color: #4285f4;
            background-color: #f9f9f9;
        }
        .active-nav-item {
            background-color: #e1efff;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # Sidebar Navigation
        with st.sidebar:
            st.image("https://img.icons8.com/fluency/96/microscope.png", width=50)
            st.header("Research Assistant")
            menu_selection = st.radio(
                "Navigation", 
                [
                    "Home", 
                    "Search Research", 
                    "Paper Analysis",
                    "Chat Assistant", 
                    "Profile", 
                    "Settings"
                ]
            )

            # User authentication section in sidebar
            self._render_auth_section()

        # Render appropriate page based on menu selection
        if menu_selection == "Home":
            self._render_home_page()
        elif menu_selection == "Search Research":
            self._render_research_search()
        elif menu_selection == "Paper Analysis":
            self._render_paper_analysis()
        elif menu_selection == "Chat Assistant":
            self._render_chat_assistant()
        elif menu_selection == "Profile":
            self._render_user_profile()
        elif menu_selection == "Settings":
            self._render_app_settings()

        # Add bottom navigation menu
        bottom_menu_html = f"""
        <div class="bottom-menu">
            <a href="#" class="bottom-menu-item {'active-nav-item' if menu_selection == 'Home' else ''}" onclick="
                var radio = window.parent.document.querySelectorAll('input[type=radio][value=\\'Home\\']')[0];
                if (radio) {{
                    radio.click();
                }}
            ">
                <i class="nav-icon">🏠</i> Home
            </a>
            <a href="#" class="bottom-menu-item {'active-nav-item' if menu_selection == 'Search Research' else ''}" onclick="
                var radio = window.parent.document.querySelectorAll('input[type=radio][value=\\'Search Research\\']')[0];
                if (radio) {{
                    radio.click();
                }}
            ">
                <i class="nav-icon">🔍</i> Search
            </a>
            <a href="#" class="bottom-menu-item {'active-nav-item' if menu_selection == 'Paper Analysis' else ''}" onclick="
                var radio = window.parent.document.querySelectorAll('input[type=radio][value=\\'Paper Analysis\\']')[0];
                if (radio) {{
                    radio.click();
                }}
            ">
                <i class="nav-icon">📊</i> Analyze
            </a>
            <a href="#" class="bottom-menu-item {'active-nav-item' if menu_selection == 'Chat Assistant' else ''}" onclick="
                var radio = window.parent.document.querySelectorAll('input[type=radio][value=\\'Chat Assistant\\']')[0];
                if (radio) {{
                    radio.click();
                }}
            ">
                <i class="nav-icon">💬</i> Chat
            </a>
            <a href="#" class="bottom-menu-item {'active-nav-item' if menu_selection == 'Profile' else ''}" onclick="
                var radio = window.parent.document.querySelectorAll('input[type=radio][value=\\'Profile\\']')[0];
                if (radio) {{
                    radio.click();
                }}
            ">
                <i class="nav-icon">👤</i> Profile
            </a>
        </div>
        """
        st.markdown(bottom_menu_html, unsafe_allow_html=True)

    def _render_auth_section(self):
        """Render the authentication section in the sidebar"""
        st.sidebar.divider()
        st.sidebar.markdown("<h3 style='margin-bottom: 15px;'>Account</h3>", unsafe_allow_html=True)

        if st.session_state.current_user:
            user = st.session_state.current_user

            # User profile card
            st.sidebar.markdown(f"""
            <div style="padding: 15px; border-radius: 10px; background-color: #f0f7ff; margin-bottom: 15px;">
                <h4 style="margin-top: 0; font-size: 1.2em;">👤 {user['username']}</h4>
                <p style="font-size: 0.9em; margin: 5px 0;">{user.get('email', 'No email provided')}</p>
                <p style="font-size: 0.8em; color: #666; margin: 0;">Member since {user.get('join_date', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)

            # Quick links
            st.sidebar.markdown("<h4>Quick Links</h4>", unsafe_allow_html=True)
            col1, col2 = st.sidebar.columns(2)
            with col1:
                if st.button("📚 My Papers", use_container_width=True):
                    # Redirect to profile
                    st.rerun()
            with col2:
                if st.button("⚙️ Settings", use_container_width=True):
                    # Redirect to settings
                    st.rerun()

            # Logout button
            st.sidebar.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
            if st.sidebar.button("🚪 Logout", use_container_width=True):
                st.session_state.current_user = None
                st.session_state.selected_papers = []
                st.session_state.paper_analysis = {}
                st.session_state.chat_history = []
                st.session_state.research_history = []
                st.sidebar.success("Logged out successfully!")
                st.rerun()
        else:
            # Authentication tabs
            auth_option = st.sidebar.radio("", ["Login", "Register"], horizontal=True, label_visibility="collapsed")

            st.sidebar.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)

            if auth_option == "Login":
                with st.sidebar.form("login_form"):
                    st.markdown("<h4 style='margin-bottom: 15px;'>Welcome Back</h4>", unsafe_allow_html=True)
                    username = st.text_input("Username", placeholder="Enter your username", key="login_username")
                    password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

                    # Remember me checkbox
                    st.checkbox("Remember me", value=True)

                    st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
                    submit = st.form_submit_button("🔐 Login", use_container_width=True)

                    if submit:
                        if username and password:
                            user = self.user_manager.authenticate_user(username, password)
                            if user:
                                st.session_state.current_user = user
                                st.session_state.research_history = []
                                st.sidebar.success(f"Welcome back, {user['username']}!")
                                st.rerun()
                            else:
                                st.sidebar.error("Invalid username or password")
                        else:
                            st.sidebar.warning("Please enter both username and password")
            else:
                with st.sidebar.form("register_form"):
                    st.markdown("<h4 style='margin-bottom: 15px;'>Create Account</h4>", unsafe_allow_html=True)
                    username = st.text_input("Username", placeholder="Choose a username", key="reg_username")
                    email = st.text_input("Email", placeholder="Enter your email", key="reg_email")
                    password = st.text_input("Password", type="password", placeholder="Create a password", key="reg_password")
                    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="reg_confirm_password")

                    # Terms and conditions
                    st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
                    st.checkbox("I agree to the Terms of Service and Privacy Policy", value=True)

                    st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
                    submit = st.form_submit_button("✨ Create Account", use_container_width=True)

                    if submit:
                        if not all([username, email, password, confirm_password]):
                            st.sidebar.warning("Please fill out all fields")
                        elif password != confirm_password:
                            st.sidebar.error("Passwords do not match")
                        else:
                            user = self.user_manager.create_profile(username, email, password)
                            if user:
                                st.session_state.current_user = user
                                st.session_state.research_history = []
                                st.sidebar.success(f"Welcome, {user['username']}!")
                                st.rerun()
                            else:
                                st.sidebar.error("Username or email already exists")

    def _render_home_page(self):
        """Render the landing page of the research assistant"""
        st.markdown("<h1 class='main-header'>Welcome to Your Research Companion</h1>", unsafe_allow_html=True)

        # Quick search bar at the top
        col1, col2 = st.columns([4, 1])
        with col1:
            quick_search = st.text_input("📝 Quick search for research papers...", 
                                       placeholder="Enter topic or keywords (e.g., machine learning, climate change)",
                                       key="home_quick_search")
        with col2:
            search_button = st.button("🔍 Search", use_container_width=True, key="home_search_btn")

        if search_button and quick_search:
            st.session_state.quick_search_query = quick_search
            st.session_state.app_page = "Search Research"
            st.rerun()

        # Trending topics
        st.markdown("<h3 style='margin-top: 20px;'>Trending Topics</h3>", unsafe_allow_html=True)
        topic_cols = st.columns(3)
        for i, topic in enumerate(st.session_state.trending_topics):
            col_idx = i % 3
            with topic_cols[col_idx]:
                if st.button(f"#{topic}", key=f"topic_{i}", use_container_width=True):
                    st.session_state.quick_search_query = topic
                    st.session_state.app_page = "Search Research"
                    st.rerun()

        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

        # Feature description cards with animation
        st.markdown("<h2 class='sub-header'>Explore Features</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="card">
                <h3>📚 Research Paper Search</h3>
                <p>Search papers across multiple academic databases including Semantic Scholar, arXiv, and PubMed.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Try Search", key="try_search", use_container_width=True):
                st.session_state.app_page = "Search Research"
                st.rerun()

        with col2:
            st.markdown("""
            <div class="card">
                <h3>🧠 AI Paper Analysis</h3>
                <p>Get AI-powered summaries, key findings, and insights from complex research papers.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Try Analysis", key="try_analysis", use_container_width=True):
                st.session_state.app_page = "Paper Analysis"
                st.rerun()

        with col3:
            st.markdown("""
            <div class="card">
                <h3>💬 Research Chat Assistant</h3>
                <p>Ask questions about papers and get comprehensive, research-based answers.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Try Chat", key="try_chat", use_container_width=True):
                st.session_state.app_page = "Chat Assistant"
                st.rerun()

        # Demo papers section - makes the page more interactive
        st.markdown("<h2 class='sub-header' style='margin-top: 40px;'>Example Papers</h2>", unsafe_allow_html=True)

        demo_papers = [
            {
                "title": "Attention Is All You Need",
                "authors": ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar", "Jakob Uszkoreit"],
                "year": 2017,
                "source": "NeurIPS",
                "citations": 54361,
                "abstract": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
            },
            {
                "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
                "authors": ["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee", "Kristina Toutanova"],
                "year": 2018,
                "source": "arXiv",
                "citations": 45328,
                "abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers."
            }
        ]

        for i, paper in enumerate(demo_papers):
            with st.container():
                st.markdown(f"""
                <div class="demo-paper">
                    <h3>{paper['title']}</h3>
                    <p><em>{', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}</em> • {paper['year']} • {paper['source']} • Cited by: {paper['citations']}</p>
                    <p>{paper['abstract']}</p>
                </div>
                """, unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("📊 Analyze", key=f"analyze_demo_{i}", use_container_width=True):
                        st.session_state.selected_paper = paper
                        st.session_state.app_page = "Paper Analysis"
                        st.rerun()
                with col2:
                    if st.button("💬 Discuss", key=f"discuss_demo_{i}", use_container_width=True):
                        st.session_state.chat_context = paper
                        st.session_state.app_page = "Chat Assistant"
                        st.rerun()
                with col3:
                    if st.button("🔖 Save", key=f"save_demo_{i}", use_container_width=True):
                        if st.session_state.current_user:
                            st.toast(f"Paper saved: {paper['title']}")
                        else:
                            st.toast("Please login to save papers", icon="⚠️")

        # Key benefits section
        st.markdown("<h2 class='sub-header' style='margin-top: 40px;'>Key Benefits</h2>", unsafe_allow_html=True)

        benefits_col1, benefits_col2 = st.columns(2)

        with benefits_col1:
            st.markdown("""
            * **Save Time**: Quickly find relevant research papers
            * **Deep Understanding**: AI-powered analysis of complex concepts
            * **Stay Current**: Access the latest research across disciplines
            """)

        with benefits_col2:
            st.markdown("""
            * **Comprehensive Insights**: Get thorough paper breakdowns
            * **Interactive Exploration**: Converse with AI about papers
            * **Personalized Experience**: Save and track your research interests
            """)

        # Recent activity if user is logged in
        if st.session_state.current_user:
            st.divider()
            st.markdown("<h2 class='sub-header'>Recent Activity</h2>", unsafe_allow_html=True)

            if st.session_state.research_history:
                for idx, item in enumerate(st.session_state.research_history[-5:]):
                    with st.expander(f"{item['type'].title()}: {item['title']}"):
                        st.markdown(f"**Date**: {item['date']}")
                        st.markdown(f"**Description**: {item['description']}")
            else:
                st.info("No recent activity. Start searching or analyzing papers!")

        # Bottom spacing for the navigation bar
        st.markdown("<div style='margin-bottom: 80px;'></div>", unsafe_allow_html=True)

    def _render_research_search(self):
        """Render research paper search interface"""
        st.markdown("<h1 class='main-header'>Research Paper Search</h1>", unsafe_allow_html=True)

        # Search form in a card
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="margin-bottom: 10px;">Search Parameters</h3>
        </div>
        """, unsafe_allow_html=True)

        with st.form(key="search_form"):
            col1, col2 = st.columns([3, 1])
            with col1:
                search_query = st.text_input("Enter your research topic or keywords", 
                                            placeholder="e.g., machine learning, quantum computing, climate change")
            with col2:
                search_source = st.selectbox("Source", 
                                            ["All Sources", "Semantic Scholar", "arXiv", "PubMed", "Google Scholar"])

            st.markdown("<div style='margin: 10px 0'></div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                year_range = st.slider("Publication Year", 1970, 2023, (2010, 2023))
            with col2:
                sort_by = st.selectbox("Sort By", ["Relevance", "Date", "Citation Count"])
            with col3:
                max_results = st.slider("Max Results", 10, 100, 30)

            search_button = st.form_submit_button("🔍 Search Papers", use_container_width=True)

        # Process search if button clicked
        if search_button and search_query:
            with st.spinner("Searching for papers..."):
                results = self.paper_manager.fetch_research_papers(
                    search_query, 
                    source=search_source if search_source != "All Sources" else None,
                    year_range=year_range,
                    sort_by=sort_by.lower(),
                    max_results=max_results
                )
                st.session_state.search_results = results

                # Add to history if user is logged in
                if st.session_state.current_user and results:
                    utils.add_to_history(
                        "search",
                        f"Search: {search_query}",
                        f"Found {len(results)} papers about {search_query}"
                    )

        # Display search results
        if st.session_state.search_results:
            st.markdown(f"<h2 class='sub-header'>Found {len(st.session_state.search_results)} papers</h2>", unsafe_allow_html=True)

            for idx, paper in enumerate(st.session_state.search_results):
                with st.container():
                    st.markdown(f"""
                    <div style="padding: 15px; border-radius: 8px; background-color: #f8f9fa; margin-bottom: 15px;">
                        <h3 style="margin: 0 0 10px 0; color: #1e3a8a;">{paper['title']}</h3>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**Authors**: {', '.join(paper['authors'])}")
                        st.markdown(f"**Published**: {paper['year']} | **Citations**: {paper['citation_count']}")
                        st.markdown(f"**Source**: {paper['source']}")
                        if paper.get('abstract'):
                            with st.expander("Abstract"):
                                st.markdown(f"<div style='padding: 10px; border-left: 3px solid #4A5AE2;'>{paper['abstract']}</div>", unsafe_allow_html=True)
                    with col2:
                        if st.button("🧠 Analyze", key=f"analyze_{idx}", use_container_width=True):
                            st.session_state.paper_analysis = self.paper_manager.analyze_paper(paper)
                            st.session_state.selected_papers = [paper]
                            # Update chat bot context
                            self.chat_bot.update_research_context([paper, st.session_state.paper_analysis])
                            # Switch to analysis page
                            st.rerun()

                        st.markdown("<div style='margin: 5px 0'></div>", unsafe_allow_html=True)
                        # Add to research collection
                        if st.button("💾 Save", key=f"save_{idx}", use_container_width=True):
                            if st.session_state.current_user:
                                if self.user_manager.save_paper(st.session_state.current_user['id'], paper):
                                    st.success("Paper saved to your collection!")
                            else:
                                st.warning("Please login to save papers to your collection.")

                st.divider()
        elif search_button and search_query:
            st.warning("No papers found matching your criteria. Try different keywords or filters.")

    def _render_paper_analysis(self):
        """Render paper analysis interface"""
        st.markdown("<h1 class='main-header'>Research Paper Analysis</h1>", unsafe_allow_html=True)

        # Check if we have a paper to analyze
        if not st.session_state.selected_papers:
            st.info("No paper selected for analysis. Please search and select a paper first.")
            st.markdown("""
            <div style="padding: 20px; border-radius: 10px; background-color: #f0f7ff; margin-top: 20px;">
                <h3>How to analyze a paper:</h3>
                <ol>
                    <li>Go to the Search Research tab</li>
                    <li>Search for papers on your topic of interest</li>
                    <li>Click the "Analyze" button on any paper you'd like to analyze</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            return

        paper = st.session_state.selected_papers[0]

        # Paper details section
        st.markdown(f"""
        <div style="padding: 15px; border-radius: 10px; background-color: #f8f9fa; margin-bottom: 20px;">
            <h2 style="color: #1e3a8a; margin-bottom: 10px;">{paper['title']}</h2>
            <p><strong>Authors:</strong> {', '.join(paper['authors'])}</p>
            <p><strong>Published:</strong> {paper['year']} | <strong>Source:</strong> {paper['source']}</p>
        </div>
        """, unsafe_allow_html=True)

        if paper.get('abstract'):
            with st.expander("📄 Abstract", expanded=True):
                st.markdown(f"<div style='padding: 10px; border-left: 3px solid #4A5AE2; background-color: #f8f9fa;'>{paper['abstract']}</div>", unsafe_allow_html=True)

        # If we haven't analyzed the paper yet, do it now
        if not st.session_state.paper_analysis:
            with st.spinner("🔍 Analyzing paper content..."):
                st.session_state.paper_analysis = self.paper_manager.analyze_paper(paper)

        analysis = st.session_state.paper_analysis

        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>AI-Powered Analysis</h2>", unsafe_allow_html=True)

        # Tabs for different analysis sections
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "💡 Key Findings", "🔬 Methodology", "🔮 Implications"])

        with tab1:
            st.markdown(f"""
            <div style="padding: 15px; background-color: #f8f9fa; border-radius: 10px; margin-top: 10px;">
                <h3>Summary</h3>
                <div style="padding: 10px; border-left: 3px solid #4A5AE2; margin-top: 10px;">
                    {analysis['summary']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("<h3>Key Findings</h3>", unsafe_allow_html=True)
            for idx, finding in enumerate(analysis['key_findings']):
                st.markdown(f"""
                <div style="padding: 15px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 10px;">
                    <h4 style="color: #1e3a8a;">{idx+1}. {finding['title']}</h4>
                    <p>{finding['description']}</p>
                </div>
                """, unsafe_allow_html=True)

        with tab3:
            st.markdown("<h3>Methodology</h3>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="padding: 15px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 15px;">
                <p>{analysis['methodology']['description']}</p>
            </div>
            """, unsafe_allow_html=True)

            if analysis['methodology'].get('steps'):
                st.markdown("<h4>Research Steps</h4>", unsafe_allow_html=True)
                for idx, step in enumerate(analysis['methodology']['steps']):
                    st.markdown(f"""
                    <div style="padding: 15px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 10px; border-left: 3px solid #4A5AE2;">
                        <h5>Step {idx+1}: {step['title']}</h5>
                        <p>{step['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)

        with tab4:
            st.markdown("<h3>Implications</h3>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="padding: 15px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 15px;">
                <p>{analysis['implications']['description']}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<h4>Research Gaps</h4>", unsafe_allow_html=True)
            gaps_html = ""
            for gap in analysis['implications']['research_gaps']:
                gaps_html += f"<li>{gap}</li>"

            st.markdown(f"""
            <div style="padding: 15px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 15px;">
                <ul>{gaps_html}</ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<h4>Future Directions</h4>", unsafe_allow_html=True)
            directions_html = ""
            for direction in analysis['implications']['future_directions']:
                directions_html += f"<li>{direction}</li>"

            st.markdown(f"""
            <div style="padding: 15px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 15px;">
                <ul>{directions_html}</ul>
            </div>
            """, unsafe_allow_html=True)

        # Action buttons
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if st.button("💬 Discuss in Chat", use_container_width=True):
                # Switch to chat tab with this paper context
                st.rerun()

        with col2:
            if st.session_state.current_user:
                if st.button("💾 Save Analysis", use_container_width=True):
                    self.user_manager.save_paper(st.session_state.current_user['id'], paper)
                    st.success("Paper saved to your collection!")
            else:
                st.button("💾 Save Analysis (Login Required)", disabled=True, use_container_width=True)

        with col3:
            if st.button("🔍 New Search", use_container_width=True):
                # Reset the analysis and go back to search
                st.session_state.selected_papers = []
                st.session_state.paper_analysis = {}
                st.rerun()

        # Add to history if user is logged in
        if st.session_state.current_user:
            utils.add_to_history(
                "analysis",
                f"Analysis: {paper['title']}",
                f"Analyzed research paper on {paper['title']}"
            )

    def _render_chat_assistant(self):
        """Render AI-powered research chat interface"""
        st.markdown("<h1 class='main-header'>Research Chat Assistant</h1>", unsafe_allow_html=True)

        # Initialize chat context
        if 'chat_context' not in st.session_state or st.session_state.selected_papers:
            if st.session_state.selected_papers and st.session_state.paper_analysis:
                st.session_state.chat_context = {
                    'papers': st.session_state.selected_papers,
                    'analysis': st.session_state.paper_analysis
                }
            else:
                st.session_state.chat_context = {'papers': [], 'analysis': {}}

        # Two column layout with context on the left and chat on the right
        context_col, chat_col = st.columns([1, 3])

        with context_col:
            st.markdown("<h3>Research Context</h3>", unsafe_allow_html=True)

            if st.session_state.chat_context['papers']:
                st.markdown("""
                <div style="background-color: #f0f7ff; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                    <h4 style="margin-top: 0;">Currently Discussing:</h4>
                </div>
                """, unsafe_allow_html=True)

                for paper in st.session_state.chat_context['papers']:
                    st.markdown(f"""
                    <div style="padding: 10px; border-left: 3px solid #4A5AE2; margin-bottom: 10px; background-color: #f8f9fa;">
                        <p style="font-weight: bold; margin-bottom: 5px;">{paper['title']}</p>
                        <p style="font-size: 0.9em; margin-bottom: 0;">({paper['year']}, {paper['source']})</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("""
                <div style="margin: 15px 0;">
                    <p>Ask specific questions about this paper such as:</p>
                    <ul>
                        <li>What are the key findings?</li>
                        <li>Explain the methodology</li>
                        <li>What are its implications?</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px;">
                    <p>No specific papers in context.</p>
                    <p>You can ask general research questions or search for papers first.</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div style="margin: 15px 0;">
                    <p>Try asking questions like:</p>
                    <ul>
                        <li>What are recent advances in machine learning?</li>
                        <li>Explain quantum computing basics</li>
                        <li>How does climate change affect biodiversity?</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            if st.button("🔍 Search Papers", use_container_width=True):
                # Redirect to search tab
                st.rerun()

        with chat_col:
            # Create a container with fixed height for scrollable chat history
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; margin-bottom: 15px;">
                <h3 style="margin: 0;">Research Conversation</h3>
            </div>
            """, unsafe_allow_html=True)

            # Display chat history in a stylized container
            chat_container = st.container()
            with chat_container:
                if not st.session_state.chat_history:
                    st.markdown("""
                    <div style="text-align: center; padding: 30px; color: #666;">
                        <p>Your conversation will appear here.</p>
                        <p>Start by asking a research question below.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    for message in st.session_state.chat_history:
                        if message['role'] == 'user':
                            st.markdown(f"""
                            <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                                <div style="background-color: #E9F2FF; padding: 10px 15px; border-radius: 15px 15px 0 15px; max-width: 80%;">
                                    <p style="margin: 0;">{message['content']}</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                                <div style="background-color: #F0F2F6; padding: 10px 15px; border-radius: 15px 15px 15px 0; max-width: 80%;">
                                    <p style="margin: 0;">{message['content']}</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

            # Input for new messages
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

            with st.form(key="chat_form", clear_on_submit=True):
                user_query = st.text_area(
                    "Ask a research-related question",
                    placeholder="Example: What are the main findings of this paper? How does it compare to related work?",
                    height=100
                )

                col1, col2 = st.columns([4, 1])
                with col2:
                    submit_button = st.form_submit_button("Send Message", use_container_width=True)

            if submit_button and user_query:
                # Add user message to history
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_query
                })

                # Generate response
                with st.spinner("Generating research insights..."):
                    response = self.chat_bot.generate_response(user_query)

                    # Add assistant response to history
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })

                    # Add to history if user is logged in
                    if st.session_state.current_user:
                        utils.add_to_history(
                            "chat",
                            f"Chat: {user_query[:50]}...",
                            f"Research conversation about {user_query[:100]}..."
                        )

                # Rerun to display the updated chat
                st.rerun()

    def _render_user_profile(self):
        """Render user profile management interface"""
        st.markdown("<h1 class='main-header'>User Profile</h1>", unsafe_allow_html=True)

        if not st.session_state.current_user:
            st.warning("Please login to view and manage your profile.")
            st.markdown("""
            <div style="padding: 20px; border-radius: 10px; background-color: #f0f7ff; margin-top: 20px; text-align: center;">
                <h3>Login Required</h3>
                <p>You need to login to access your profile, saved papers, and research history.</p>
                <p>Use the login form in the sidebar to access your account.</p>
            </div>
            """, unsafe_allow_html=True)
            return

        user = st.session_state.current_user

        # Profile overview tab system
        profile_tab, papers_tab, activity_tab = st.tabs(["📋 Profile", "📚 Saved Papers", "📝 Activity"])

        with profile_tab:
            # User info in a card
            st.markdown(f"""
            <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-bottom: 20px;">
                <h2 style="margin-top: 0;">Profile Information</h2>
                <div style="margin: 15px 0;">
                    <p><strong>Username:</strong> {user['username']}</p>
                    <p><strong>Email:</strong> {user['email']}</p>
                    <p><strong>Joined:</strong> {user['join_date']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Edit profile form
            st.markdown("<h3>Update Profile</h3>", unsafe_allow_html=True)
            with st.form("edit_profile_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_email = st.text_input("Email", value=user['email'])
                with col2:
                    st.write("Password Settings")
                    new_password = st.text_input("New Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")

                submit = st.form_submit_button("📝 Update Profile", use_container_width=True)

                if submit:
                    if new_password and new_password != confirm_password:
                        st.error("Passwords do not match!")
                    else:
                        updates = {'email': new_email}
                        if new_password:
                            updates['password'] = new_password

                        if self.user_manager.update_profile(user['id'], updates):
                            st.success("Profile updated successfully!")
                            # Update session state
                            st.session_state.current_user['email'] = new_email
                        else:
                            st.error("Failed to update profile!")

            # Account preferences
            st.markdown("<h3>Account Preferences</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.checkbox("Email notifications for new research", value=True)
                st.checkbox("Weekly research digest", value=False)
            with col2:
                st.checkbox("Save search history", value=True)
                st.checkbox("Personalized recommendations", value=True)

            if st.button("Save Preferences", use_container_width=True):
                st.success("Preferences saved successfully!")

        with papers_tab:
            st.markdown("<h2>Your Research Collection</h2>", unsafe_allow_html=True)

            # Get saved papers
            saved_papers = self.user_manager.get_saved_papers(user['id'])

            if saved_papers:
                # Sort options
                sort_col1, sort_col2, sort_col3 = st.columns([2, 2, 1])
                with sort_col1:
                    st.selectbox("Sort by", ["Date Saved", "Title", "Publication Year", "Citations"])
                with sort_col2:
                    st.selectbox("Filter by source", ["All Sources", "Semantic Scholar", "arXiv", "PubMed"])
                with sort_col3:
                    st.button("🔄 Apply", use_container_width=True)

                st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

                for idx, paper in enumerate(saved_papers):
                    with st.container():
                        st.markdown(f"""
                        <div style="padding: 15px; border-radius: 8px; background-color: #f8f9fa; margin-bottom: 15px;">
                            <h3 style="margin: 0 0 10px 0; color: #1e3a8a;">{paper['title']}</h3>
                        </div>
                        """, unsafe_allow_html=True)

                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**Authors**: {', '.join(paper['authors'])}")
                            st.markdown(f"**Published**: {paper['year']} | **Citations**: {paper['citation_count']}")
                            st.markdown(f"**Source**: {paper['source']}")

                            if paper.get('abstract'):
                                with st.expander("View Abstract"):
                                    st.markdown(f"<div style='padding: 10px; border-left: 3px solid #4A5AE2;'>{paper['abstract']}</div>", unsafe_allow_html=True)

                        with col2:
                            st.button("🧠 Analyze", key=f"analyze_saved_{idx}", use_container_width=True)
                            st.markdown("<div style='margin: 5px 0;'></div>", unsafe_allow_html=True)
                            st.button("💬 Discuss", key=f"discuss_saved_{idx}", use_container_width=True)
                            st.markdown("<div style='margin: 5px 0;'></div>", unsafe_allow_html=True)
                            if st.button("🗑️ Remove", key=f"remove_saved_{idx}", use_container_width=True):
                                if self.user_manager.remove_saved_paper(user['id'], paper['id']):
                                    st.success("Paper removed from your collection!")
                                    st.rerun()
                        st.divider()
            else:
                st.markdown("""
                <div style="padding: 30px; border-radius: 10px; background-color: #f0f7ff; text-align: center; margin-top: 20px;">
                    <h3>Your collection is empty</h3>
                    <p>You haven't saved any papers yet.</p>
                    <p>Search for papers and save them to build your research collection.</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button("🔍 Search Papers Now", use_container_width=True):
                    # Redirect to search
                    st.rerun()

        with activity_tab:
            st.markdown("<h2>Your Research Activity</h2>", unsafe_allow_html=True)

            # Activity metrics
            metrics_row = st.columns(4)
            with metrics_row[0]:
                searches = len([item for item in st.session_state.research_history if item['type'] == 'search'])
                st.metric("Searches", searches)
            with metrics_row[1]:
                analyses = len([item for item in st.session_state.research_history if item['type'] == 'analysis'])
                st.metric("Analyses", analyses)
            with metrics_row[2]:
                chats = len([item for item in st.session_state.research_history if item['type'] == 'chat'])
                st.metric("Chat Sessions", chats)
            with metrics_row[3]:
                saved = len(saved_papers) if saved_papers else 0
                st.metric("Saved Papers", saved)

            # Activity timeline
            st.markdown("<h3>Recent Activity</h3>", unsafe_allow_html=True)

            if st.session_state.research_history:
                for idx, item in enumerate(st.session_state.research_history[-15:]):
                    st.markdown(f"""
                    <div style="padding: 12px; border-radius: 8px; background-color: #f8f9fa; margin-bottom: 8px; 
                         border-left: 3px solid {'#4A5AE2' if item['type'] == 'search' else '#7E57C2' if item['type'] == 'analysis' else '#26A69A'}">
                        <p style="margin: 0; font-size: 0.9em; color: #666;">{item['date']}</p>
                        <p style="margin: 5px 0; font-weight: bold;">{item['title']}</p>
                        <p style="margin: 0; font-size: 0.9em;">{item['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No activity recorded yet. Start searching or analyzing papers!")

    def _render_app_settings(self):
        """Render application settings interface"""
        st.markdown("<h1 class='main-header'>Application Settings</h1>", unsafe_allow_html=True)

        # Settings tabs
        api_tab, ai_tab, display_tab, advanced_tab = st.tabs(["🔌 API", "🧠 AI Model", "🎨 Display", "⚙️ Advanced"])

        with api_tab:
            st.markdown("<h2>Research API Configuration</h2>", unsafe_allow_html=True)
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background-color: #f0f7ff; margin-bottom: 20px;">
                <p><strong>Note:</strong> Configure which academic APIs to use for research paper retrieval.</p>
            </div>
            """, unsafe_allow_html=True)

            api_col1, api_col2 = st.columns(2)

            with api_col1:
                st.markdown("<h3>Available Sources</h3>", unsafe_allow_html=True)
                use_semantic = st.checkbox("Semantic Scholar API", value=True, 
                                        help="Access papers from all scientific domains with rich metadata")
                use_arxiv = st.checkbox("arXiv API", value=True,
                                      help="Specialized for physics, mathematics, computer science")
                use_pubmed = st.checkbox("PubMed API", value=True,
                                       help="Access medical and biological sciences research")
                use_google = st.checkbox("Google Scholar API", value=False,
                                       help="Broad coverage but with API limitations")

            with api_col2:
                st.markdown("<h3>API Keys (Optional)</h3>", unsafe_allow_html=True)
                st.text_input("Semantic Scholar API Key", placeholder="Enter API key for higher rate limits")
                st.text_input("PubMed API Key", placeholder="Enter API key for additional features")
                st.text_input("Custom API Key", placeholder="For additional services")

            if st.button("💾 Save API Configuration", use_container_width=True):
                st.success("API settings saved successfully!")

        with ai_tab:
            st.markdown("<h2>AI Model Settings</h2>", unsafe_allow_html=True)
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background-color: #f0f7ff; margin-bottom: 20px;">
                <p><strong>Configure how the AI analyzes papers and generates responses.</strong></p>
                <p>Higher values provide more detailed results but may take longer to process.</p>
            </div>
            """, unsafe_allow_html=True)

            ai_col1, ai_col2 = st.columns(2)

            with ai_col1:
                st.markdown("<h3>Analysis Settings</h3>", unsafe_allow_html=True)
                st.slider("Research Depth", 1, 5, 3, 
                         help="Controls how deep the AI analyzes papers. Higher values mean more detailed analysis but slower response.")
                st.slider("Citation Analysis", 1, 5, 3,
                         help="How thoroughly the AI analyzes citation relationships between papers")
                st.selectbox("Analysis Language", ["English", "Spanish", "French", "German", "Chinese", "Japanese"])

            with ai_col2:
                st.markdown("<h3>Response Settings</h3>", unsafe_allow_html=True)
                st.slider("Response Detail Level", 1, 5, 3, 
                         help="Controls the detail level in AI responses. Higher values mean more detailed responses.")
                st.slider("Academic Language Level", 1, 5, 3,
                         help="Controls how technical the AI responses are, from simple to highly technical")
                st.multiselect("Focus Areas", 
                              ["Methodology", "Key Findings", "Theoretical Contributions", "Practical Applications", "Limitations"],
                              default=["Key Findings", "Methodology"])

            if st.button("💾 Save AI Settings", use_container_width=True):
                st.success("AI model settings saved successfully!")

        with display_tab:
            st.markdown("<h2>Display & Interface Settings</h2>", unsafe_allow_html=True)

            display_col1, display_col2 = st.columns(2)

            with display_col1:
                st.markdown("<h3>Theme Settings</h3>", unsafe_allow_html=True)
                theme_mode = st.radio("Color Theme", ["Light", "Dark", "System Default"])
                accent_color = st.color_picker("Accent Color", "#4A5AE2")
                st.selectbox("Font Family", ["System Default", "Sans Serif", "Serif", "Monospace"])
                st.slider("Font Size", 80, 120, 100, 5, format="%d%%")

            with display_col2:
                st.markdown("<h3>Layout Settings</h3>", unsafe_allow_html=True)
                st.checkbox("Compact View", value=False, help="Use a more compact UI with less whitespace")
                st.checkbox("Show Paper Thumbnails", value=True, help="Display paper thumbnails when available")
                st.number_input("Results Per Page", min_value=5, max_value=50, value=10)
                st.selectbox("Default Sort Order", ["Relevance", "Date (Newest)", "Date (Oldest)", "Citations (High to Low)"])

            st.markdown("<h3>Preview</h3>", unsafe_allow_html=True)
            preview_tabs = st.tabs(["Light Theme", "Dark Theme"])

            with preview_tabs[0]:
                st.markdown("""
                <div style="padding: 15px; border-radius: 10px; background-color: #f8f9fa; margin-top: 10px;">
                    <h4 style="color: #1e3a8a;">Sample Research Paper</h4>
                    <p><strong>Authors:</strong> John Smith, Jane Doe</p>
                    <p><strong>Abstract:</strong> This is how research papers will appear with the selected settings.</p>
                </div>
                """, unsafe_allow_html=True)

            with preview_tabs[1]:
                st.markdown("""
                <div style="padding: 15px; border-radius: 10px; background-color: #1e1e1e; color: #f0f0f0; margin-top: 10px;">
                    <h4 style="color: #6c8eff;">Sample Research Paper</h4>
                    <p><strong>Authors:</strong> John Smith, Jane Doe</p>
                    <p><strong>Abstract:</strong> This is how research papers will appear with the selected settings.</p>
                </div>
                """, unsafe_allow_html=True)

            if st.button("💾 Save Display Settings", use_container_width=True):
                st.success("Display settings saved successfully!")

        with advanced_tab:
            st.markdown("<h2>Advanced Settings</h2>", unsafe_allow_html=True)

            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background-color: #ffe8e8; margin-bottom: 20px;">
                <h4 style="color: #c62828; margin-top: 0;">⚠️ Advanced Options</h4>
                <p>These settings are for advanced users. Incorrect configuration may affect application performance.</p>
            </div>
            """, unsafe_allow_html=True)

            adv_col1, adv_col2 = st.columns(2)

            with adv_col1:
                st.markdown("<h3>Cache Settings</h3>", unsafe_allow_html=True)
                st.checkbox("Enable Paper Caching", value=True, help="Cache paper data to improve performance")
                st.number_input("Cache Timeout (hours)", min_value=1, max_value=168, value=24)
                st.checkbox("Cache AI Analysis Results", value=True)

                st.markdown("<h3>Request Settings</h3>", unsafe_allow_html=True)
                st.number_input("API Request Timeout (seconds)", min_value=5, max_value=60, value=30)
                st.number_input("Max Concurrent Requests", min_value=1, max_value=10, value=3)

            with adv_col2:
                st.markdown("<h3>Data Export/Import</h3>", unsafe_allow_html=True)
                st.download_button("Export All Settings", "settings_data", "research_assistant_settings.json")
                uploaded_file = st.file_uploader("Import Settings", type=["json"])

                st.markdown("<h3>System</h3>", unsafe_allow_html=True)
                st.button("Clear All Cache", help="Remove all cached data from the system")
                st.button("Reset to Default Settings", help="Reset all settings to their default values")

            if st.button("💾 Save Advanced Settings", use_container_width=True):
                st.success("Advanced settings saved successfully!")