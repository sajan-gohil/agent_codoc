from typing import Optional, List, Dict
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool, tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_tavily import TavilySearch
from langchain.schema import SystemMessage
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import re
import json

load_dotenv()


class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Search query for finding the library/API documentation for specific functionality.")


class DocSearchAgent:
    def __init__(self, model_name="gpt-4o-mini",
                 openai_api_key: Optional[str] = None,
                 tavily_api_key: Optional[str] = None):
        """
        Initialize the documentation search agent.
        
        Args:
            model_name: OpenAI model to use to formulate search query
            openai_api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY in environment.
            tavily_api_key: Tavily API key. If not provided, will look for TAVILY_API_KEY in environment.
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.tavily_api_key = tavily_api_key or os.getenv("TAVILY_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        if not self.tavily_api_key:
            raise ValueError("Tavily API key is required")
            
        self.llm = ChatOpenAI(model=model_name, max_tokens=100, temperature=0)
        self.search_agent = TavilySearch(
            api_key=self.tavily_api_key,
            max_results=1,
            include_answer=False,
            include_raw_content=False
        )
    
    def get_search_query(self, text):
        # Create the system message
        system_message = SystemMessage(content="""You are an AI assistant that specializes in finding documentation URLs.
        You will be given some query and the name of a library with a specific version if needed.
        Formulate a search query which will get the best search results for whatever functionality the library might be needed for.
        1. Use the search tool to find relevant web pages or github repos
        2. Include both GitHub repository URLs and documentation web pages
        3. Give only the search query which should bring the documentation web page results when pasted verbatim in the search bar.
        """)
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            system_message,
            ("human", "{input}"),
        ])
        structured_llm = self.llm.with_structured_output(SearchQuery)
        search_query = structured_llm.invoke(prompt.format_messages(input=text))
        print("search_query = ", search_query.search_query)
        return search_query.search_query
    
    def search_documentation(self, question: str, library_reference: str) -> List[str]:
        """
        Search for documentation URLs based on the given query.
        
        Args:
            query: The search query about a library or functionality
            
        Returns:
            List[str]: A list of URLs to documentation pages or GitHub repositories
        """
        try:
            search_query = self.get_search_query(
                "Question: {question} | Library info: {library_reference}".format(
                    question=question, library_reference=library_reference))
            search_results = self.search_agent.invoke({"query": search_query})
            # Parse the response as JSON array of URLs
            # if not isinstance(urls, dict):
            #     return []
            # Filter and validate URLs
            valid_urls = []
            for result in search_results.get("results"):
                url = result.get("url")
                # Check if it's a GitHub URL or a web page
                if re.match(r'https?://github\.com/[^/]+/[^/]+', url) or \
                   re.match(r'https?://[^/]+', url):
                    valid_urls.append(url)
            return valid_urls

        except Exception as e:
            print(f"Error searching documentation: {str(e)}")
            return []

# Example usage
if __name__ == "__main__":
    # Initialize the agent
    agent = DocSearchAgent()
    
    # Example query
    query = "Python puzzle library how to use"
    urls = agent.search_documentation(query, "puzzle")
    print("Found documentation URLs:")
    for url in urls:
        print(f"- {url}") 