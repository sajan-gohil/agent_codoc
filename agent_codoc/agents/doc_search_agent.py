from typing import Optional, List
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.tavily_search import TavilySearchResults
from langchain.schema import SystemMessage
import os
from dotenv import load_dotenv

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
        system_message = SystemMessage(content="""You are a helpful AI assistant that specializes in finding and explaining documentation.
        When given a query about a library or functionality:
        1. Use the search tool to find relevant documentation
        2. Analyze the search results to find the most relevant information
        3. Provide a clear, concise explanation with relevant code examples if available
        4. Include links to the official documentation when possible
        5. If the search results don't provide enough information, say so and suggest alternative search terms
        
        Always be accurate and honest about what you find. If you're not sure about something, say so.""")
        
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
    
    def search_documentation(self, query: str) -> str:
        """
        Search for documentation based on the given query.
        
        Args:
            query: The search query about a library or functionality
            
        Returns:
            str: The agent's response with documentation information
        """
        try:
            response = self.agent_executor.invoke({"input": query})
            return response["output"]
        except Exception as e:
            return f"Error searching documentation: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Initialize the agent
    agent = DocSearchAgent()
    
    # Example query
    query = "Python requests library POST method documentation"
    result = agent.search_documentation(query)
    print(result) 