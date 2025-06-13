from typing import List, Dict, Optional, Tuple
import re
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import json
import time
from langchain_openai import ChatOpenAI
from langchain.tools import Tool, tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage


class LibraryInfo(BaseModel):
    name: str
    version: Optional[str] = None
    is_niche: bool = False
    popularity_score: Optional[float] = None
    documentation_url: Optional[str] = None


@tool
def detect_libraries(input: str) -> List[LibraryInfo]:
    """Detects libraries/APIs mentioned in the input and returns their structured metadata."""
    pass  # The model simulates this


system_message = SystemMessage(content="""You are a library detection agent.
Extract any niche or obscure programming libraries, frameworks, or APIs mentioned in the input.
Return a JSON array where each item is an object with the following fields:
- name (string)
- version (string or null)
- is_niche (boolean)
- popularity_score (float or null)
- documentation_url (string or null)

Return only a JSON array of these objects. If none, return [].
Do not include any extra text or explanation.""")


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
        self.llm = ChatOpenAI(model=model_name, max_tokens=500)

    def _detect_libraries_with_llm(self, text: str) -> List[LibraryInfo]:
        """Use LLM to detect libraries in text when pattern matching fails."""
        try:        
            libraries = []
            prompt = ChatPromptTemplate.from_messages([
                system_message,
                ("human", "{input}"),
            ])
            response = self.llm.invoke_with_functions(prompt.format_messages(input=text),
                                                      functions=[detect_libraries])
            if len(response.additional_kwargs.get("tool_calls", [])) > 0:
                tool_call = response.additional_kwargs["tool_calls"][0]
                arguments = tool_call["function"]["arguments"]
                args_dict = json.loads(arguments)
                libraries = [LibraryInfo(**item) for item in args_dict]
            return libraries
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
        
        # If no libraries found through pattern matching, try LLM
        if not found_libraries:
            llm_detected = self._detect_libraries_with_llm(question)
            results.extend(llm_detected)
            
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