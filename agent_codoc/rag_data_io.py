import sqlite3
import os
import traceback
import tiktoken
import requests
import bs4
import re
from typing import List, Tuple, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SQLiteVec
from langchain.text_splitter import (
    MarkdownHeaderTextSplitter,
    MarkdownTextSplitter,
    RecursiveCharacterTextSplitter,
)
from sqlite_utils_sqlite_vec import sqlite_vec


class RAGDataIO:
    def __init__(self, db_path: str = None, connection=None, cursor=None, top_k: int = 5):
        """Initialize the vector database with SQLite backend."""
        self.db_path = db_path
        self.top_k = top_k
        self.conn = connection
        self.cur = cursor
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.encoding = tiktoken.encoding_for_model(self.embeddings.model)
        self.initialize_database()

    def initialize_database(self) -> None:
        """Connect to SQLite database. Create a new database if it doesn't exist."""
        if self.conn is None:
            if self.db_path is None:
                self.db_path = ":memory:"
            self.conn = sqlite3.connect(self.db_path)
        self.documentation_store = SQLiteVec(table="rag_documentation_database",
                                      embedding=self.embeddings,
                                      connection=self.conn)
        self.qa_chat_store = SQLiteVec(table="rag_qa_database",
                                      embedding=self.embeddings,
                                      connection=self.conn)
        self.initialize_rag_data()

    def initialize_rag_data(self, data_path: str = "./data/") -> None:
        """Check if the embedding table is populated. If not, add data from documents."""
        try:
            # Get list of all document paths that have been processed
            processed_docs = set()
            try:
                self.cur.execute("SELECT metadata FROM rag_documentation_database")
                for row in self.cur.fetchall():
                    if row[0]:
                        metadata = eval(row[0])  # Safely convert string to dict
                        if 'source' in metadata:
                            processed_docs.add(metadata['source'])
            except sqlite3.OperationalError as e:
                # Table might not exist yet
                print("Exception in initializing database:", e)
                traceback.print_exc()

            # Process only new documents
            try:
                for doc in os.listdir(data_path):
                    doc_path = os.path.join(data_path, doc)
                    if doc_path in processed_docs:
                        continue
                    
                    if doc.endswith(".md"):
                        self.add_markdown_document(doc_path=doc_path)
                    elif doc.endswith(".txt"):
                        self.add_text_document(doc_path=doc_path)
                    elif doc.endswith(".pdf"):
                        self.add_pdf_document(doc_path=doc_path)
            except Exception as e:
                print(f"Error processing documents: {e}")
                traceback.print_exc()
            
        except Exception as e:
            print(f"Error initializing documents to database: {e}")
            traceback.print_exc()

    def add_markdown_document(self,
                              doc_path: Optional[str] = None,
                              text: Optional[str] = None) -> None:
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
            ("#####", "Header 5"),
            ("######", "Header 6"),
        ]
        if doc_path is not None:
            with open(doc_path, 'r') as f:
                text = f.read()
        documents = MarkdownHeaderTextSplitter(headers_to_split_on).split_text(text)
        texts, metadatas = [], []
        for document in documents:
            # Check number of tokens of text
            doc_text = document.page_content
            num_tokens = len(self.encoding.encode(doc_text))
            if num_tokens > 8192:
                # Split the text into smaller chunks
                text_chunks = MarkdownTextSplitter(chunk_size=4096).split_text(doc_text)
                for text_chunk in text_chunks:
                    text_chunk = "\n".join(document.metadata.values()) + "\n" + text_chunk
                    texts.append(text_chunk)
                    metadatas.append(document.metadata)
            else:
                doc_text = "\n".join(document.metadata.values()) + "\n" + doc_text
                texts.append(doc_text)
                metadatas.append(document.metadata)
        self.add_documents(texts, metadatas)

    def add_text_document(self,
                          doc_path: Optional[str] = None,
                          text: Optional[str] = None) -> None:
        if doc_path is not None:
            with open(doc_path, 'r') as f:
                text = f.read()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=4096,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False
        )
        documents = splitter.split_text(text)
        texts = []
        texts = [chunk for chunk in documents]  # Each chunk is a string
        self.add_documents(texts)

    def add_pdf_document(self,
                         doc_path: Optional[str] = None,
                         text: Optional[str] = None) -> None:
        """Add a PDF document's text content to the database."""
        if doc_path is not None:
            try:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                file_content = ""
                for page in pdf_reader.pages:
                    file_content += page.extract_text() + "\n\n\n"
            except Exception as e:
                st.error(f"Failed to read PDF file: {e}")
                st.stop()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=4096,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False
        )
        documents = splitter.split_text(text)
        texts = [chunk for chunk in documents]  # Each chunk is a string
        self.add_documents(texts)

    def add_json_document(self, doc_path):
        raise NotImplementedError()

    def add_url_document(self, url: str) -> None:
        """Fetch a document from a URL and add it to the database.
        If the URL is a GitHub repository, it attempts to find and add the README.md.
        """
        try:
            # Check if the URL is a GitHub repository URL
            github_repo_pattern = r"https?://github\.com/([^/]+)/([^/]+)(?:/(?:tree|blob)/([^/]+))?"
            match = re.match(github_repo_pattern, url)

            if match:
                user, repo, branch = match.groups()
                readme_urls_to_try = []

                if branch:
                    # If a branch is specified in the URL, try that first
                    readme_urls_to_try.append(f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/README.md")
                
                # Add common default branches
                readme_urls_to_try.extend([
                    f"https://raw.githubusercontent.com/{user}/{repo}/main/README.md",
                    f"https://raw.githubusercontent.com/{user}/{repo}/master/README.md",
                    f"https://raw.githubusercontent.com/{user}/{repo}/master/Readme.md",
                    f"https://raw.githubusercontent.com/{user}/{repo}/main/Readme.md",
                    f"https://raw.githubusercontent.com/{user}/{repo}/main/readme.md",
                    f"https://raw.githubusercontent.com/{user}/{repo}/master/readme.md"
                ])

                for readme_url in readme_urls_to_try:
                    try:
                        print(f"Attempting to fetch README from: {readme_url}")
                        response = requests.get(readme_url)
                        if response.status_code == 200:
                            content_type = response.headers.get('Content-Type', '')
                            if 'text/plain' in content_type or readme_url.endswith('.md'): # raw.githubusercontent serves md as text/plain
                                print(f"Successfully fetched README.md from {readme_url}")
                                self.add_markdown_document(text=response.text)
                                return # Successfully processed README, so exit
                            else:
                                print(f"README found at {readme_url} but content type is not plain text or markdown: {content_type}")
                        elif response.status_code == 404:
                            print(f"README.md not found at {readme_url} (404)")
                        else:
                            print(f"Failed to fetch README.md from {readme_url}. Status: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        print(f"Error fetching README from {readme_url}: {e}")
                        # Continue to try other README URLs or fallback
                
                # If README processing failed or wasn't applicable, inform and proceed to generic handling (optional)
                print(f"Could not find or process a README.md for GitHub URL {url}. Attempting generic URL processing.")

            # Fallback to generic URL processing if not a GitHub repo or README not found/processed
            response = requests.get(url)
            response.raise_for_status() # Will raise an HTTPError for bad responses (4XX or 5XX)
            content_type = response.headers.get('Content-Type', '')
            if url.endswith('.md') or 'markdown' in content_type:
                # Save to temp file and reuse markdown logic
                self.add_markdown_document(text=response.text)
            elif url.endswith('.txt') or 'text/plain' in content_type:
                self.add_text_document(text=response.text)
            else:
                # For other types (e.g., HTML), extract visible text from the webpage
                soup = bs4.BeautifulSoup(response.text, "html.parser")
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text(separator="\n")
                # Clean up the text
                lines = [line.strip() for line in text.splitlines()]
                text = "\n".join(line for line in lines if line)
                self.add_text_document(text=text)
                
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch document from URL: {url}\nError: {e}")
            raise RuntimeError(
                f"Failed to fetch document from URL: {url}. Please check the URL and your network connection."
            ) from e
        except Exception as e:
            print(f"Failed to add document from URL: {url}\nError: {e}")
            # traceback.print_exc() # Optionally, uncomment for more detailed logs in terminal
            raise RuntimeError(
                f"Failed to process or add document content from URL: {url}. The document format might be unsupported or corrupted."
            ) from e

    def add_documents(self, texts: List[str], metadatas: dict = None):
        """Add a new document and its embedding to the database."""
        # Check for duplicates before adding
        for text_idx, text in enumerate(texts):
            # Check if exact text already exists
            self.cur.execute("SELECT rowid FROM rag_documentation_database WHERE text = ?", (text,))
            if self.cur.fetchone() is not None:
                print(f"Skipping duplicate text chunk")
                continue
            self.documentation_store.add_texts([text], metadatas)

    def search_similar(self, query: str):
        """Search for the most similar documents to the query."""
        results = self.documentation_store.similarity_search_with_score(query, k=self.top_k)
        qa_results = self.qa_chat_store.similarity_search_with_score(
            query, k=self.top_k)
        return results, qa_results

    # def _clear_database(self):
    #     """Clear all documents from the database."""
    #     with sqlite3.connect(self.db_path) as conn:
    #         conn.execute("DELETE FROM documents")
    #         conn.commit()