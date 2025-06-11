from typing import List, Dict, Optional, Tuple
import re
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import json
import time
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage

@dataclass
class LibraryInfo:
    name: str
    version: Optional[str] = None
    is_niche: bool = False
    popularity_score: Optional[float] = None
    documentation_url: Optional[str] = None

class LibraryAnalyzer:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        """Initialize the library analyzer with common libraries and APIs."""
        # Common Python libraries that are well-documented and widely used
        self.common_libraries = {
            'requests', 'numpy', 'pandas', 'tensorflow', 'pytorch', 'scikit-learn',
            'flask', 'django', 'fastapi', 'sqlalchemy', 'pytest', 'unittest',
            'matplotlib', 'seaborn', 'pillow', 'opencv-python', 'beautifulsoup4',
            'selenium', 'scrapy', 'aiohttp', 'asyncio', 'pymongo', 'redis',
            'celery', 'airflow', 'streamlit', 'gradio', 'transformers', 'spacy',
            'nltk', 'gensim', 'pyspark', 'dask', 'ray', 'fastai', 'keras',
            'plotly', 'bokeh', 'dash', 'pygame', 'pyqt', 'tkinter', 'wxpython'
        }
        
        # Common APIs that are well-documented
        self.common_apis = {
            'rest', 'graphql', 'grpc', 'soap', 'openai', 'aws', 'azure',
            'google cloud', 'firebase', 'stripe', 'twilio', 'sendgrid',
            'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'slack',
            'discord', 'telegram', 'whatsapp', 'facebook', 'twitter', 'instagram',
            'linkedin', 'youtube', 'spotify', 'paypal', 'square', 'shopify'
        }
        
        # Cache for library popularity scores
        self.popularity_cache = {}
        
        # Initialize LLM for fallback detection
        self.llm = ChatOpenAI(model=model_name, max_tokens=50)
        self._setup_llm_agent()
        
    def _setup_llm_agent(self):
        """Set up the LLM agent for library detection."""
        # Create a tool for library detection
        detect_libraries_tool = Tool(
            name="detect_libraries",
            func=lambda x: x,  # Placeholder, actual detection is in the prompt
            description="Detect libraries and APIs mentioned in the text. Return a JSON array of library names."
        )
        
        # Create the system message
        system_message = SystemMessage(content="""You are a library detection agent. Your task is to identify any niche programming libraries, frameworks, or APIs mentioned in the text.
        You are only supposed to that are very uncommon, which might not have been used by many people and has very less documentation. The kind of apis and libraries on which an LLM might fail in code generation.
        Return ONLY a JSON array of library names, nothing else. Example: ["obscure-lib", "pypdf345", "pytorch-molecule"].
        If no libraries are mentioned, return an empty array: [].
        Do not include explanations or any other text.""")
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            system_message,
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_openai_tools_agent(self.llm, [detect_libraries_tool], prompt)
        
        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=[detect_libraries_tool],
            verbose=False
        )

    def _detect_libraries_with_llm(self, text: str) -> List[str]:
        """Use LLM to detect libraries in text when pattern matching fails."""
        try:
            response = self.agent_executor.invoke({"input": text})
            # Parse the response as JSON
            libraries = json.loads(response["output"])
            return libraries if isinstance(libraries, list) else []
        except Exception as e:
            print(f"Error in LLM library detection: {e}")
            return []

    def _extract_version(self, text: str, library_name: str) -> Optional[str]:
        """Extract version number for a library if mentioned."""
        # Common version patterns
        patterns = [
            rf"{library_name}[=<>~!]+\s*([\d.]+)",  # pip-style: library==1.2.3
            rf"{library_name}\s+([\d.]+)",          # space-separated: library 1.2.3
            rf"version\s+([\d.]+)\s+of\s+{library_name}",  # version 1.2.3 of library
            rf"{library_name}\s+version\s+([\d.]+)"  # library version 1.2.3
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _get_pypi_stats(self, library_name: str) -> Optional[float]:
        """Get library popularity score from PyPI."""
        if library_name in self.popularity_cache:
            return self.popularity_cache[library_name]
            
        try:
            url = f"https://pypi.org/pypi/{library_name}/json"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # Use download count as popularity metric
                downloads = data.get('info', {}).get('downloads', {}).get('last_month', 0)
                self.popularity_cache[library_name] = downloads
                return downloads
        except Exception:
            pass
        return None

    def _is_niche_library(self, library_name: str, version: Optional[str] = None) -> bool:
        """Determine if a library is niche based on popularity and documentation."""
        # Check if it's in our common libraries list
        if library_name.lower() in self.common_libraries:
            return False
            
        # Get PyPI stats
        popularity = self._get_pypi_stats(library_name)
        if popularity is not None:
            # Consider libraries with less than 1000 monthly downloads as niche
            return popularity < 1000
            
        # If we can't get stats, check if it's a well-known API
        return library_name.lower() not in self.common_apis

    def _find_documentation_url(self, library_name: str) -> Optional[str]:
        """Try to find the documentation URL for a library."""
        try:
            # Try PyPI first
            url = f"https://pypi.org/pypi/{library_name}/json"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('info', {}).get('project_urls', {}).get('Documentation')
                
            # Try GitHub if PyPI fails
            url = f"https://github.com/{library_name}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return url
        except Exception:
            pass
        return None

    def analyze_question(self, question: str) -> List[LibraryInfo]:
        """
        Analyze a question to identify niche/uncommon libraries and APIs.
        
        Args:
            question: The user's question text
            
        Returns:
            List of LibraryInfo objects containing information about identified libraries
        """
        # First try pattern matching
        found_libraries = set()
        patterns = [
            r'using\s+([a-zA-Z0-9_-]+)',
            r'with\s+([a-zA-Z0-9_-]+)',
            r'([a-zA-Z0-9_-]+)\s+library',
            r'([a-zA-Z0-9_-]+)\s+api',
            r'([a-zA-Z0-9_-]+)\s+package',
            r'([a-zA-Z0-9_-]+)\s+module',
            r'import\s+([a-zA-Z0-9_-]+)',
            r'from\s+([a-zA-Z0-9_-]+)\s+import'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, question, re.IGNORECASE)
            for match in matches:
                library_name = match.group(1).lower()
                if library_name not in {'the', 'a', 'an', 'this', 'that', 'these', 'those'}:
                    found_libraries.add(library_name)
        
        # If no libraries found through pattern matching, try LLM
        if not found_libraries:
            llm_detected = self._detect_libraries_with_llm(question)
            found_libraries.update(llm_detected)
        
        # Analyze each found library
        results = []
        for library_name in found_libraries:
            version = self._extract_version(question, library_name)
            is_niche = self._is_niche_library(library_name, version)
            popularity = self._get_pypi_stats(library_name)
            docs_url = self._find_documentation_url(library_name)
            
            results.append(LibraryInfo(
                name=library_name,
                version=version,
                is_niche=is_niche,
                popularity_score=popularity,
                documentation_url=docs_url
            ))
        
        return results

    def get_niche_libraries(self, question: str) -> List[LibraryInfo]:
        """
        Get only the niche/uncommon libraries from a question.
        
        Args:
            question: The user's question text
            
        Returns:
            List of LibraryInfo objects for niche libraries only
        """
        all_libraries = self.analyze_question(question)
        return [lib for lib in all_libraries if lib.is_niche]

# Example usage
if __name__ == "__main__":
    analyzer = LibraryAnalyzer()
    test_question = "How do I use the obscure-lib==1.2.3 library to process data?"
    niche_libs = analyzer.get_niche_libraries(test_question)
    for lib in niche_libs:
        print(f"Found niche library: {lib.name}")
        if lib.version:
            print(f"Version: {lib.version}")
        if lib.documentation_url:
            print(f"Documentation: {lib.documentation_url}")
        print("---") 