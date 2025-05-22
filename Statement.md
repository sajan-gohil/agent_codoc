# Project Contribution Statement

This document outlines the contributions of the team members to the development of the LLM Chat Interface for API Documentation.

## Sajan Gohil: Core Application Logic & Chat Interface

Member A was primarily responsible for establishing the foundational structure of the application and developing the user-facing chat interface. Key contributions include:

-   **Streamlit Application Setup**: Initialized and configured the main Streamlit application file (`app.py`).
-   **User Interface Development**: Designed and implemented the chat UI, including rendering chat messages (user and bot), handling user text input, and managing the overall page layout.
-   **Chat State Management**: Implemented the use of `st.session_state` to manage conversation history, input values, and busy states effectively.
-   **Core Chat Processing**: Developed the primary workflow in `app.py` for taking user input, invoking the chat processing logic, and displaying the generated responses.
-   **Initial ChatSession Structure**: Laid the groundwork for the `ChatSession` class in `agent_codoc/chat_session.py`, including basic LLM initialization and the initial message processing flow.

## Suraj Kumar Samal : RAG System - Document Processing & Vector Store

Member B focused on the core Retrieval Augmented Generation (RAG) system, particularly the ingestion, processing, and storage of documentation. Key contributions include:

-   **RAGDataIO Class Development**: Designed and implemented the `RAGDataIO` class (`agent_codoc/rag_data_io.py`) as the central component for managing documentation data for the RAG system.
-   **Local Document Processing**: Implemented functionality to load, parse, and process local documentation files (Markdown `.md` and plain text `.txt`) from the `./data/` directory.
-   **Text Splitting and Chunking**: Integrated and configured LangChain's text splitters (`MarkdownHeaderTextSplitter`, `MarkdownTextSplitter`, `RecursiveCharacterTextSplitter`) to break down documents into manageable chunks for embedding.
-   **Vector Store Integration**: Set up and managed the `SQLiteVec` vector store, configuring it for storing and retrieving document embeddings.
-   **Embedding Generation**: Configured the use of `OpenAIEmbeddings` (specifically `text-embedding-3-small`) to generate vector representations of the document chunks.
-   **Similarity Search**: Implemented the `search_similar` method to query the vector store and retrieve documents relevant to a user's query.

## Ashwini Mandlay: Database Management & Advanced Documentation Features

Member C was responsible for the backend database systems and the more advanced features related to dynamic documentation ingestion. Key contributions include:

-   **Database Schema Design**: Designed and implemented the SQLite database schema in `agent_codoc/db_setup.py`, creating tables for chat sessions and the RAG documentation metadata.
-   **Database Connection and `sqlite-vec`**: Ensured robust SQLite database connection handling, including `check_same_thread=False` for Streamlit compatibility and the correct loading of the `sqlite-vec` extension.
-   **URL-Based Documentation Ingestion**: Developed the feature to add documentation from external URLs within `RAGDataIO`:
    -   Implemented fetching of content from generic URLs.
    -   Added logic to handle different content types (HTML parsing with BeautifulSoup, direct Markdown/text).
    -   Specifically implemented the detection of GitHub repository URLs and the logic to find, fetch, and process `README.md` files from these repositories (including trying multiple common branch names and README file name casings).
-   **Error Handling for Data Ingestion**: Implemented error handling (e.g., raising `RuntimeError`) in the URL ingestion process to provide feedback to the Streamlit UI upon failure.

## Preetam Chhimpa: LLM Integration, Prompt Engineering & System Refinement

Member D focused on the integration of the Large Language Model, optimizing its performance through prompt engineering, and overall system refinement and debugging. Key contributions include:

-   **LLM Integration**: Integrated the `ChatOpenAI` model (specifically `gpt-4o-mini`) into the `ChatSession` class to generate responses.
-   **Prompt Engineering**: Developed and iteratively refined the `BASE_PROMPT` to effectively guide the LLM in using the retrieved context from documentation and chat history to answer user questions accurately and maintain the desired persona.
-   **Chat History Management**: Implemented chat history tracking within `ChatSession` and the `truncate_chat_history` method to manage context length for the LLM, considering token limits.
-   **Tokenization and Encoding**: Handled token counting and encoding using `tiktoken` to ensure inputs to the LLM are within limits.
-   **System Debugging and Refinement**: Played a crucial role in troubleshooting and resolving various integration issues, such as SQLite UNIQUE constraints, incorrect text splitter arguments, database initialization problems, and ensuring smooth data flow between `app.py`, `ChatSession`, and `RAGDataIO`.
-   **Project Documentation**: Contributed significantly to the creation and refinement of the project's `README.md` file.
-   **User Feedback Improvements**: Enhanced error messages and user feedback mechanisms in the Streamlit application, particularly for documentation addition failures.
