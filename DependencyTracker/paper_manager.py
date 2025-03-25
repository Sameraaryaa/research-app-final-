import requests
import json
import os
import streamlit as st
from typing import List, Dict, Any
from datetime import datetime
from database import get_database

class ResearchPaperManager:
    def __init__(self):
        """
        Initialize the Research Paper Manager
        """
        # Get database instance
        self.db = get_database()
        
        # API keys (from environment variables)
        self.semantic_scholar_api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
        self.arxiv_api_key = os.getenv("ARXIV_API_KEY", "")
        self.pubmed_api_key = os.getenv("PUBMED_API_KEY", "")
        
        # API endpoints
        self.semantic_scholar_endpoint = "https://api.semanticscholar.org/v1/paper/"
        self.arxiv_endpoint = "http://export.arxiv.org/api/query"
        self.pubmed_endpoint = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        
    def fetch_research_papers(self, 
                             query: str, 
                             source: str = None, 
                             year_range: tuple = (1900, 2023),
                             sort_by: str = "relevance",
                             max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch research papers from multiple sources
        
        Args:
            query (str): Search query for research papers
            source (str): Specific source to search (None for all sources)
            year_range (tuple): Range of publication years to include
            sort_by (str): How to sort results (relevance, date, citation_count)
            max_results (int): Maximum number of papers to retrieve
        
        Returns:
            List of research paper dictionaries
        """
        papers = []
        
        # Create a search key for caching
        if source is None:
            source_key = "all"
        else:
            source_key = source.lower().replace(" ", "_")
            
        search_key = f"{query}_{source_key}_{year_range[0]}_{year_range[1]}_{sort_by}"
        
        # Check if we have this search cached in session state
        if 'paper_search_cache' not in st.session_state:
            st.session_state.paper_search_cache = {}
            
        if search_key in st.session_state.paper_search_cache:
            return st.session_state.paper_search_cache[search_key]
            
        # Determine which sources to query
        sources_to_query = []
        if source is None:
            sources_to_query = ["semantic_scholar", "arxiv", "pubmed"]
        else:
            if source.lower() == "semantic scholar":
                sources_to_query = ["semantic_scholar"]
            elif source.lower() == "arxiv":
                sources_to_query = ["arxiv"]
            elif source.lower() == "pubmed":
                sources_to_query = ["pubmed"]
            elif source.lower() == "google scholar":
                sources_to_query = []  # Google Scholar doesn't have a public API
        
        # Query each source
        if "semantic_scholar" in sources_to_query:
            semantic_papers = self._fetch_from_semantic_scholar(query, year_range, max_results)
            papers.extend(semantic_papers)
            
        if "arxiv" in sources_to_query:
            arxiv_papers = self._fetch_from_arxiv(query, year_range, max_results)
            papers.extend(arxiv_papers)
            
        if "pubmed" in sources_to_query:
            pubmed_papers = self._fetch_from_pubmed(query, year_range, max_results)
            papers.extend(pubmed_papers)
            
        # Store papers in database for future reference
        for paper in papers:
            self.db.add_paper(paper)
            
        # Cache results in session state
        st.session_state.paper_search_cache[search_key] = papers
        
        # In a real implementation, we would sort the papers according to the sort_by parameter
        # Here we're just simulating that behavior with a mock sort
        if sort_by == "date":
            papers.sort(key=lambda x: x.get('year', 0), reverse=True)
        elif sort_by == "citation_count":
            papers.sort(key=lambda x: x.get('citation_count', 0), reverse=True)
        
        # Limit the number of results
        return papers[:max_results]
    
    def _fetch_from_semantic_scholar(self, query: str, year_range: tuple, max_results: int) -> List[Dict[str, Any]]:
        """
        Fetch papers from Semantic Scholar API
        """
        try:
            # This is a simplified example. In a real implementation,
            # you would use the actual Semantic Scholar API with proper pagination
            
            # For the purpose of this example, let's return sample data
            # In a real implementation, you would make an actual API call:
            
            """
            headers = {"x-api-key": self.semantic_scholar_api_key} if self.semantic_scholar_api_key else {}
            params = {
                "query": query,
                "year": f"{year_range[0]}-{year_range[1]}",
                "limit": max_results
            }
            response = requests.get(self.semantic_scholar_endpoint + "search", params=params, headers=headers)
            if response.status_code == 200:
                return response.json().get('papers', [])
            """
            
            # Sample data for demonstration purposes
            papers = [
                {
                    "id": "sem1",
                    "title": "Attention Is All You Need",
                    "authors": ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"],
                    "year": 2017,
                    "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
                    "citation_count": 45000,
                    "source": "Semantic Scholar",
                    "url": "https://api.semanticscholar.org/v1/paper/sem1"
                },
                {
                    "id": "sem2",
                    "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
                    "authors": ["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee", "Kristina Toutanova"],
                    "year": 2018,
                    "abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers.",
                    "citation_count": 35000,
                    "source": "Semantic Scholar",
                    "url": "https://api.semanticscholar.org/v1/paper/sem2"
                }
            ]
            
            return papers
        
        except Exception as e:
            print(f"Error fetching papers from Semantic Scholar: {e}")
            return []
    
    def _fetch_from_arxiv(self, query: str, year_range: tuple, max_results: int) -> List[Dict[str, Any]]:
        """
        Fetch papers from arXiv API
        """
        try:
            # This is a simplified example. In a real implementation,
            # you would use the actual arXiv API with proper pagination
            
            # For the purpose of this example, let's return sample data
            # In a real implementation, you would make an actual API call:
            
            """
            params = {
                "search_query": f"all:{query} AND submittedDate:[{year_range[0]} TO {year_range[1]}]",
                "max_results": max_results,
                "sortBy": "relevance",
                "sortOrder": "descending"
            }
            response = requests.get(self.arxiv_endpoint, params=params)
            if response.status_code == 200:
                # Parse XML response and convert to our standard format
                # This would require more complex logic in a real implementation
                return parsed_papers
            """
            
            # Sample data for demonstration purposes
            papers = [
                {
                    "id": "arxiv1",
                    "title": "GPT-4 Technical Report",
                    "authors": ["OpenAI Team"],
                    "year": 2023,
                    "abstract": "We report the development of GPT-4, a large-scale, multimodal model which can accept image and text inputs and produce text outputs. While less capable than humans in many real-world scenarios, GPT-4 exhibits human-level performance on various professional and academic benchmarks.",
                    "citation_count": 500,
                    "source": "arXiv",
                    "url": "https://arxiv.org/abs/arxiv1"
                },
                {
                    "id": "arxiv2",
                    "title": "Language Models are Few-Shot Learners",
                    "authors": ["Tom B. Brown", "Benjamin Mann", "Nick Ryder"],
                    "year": 2020,
                    "abstract": "Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of text followed by fine-tuning on a specific task. We demonstrate that by scaling up language models, they become increasingly capable of performing tasks that they were not explicitly trained on.",
                    "citation_count": 12000,
                    "source": "arXiv",
                    "url": "https://arxiv.org/abs/arxiv2"
                }
            ]
            
            return papers
        
        except Exception as e:
            print(f"Error fetching papers from arXiv: {e}")
            return []
    
    def _fetch_from_pubmed(self, query: str, year_range: tuple, max_results: int) -> List[Dict[str, Any]]:
        """
        Fetch papers from PubMed API
        """
        try:
            # This is a simplified example. In a real implementation,
            # you would use the actual PubMed API with proper pagination
            
            # For the purpose of this example, let's return sample data
            # In a real implementation, you would make an actual API call:
            
            """
            # First get the IDs of matching papers
            params = {
                "db": "pubmed",
                "term": f"{query} AND ({year_range[0]}[PDAT]:{year_range[1]}[PDAT])",
                "retmax": max_results,
                "retmode": "json",
                "api_key": self.pubmed_api_key
            }
            response = requests.get(self.pubmed_endpoint, params=params)
            if response.status_code == 200:
                paper_ids = response.json().get('esearchresult', {}).get('idlist', [])
                
                # Then fetch details for each paper
                # This would require additional API calls in a real implementation
                return detailed_papers
            """
            
            # Sample data for demonstration purposes
            papers = [
                {
                    "id": "pubmed1",
                    "title": "The role of AI in genomics and precision medicine",
                    "authors": ["Sarah Johnson", "Michael Chen"],
                    "year": 2022,
                    "abstract": "Artificial intelligence is transforming genomics and precision medicine by enabling more accurate analysis of complex genomic data. This review examines recent advances in AI-based genomic analysis and their implications for personalized healthcare.",
                    "citation_count": 150,
                    "source": "PubMed",
                    "url": "https://pubmed.ncbi.nlm.nih.gov/pubmed1"
                },
                {
                    "id": "pubmed2",
                    "title": "Neural basis of language comprehension",
                    "authors": ["David Miller", "Jennifer Smith"],
                    "year": 2021,
                    "abstract": "This fMRI study investigates the neural mechanisms underlying language comprehension in different contexts. Results indicate a distributed network of brain regions involved in semantic processing, with significant implications for understanding language disorders.",
                    "citation_count": 85,
                    "source": "PubMed",
                    "url": "https://pubmed.ncbi.nlm.nih.gov/pubmed2"
                }
            ]
            
            return papers
        
        except Exception as e:
            print(f"Error fetching papers from PubMed: {e}")
            return []
    
    def analyze_paper(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform AI-powered analysis of a research paper
        
        Args:
            paper (Dict): Research paper details
        
        Returns:
            Analyzed paper insights
        """
        try:
            # First, add the paper to the database if it's not already there
            paper_db_id = self.db.add_paper(paper)
            if not paper_db_id:
                # If there's an error adding the paper to the database
                return {"error": "Failed to process paper for analysis"}
                
            # Check if we already have an analysis for this paper
            existing_analysis = self.db.get_paper_analysis(paper_db_id)
            if existing_analysis:
                # Return the cached analysis
                return existing_analysis
                
            # If we don't have analysis yet, generate it
            # Extract paper information
            title = paper['title']
            abstract = paper.get('abstract', '')
            authors = paper.get('authors', [])
            year = paper.get('year', '')
            
            # Generate analysis (in a real implementation, this would use NLP/AI)
            analysis = {
                "summary": f"This paper by {', '.join(authors[:3])} ({year}) explores {title.lower()}. " +
                          f"The research presents innovative approaches to understand and address challenges in this domain. " +
                          f"The work contributes significantly to the field by providing new methodologies and insights.",
                
                "key_findings": [
                    {
                        "title": "Novel methodology developed",
                        "description": "The authors developed a new approach that improves upon existing methods by incorporating advanced techniques and algorithms."
                    },
                    {
                        "title": "Significant performance improvements",
                        "description": "Experimental results demonstrate substantial improvements over baseline methods, with up to 30% better performance on standard benchmarks."
                    },
                    {
                        "title": "Important theoretical contributions",
                        "description": "The paper makes notable theoretical contributions by extending existing frameworks and proposing new mathematical formulations."
                    }
                ],
                
                "methodology": {
                    "description": "The research employs a multi-stage approach combining quantitative and qualitative methods to address the research questions.",
                    "steps": [
                        {
                            "title": "Data collection and preprocessing",
                            "description": "Comprehensive dataset compilation from multiple sources, followed by rigorous cleaning and normalization."
                        },
                        {
                            "title": "Model development and implementation",
                            "description": "Design and implementation of novel computational models tailored to the specific research problem."
                        },
                        {
                            "title": "Experimental evaluation",
                            "description": "Extensive evaluation using both established benchmarks and custom test scenarios to validate the approach."
                        }
                    ]
                },
                
                "implications": {
                    "description": "This research has significant implications for both theory and practice in the field.",
                    "research_gaps": [
                        "Limited evaluation in real-world settings",
                        "Computational efficiency challenges for large-scale applications",
                        "Need for more diverse datasets to ensure generalizability"
                    ],
                    "future_directions": [
                        "Extending the approach to related problem domains",
                        "Incorporating additional data sources to enhance performance",
                        "Developing more efficient implementations for resource-constrained environments"
                    ]
                }
            }
            
            # Save analysis to database for future use
            self.db.save_paper_analysis(paper_db_id, analysis)
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing paper: {e}")
            return {
                "summary": "Unable to analyze paper due to an error.",
                "key_findings": [],
                "methodology": {"description": "Not available", "steps": []},
                "implications": {"description": "Not available", "research_gaps": [], "future_directions": []}
            }
