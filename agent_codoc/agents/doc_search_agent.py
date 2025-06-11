from typing import Optional, List, Dict
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.tavily_search import TavilySearchResults
from langchain.schema import SystemMessage
import os
from dotenv import load_dotenv
import re

load_dotenv()

class DocSearchAgent:
    def __init__(self, openai_api_key: Optional[str] = None, tavily_api_key: Optional[str] = None):
        """
        Initialize the documentation search agent.
        
        Args:
            openai_api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY in environment.
            tavily_api_key: Tavily API key. If not provided, will look for TAVILY_API_KEY in environment.
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.tavily_api_key = tavily_api_key or os.getenv("TAVILY_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        if not self.tavily_api_key:
            raise ValueError("Tavily API key is required")
            
        self._setup_agent()
    
    def _setup_agent(self):
        """Set up the LangChain agent with Tavily search tool."""
        # Initialize the LLM
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=self.openai_api_key
        )
        
        # Initialize Tavily search tool
        search = TavilySearchResults(
            api_key=self.tavily_api_key,
            max_results=5
        )
        
        # Create the search tool
        search_tool = Tool(
            name="Documentation Search",
            func=search.run,
            description="""Useful for searching documentation for libraries and specific functionality.
            Input should be a search query about a library or specific functionality you want to find documentation for.
            For example: 'Python requests library POST method documentation' or 'React useState hook documentation'"""
        )
        
        # Create the system message
        system_message = SystemMessage(content="""You are a helpful AI assistant that specializes in finding documentation URLs.
        When given a query about a library or functionality:
        1. Use the search tool to find relevant web pages or github repos
        2. Extract and return ONLY the URLs from the search results
        3. Format the response as a JSON array of URLs
        4. Include both GitHub repository URLs and documentation web pages
        5. Do not include any analysis or explanation
        
        Example response format:
        ["https://github.com/user/repo", "https://docs.example.com/library"]
        
        If no relevant URLs are found, return an empty array: []""")
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            system_message,
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_openai_tools_agent(llm, [search_tool], prompt)
        
        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=[search_tool],
            verbose=True
        )
    
    def search_documentation(self, query: str) -> List[str]:
        """
        Search for documentation URLs based on the given query.
        
        Args:
            query: The search query about a library or functionality
            
        Returns:
            List[str]: A list of URLs to documentation pages or GitHub repositories
        """
        try:
            response = self.agent_executor.invoke({"input": query})
            # Parse the response as JSON array of URLs
            urls = eval(response["output"])  # Safe since we control the output format
            if not isinstance(urls, list):
                return []
            
            # Filter and validate URLs
            valid_urls = []
            for url in urls:
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
    query = "Python requests library POST method documentation"
    urls = agent.search_documentation(query)
    print("Found documentation URLs:")
    for url in urls:
        print(f"- {url}") 