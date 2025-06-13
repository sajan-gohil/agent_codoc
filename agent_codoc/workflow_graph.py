from typing import Dict, List, Tuple, TypedDict, Annotated, Sequence, Optional
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain.schema import BaseMessage
from agent_codoc.agents.library_analyzer import LibraryAnalyzer, LibraryInfo
from agent_codoc.agents.doc_search_agent import DocSearchAgent
from agent_codoc.db_setup import initialize_db
from agent_codoc.rag_data_io import RAGDataIO
from agent_codoc.chat_session import ChatSession
import json
import traceback


# Define the state types
class AgentState(TypedDict):
    """The state of the agent workflow"""
    question: str
    niche_libraries: List[LibraryInfo] = None
    doc_urls: List[str] = None
    context: str = None
    qa_context: str = None
    response: str = None
    context_docs: List[str] = None
    qa_context_docs: List[str] = None


def create_workflow_graph(
    chat_session: ChatSession,
    rag_data_io: RAGDataIO,
    library_analyzer: Optional[LibraryAnalyzer]=None,
    doc_search_agent: Optional[DocSearchAgent]=None
) -> StateGraph:
    """Create the workflow graph for the agent system."""
    if library_analyzer is None:
        library_analyzer = LibraryAnalyzer()
    if doc_search_agent is None:
        doc_search_agent = DocSearchAgent()

    def set_state(question: str) -> AgentState:
        agent_state = AgentState(question=question["question"])
        return agent_state

    def analyze_libraries(state: AgentState) -> AgentState:
        """Analyze the question for niche libraries."""
        question = state["question"]
        niche_libs = library_analyzer.analyze_question(question)
        return {"niche_libraries": niche_libs}
    
    def search_documentation(state: AgentState) -> AgentState:
        """Search for documentation URLs for niche libraries."""
        niche_libs = state["niche_libraries"]
        question = state["question"]
        doc_urls = []
        
        for lib in niche_libs:
            if lib.is_niche:
                # Search for documentation URLs
                urls = doc_search_agent.search_documentation(question, f"{lib.name} {lib.version if lib.version else ''}")
                doc_urls.extend(urls)
        
        return {"doc_urls": doc_urls}
    
    def store_documentation(state: AgentState) -> AgentState:
        """Store documentation from URLs in the RAG database."""
        doc_urls = state["doc_urls"]
        
        for url in doc_urls:
            try:
                rag_data_io.add_url_document(url)
            except Exception as e:
                print(f"Error storing documentation from {url}: {e}")
        return {}
    
    def get_rag_context(state: AgentState) -> AgentState:
        """Get context from RAG system."""
        try:
            question = state["question"]
            context_docs, context, qa_context_docs, qa_context = chat_session.get_message_context(question)
            return {
                "context": context,
                "qa_context": qa_context,
                "context_docs": context_docs,
                "qa_context_docs": qa_context_docs
            }
        except:
            traceback.print_exc()
    
    def generate_response(state: AgentState) -> AgentState:
        """Generate response using the chat session."""
        question = state["question"]
        context = state["context"]
        qa_context = state["qa_context"]
        chat_history = chat_session.truncate_chat_history()

        response = chat_session.get_chat_response(
            question=question,
            context=context,
            relevant_qa_context=qa_context,
            chat_history=chat_history
        )
        chat_session.add_message(f"User: {question} \n\n Response: {response}")  # Add to db
        return {"response": response}

    def should_search_docs(state: AgentState) -> str:
        """Determine if we need to search for documentation."""
        niche_libs = state["niche_libraries"]
        return "search_docs" if any(lib.is_niche for lib in niche_libs) else "get_context"
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("set_state", set_state)
    workflow.add_node("analyze_libraries", analyze_libraries)
    workflow.add_node("search_documentation", search_documentation)
    workflow.add_node("store_documentation", store_documentation)
    workflow.add_node("get_context", get_rag_context)
    workflow.add_node("generate_response", generate_response)
    
    # Add edges
    workflow.add_edge("set_state", "analyze_libraries")
    workflow.add_conditional_edges(
        "analyze_libraries",
        should_search_docs,
        {
            "search_docs": "search_documentation",
            "get_context": "get_context"
        }
    )
    workflow.add_edge("search_documentation", "store_documentation")
    workflow.add_edge("store_documentation", "get_context")
    workflow.add_edge("get_context", "generate_response")
    workflow.add_edge("generate_response", END)
    
    # Set entry point
    workflow.set_entry_point("set_state")
    
    return workflow.compile()

def process_message(
    chat_session: ChatSession,
    library_analyzer: LibraryAnalyzer,
    doc_search_agent: DocSearchAgent,
    rag_data_io: RAGDataIO,
    message: str
) -> str:
    """Process a message through the workflow."""
    # Create the workflow
    workflow = create_workflow_graph(
        chat_session=chat_session,
        library_analyzer=library_analyzer,
        doc_search_agent=doc_search_agent,
        rag_data_io=rag_data_io
    )
    
    # Initialize the state
    initial_state = {
        "messages": chat_session.chat_history,
        "question": message,
        "niche_libraries": [],
        "doc_urls": [],
        "context": "",
        "qa_context": "",
        "response": ""
    }
    
    # Run the workflow
    final_state = workflow.invoke(initial_state)
    
    # Add the message and response to chat history
    chat_session.add_message(f"User: {message}\n\nResponse: {final_state['response']}")
    
    return final_state["response"], final_state["context"], final_state["qa_context"]

conn, cur = initialize_db()
graph = create_workflow_graph(
    chat_session=ChatSession(),
    library_analyzer=LibraryAnalyzer(),
    doc_search_agent=DocSearchAgent(),
    rag_data_io=RAGDataIO(connection=conn,
                        cursor=cur,
                        top_k=3)
)

# # Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    # Initialize components
    chat_session = ChatSession()
    library_analyzer = LibraryAnalyzer()
    doc_search_agent = DocSearchAgent()
    rag_data_io = RAGDataIO()

    # Test message
    message = "How do I use the obscure-lib==1.2.3 library to process data?"
    response = process_message(
        chat_session=chat_session,
        library_analyzer=library_analyzer,
        doc_search_agent=doc_search_agent,
        rag_data_io=rag_data_io,
        message=message
    )
    print(f"Response: {response}") 