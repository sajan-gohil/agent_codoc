# LLM Chat Interface for API Documentation

## Overview

Navigating the often vast and intricate documentation for APIs that serve large datasets—such as those from OpenStreetMap, public government data portals, or extensive scientific data repositories—can be a significant challenge. This project introduces a Streamlit-based LLM (Large Language Model) chat interface specifically designed to simplify this process. By leveraging a Retrieval Augmented Generation (RAG) approach, the application provides users with an intuitive way to ask questions and receive contextually relevant answers directly from the API documentation. Users can interactively explore API functionalities, understand complex endpoints, and clarify usage details for even the most comprehensive data services. The application further streamlines documentation management by allowing new API documents to be added dynamically from URLs, including intelligent parsing of `README.md` files from GitHub repositories, making it easier to keep the knowledge base current.

## Live Demo
The LLM chat Interface app can be directly accessed at https://agentcodoc.streamlit.app/
## Features

- **Interactive Chat Interface**: Users can ask questions in natural language about the API.
- **Retrieval Augmented Generation (RAG)**:
    - Utilizes a vector database (SQLite with `SQLiteVec`) to store and search API documentation.
    - Embeddings are generated using OpenAI's `text-embedding-3-small` model.
    - Processes and chunks Markdown and text documents for efficient retrieval.
- **Dynamic Documentation Ingestion**:
    - Add API documentation from local files (`.md`, `.txt`) during initialization.
    - Add documentation from URLs.
    - Automatically detects GitHub repository URLs and attempts to parse and ingest their `README.md` file.
- **Chat History**: Stores and displays the conversation history for the current session.
- **Contextual Responses**: The LLM (powered by `gpt-4o-mini`) uses chat history, relevant Q&A from previous chats (if implemented), and documentation snippets to formulate answers.
- **Streamlit UI**: A user-friendly web interface built with Streamlit.

## Project Structure

```
.
├── agent_codoc/            # Core logic for the agent and RAG system
│   ├── __init__.py
│   ├── chat_session.py     # Manages chat sessions, LLM interaction, and RAG querying
│   ├── db_setup.py         # Handles SQLite database initialization and schema
│   ├── rag_data_io.py      # Manages reading, processing, and storing documentation for RAG
│   └── util_data/          # Utility data (e.g., code languages for formatting)
│       └── code_languages.py
├── data/                   # Directory for storing local API documentation files
│   ├── crustdata_detailed_examples.md
│   ├── docs_crustdata.md
│   └── ... (other .md or .txt files)
├── .git/                   # Git repository files
├── .gitignore              # Specifies intentionally untracked files that Git should ignore
├── app.py                  # Main Streamlit application file
├── chat_sessions.db        # SQLite database for chat sessions and RAG data
├── poetry.lock             # Poetry dependency lock file
├── pyproject.toml          # Poetry project configuration and dependencies
└── README.md               # This file
```

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Install Dependencies:**
    This project uses Poetry for dependency management.
    ```bash
    poetry install
    ```
    If you don't have Poetry, you can install it by following the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

3.  **Set up Environment Variables:**
    The application uses OpenAI models. You'll need an OpenAI API key. Create a `.env` file in the project root and add your API key:
    ```
    OPENAI_API_KEY='your_openai_api_key_here'
    ```

4.  **Prepare Documentation (Optional):**
    Place your API documentation files (Markdown or text) in the `data/` directory. The application will automatically process these on first run if the database is empty.

## Dependencies

Key Python libraries used:

-   `streamlit`: For building the web interface.
-   `langchain`, `langchain-openai`, `langchain-community`: For LLM integration, RAG, and text processing.
-   `tiktoken`: For token counting.
-   `requests`: For fetching documents from URLs.
-   `beautifulsoup4`: For parsing HTML from URLs.
-   `sqlite-vec`: For SQLite-based vector storage.
-   `poetry`: For dependency management.

Refer to `pyproject.toml` for a full list of dependencies and their versions.

## How to Run

Once dependencies are installed and your `.env` file is set up, run the Streamlit application from the project root directory:

```bash
poetry run streamlit run app.py
```

This will start the Streamlit server, and you can access the application in your web browser (usually at `http://localhost:8501`).

## Usage

1.  **Adding Documentation (Optional):**
    -   The application will attempt to load any `.md` or `.txt` files from the `./data/` directory upon initialization if the documentation store is empty.
    -   Use the "Add Documentation from URL" feature in the UI to add documents from a web link.
        -   If you provide a link to a GitHub repository, it will attempt to find and add the `README.md` file.
        -   Direct links to Markdown or text files are also supported.

2.  **Chatting with the API Assistant:**
    -   Type your questions about the API into the chat input box at the bottom of the page.
    -   The assistant will use the loaded documentation and its LLM capabilities to provide an answer.
    -   The chat history is displayed in the main panel.

## Future Enhancements / TODOs (Example)

-   Implement a more robust Q&A context retrieval from past chats.
-   Support for more document types (e.g., PDF, JSON).
-   User authentication and multi-user session management.
-   More sophisticated error handling and logging.
-   UI/UX improvements.


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
