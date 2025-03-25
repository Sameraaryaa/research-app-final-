from typing import List, Dict, Any, Optional
import os
import random
import streamlit as st
from datetime import datetime
from database import get_database

class ResearchChatBot:
    def __init__(self, research_context: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize chat bot with research context
        
        Args:
            research_context (List): List of research papers and their analyses
        """
        self.research_context = research_context or []
        
        # Get database connection
        self.db = get_database()
        
        # Initialize chat history in session state if not already present
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            
        # Try to get API key from environment variables
        self.llm_api_key = os.getenv("LLM_API_KEY", "")
        
    def update_research_context(self, context: List[Dict[str, Any]]):
        """
        Update the research context for the chat bot
        
        Args:
            context (List): New research context
        """
        self.research_context = context
        
    def generate_response(self, user_query: str, user_id: int = None) -> str:
        """
        Generate AI-powered research response
        
        Args:
            user_query (str): User's research question
            user_id (int): Optional user ID for saving to history
        
        Returns:
            Comprehensive research-based response
        """
        # In a real implementation, this would call an LLM API
        
        try:
            # Check if we have paper context to work with
            has_paper_context = len(self.research_context) > 0
            
            # Process the query to determine its type
            query_lower = user_query.lower()
            
            # Add query to session state chat history
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
                
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Add user query to chat history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_query,
                "timestamp": timestamp
            })
            
            # Save to database if user is logged in
            if user_id:
                paper_context = None
                if has_paper_context and len(self.research_context) > 0:
                    paper_context = self.research_context[0].get('title', 'Unknown paper')
                    
                # Add to research history
                self.db.add_history_item(
                    user_id=user_id,
                    activity_type="chat",
                    title=f"Chat: {user_query[:50]}...",
                    description=f"Question about {paper_context if paper_context else 'research'}"
                )
            
            # Generate appropriate response based on query type and context
            
            # 1. Summary request
            if "summary" in query_lower or "summarize" in query_lower:
                if has_paper_context:
                    paper = self.research_context[0]
                    response = f"Here's a summary of the paper '{paper.get('title', 'the selected paper')}':\n\n" + \
                           f"This research by {', '.join(paper.get('authors', ['the authors']))} " + \
                           f"investigates {paper.get('title', 'the topic').lower()}. " + \
                           f"\n\nThe paper makes several key contributions:\n" + \
                           f"1. Development of novel methodologies for addressing challenges in this domain\n" + \
                           f"2. Empirical evidence supporting the effectiveness of the proposed approach\n" + \
                           f"3. Theoretical foundations that advance our understanding of the underlying principles\n\n" + \
                           f"The research is particularly notable for its rigorous methodology and comprehensive analysis."
                else:
                    response = "I don't currently have a specific paper in context to summarize. " + \
                           "Please search for and select a paper first, or ask a more general research question."
                           
                # Add response to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                return response
            
            # 2. Key findings request
            elif "findings" in query_lower or "results" in query_lower or "discover" in query_lower:
                if has_paper_context:
                    paper = self.research_context[0]
                    if isinstance(self.research_context[1], dict) and 'key_findings' in self.research_context[1]:
                        findings = self.research_context[1]['key_findings']
                        response = f"The key findings of '{paper.get('title', 'the paper')}' include:\n\n"
                        for i, finding in enumerate(findings):
                            response += f"{i+1}. **{finding['title']}**: {finding['description']}\n\n"
                        return response
                    else:
                        return f"The paper '{paper.get('title', 'selected')}' presents several important findings, " + \
                               f"including methodological innovations, empirical results supporting their hypotheses, " + \
                               f"and theoretical contributions to the field."
                else:
                    return "I don't have a specific paper in context to discuss findings. " + \
                           "Please select a paper first, or ask a more general research question."
            
            # 3. Methodology question
            elif "method" in query_lower or "approach" in query_lower or "how did they" in query_lower:
                if has_paper_context:
                    paper = self.research_context[0]
                    if isinstance(self.research_context[1], dict) and 'methodology' in self.research_context[1]:
                        methodology = self.research_context[1]['methodology']
                        response = f"The methodology in '{paper.get('title', 'the paper')}' is as follows:\n\n"
                        response += methodology['description'] + "\n\n"
                        if 'steps' in methodology and methodology['steps']:
                            response += "The research process involved these key steps:\n\n"
                            for i, step in enumerate(methodology['steps']):
                                response += f"{i+1}. **{step['title']}**: {step['description']}\n\n"
                        return response
                    else:
                        return f"The researchers employed a multi-faceted methodology combining quantitative analysis " + \
                               f"with qualitative assessments. Their approach involved data collection from multiple sources, " + \
                               f"rigorous preprocessing, model development, and comprehensive evaluation against established benchmarks."
                else:
                    return "I don't have a specific paper in context to discuss methodology. " + \
                           "If you're asking about research methods in general, please specify which area or approach you're interested in."
            
            # 4. Implications or future work
            elif any(term in query_lower for term in ["implications", "impact", "future", "next steps"]):
                if has_paper_context:
                    paper = self.research_context[0]
                    if isinstance(self.research_context[1], dict) and 'implications' in self.research_context[1]:
                        implications = self.research_context[1]['implications']
                        response = f"**Implications of '{paper.get('title', 'the paper')}':**\n\n"
                        response += implications['description'] + "\n\n"
                        
                        response += "**Research Gaps Identified:**\n"
                        for gap in implications['research_gaps']:
                            response += f"- {gap}\n"
                        
                        response += "\n**Future Research Directions:**\n"
                        for direction in implications['future_directions']:
                            response += f"- {direction}\n"
                        
                        return response
                    else:
                        return f"The research has several important implications for both theory and practice. " + \
                               f"It extends our understanding of {paper.get('title', 'the subject').lower()} and " + \
                               f"provides practical approaches that can be applied in real-world scenarios. " + \
                               f"Future work could explore additional domains, incorporate more diverse datasets, " + \
                               f"and develop more efficient computational methods."
                else:
                    return "To discuss research implications, it would be helpful to have a specific paper in context. " + \
                           "Please select a paper first, or specify which research area you're interested in."
            
            # 5. Compare papers (if we had multiple papers in context)
            elif "compare" in query_lower or "difference" in query_lower or "similar" in query_lower:
                return "To compare multiple papers, please select at least two papers from your search results. " + \
                       "Currently, our system allows detailed analysis of one paper at a time, but we're working " + \
                       "on adding multi-paper comparison features in the future."
            
            # 6. General response for other queries
            else:
                if has_paper_context:
                    paper = self.research_context[0]
                    return f"Regarding your question about {user_query}, in the context of '{paper.get('title', 'the selected paper')}':\n\n" + \
                           f"The paper addresses aspects related to your question through its {random.choice(['innovative', 'comprehensive', 'novel'])} " + \
                           f"approach to {paper.get('title', 'the research topic').lower()}. The authors provide insights that " + \
                           f"contribute to our understanding of this area, specifically through their analysis of relevant factors " + \
                           f"and the implications of their findings for both theory and practice.\n\n" + \
                           f"For more specific information, you might consider asking about the paper's methodology, key findings, " + \
                           f"or broader implications."
                else:
                    return f"To provide a more informed response about {user_query}, it would be helpful to have a specific " + \
                           f"research paper in context. You can search for relevant papers using the Search function, or I can " + \
                           f"try to answer your question based on general knowledge in this field.\n\n" + \
                           f"Would you like to search for papers related to this topic, or would you prefer a general overview?"
        
        except Exception as e:
            print(f"Error generating chat response: {e}")
            return "I apologize, but I encountered an error while processing your question. Please try asking in a different way or search for specific papers to provide more context."
