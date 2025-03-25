import streamlit as st
from research_assistant import ResearchAssistantApp

def main():
    """
    Main entry point for the Research Assistant application.
    """
    # Initialize the Research Assistant App
    app = ResearchAssistantApp()
    app.run()

if __name__ == "__main__":
    main()
