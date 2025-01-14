import sqlite3
import os
import traceback
import tiktoken
from typing import List, Tuple
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SQLiteVec
from langchain_text_splitters import (MarkdownHeaderTextSplitter,
                                      MarkdownTextSplitter,
                                      RecursiveCharacterTextSplitter,
                                      )


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
        num_docs = self.cur.execute(
            "SELECT COUNT(*) FROM rag_documentation_database").fetchone()[0]
        print("NUM DOCS = ", num_docs)
        if num_docs == 0:
            try:
                for doc in os.listdir(data_path):
                    if doc.endswith(".md"):
                        self.add_markdown_document(data_path + doc)
                    elif doc.endswith(".txt"):
                        self.add_text_document(data_path + doc)
            except Exception as e:
                print(f"Error initializing documents to database: {e}")
                traceback.print_exc()

    def add_markdown_document(self, doc_path) -> None:
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
            ("#####", "Header 5"),
            ("######", "Header 6"),
        ]
        with open(doc_path, 'r') as f:
            text = f.read()
            documents = MarkdownHeaderTextSplitter(
                headers_to_split_on).split_text(text)
            texts = []
            metadatas = []
            for document in documents:
                # Check number of tokens of text
                text = document.page_content
                num_tokens = len(self.encoding.encode(text))
                if num_tokens > 8192:
                    # Split the text into smaller chunks
                    text_chunks = MarkdownTextSplitter().split_text(
                        text, chunk_size=4096)
                    for text_chunk in text_chunks:
                        text_chunk = "\n".join(
                            document.metadata.values()) + "\n" + text_chunk
                        texts.append(text_chunk)
                        metadatas.append(document.metadata)
                else:
                    text = "\n".join(document.metadata.values()) + "\n" + text
                    texts.append(text)
                    metadatas.append(document.metadata)
            self.add_documents(texts, metadatas)

    def add_text_document(self, doc_path) -> None:
        with open(doc_path, 'r') as f:
            text = f.read()
            documents = RecursiveCharacterTextSplitter().split_text(
                text, chunk_size=4096, chunk_overlap=50)
            texts = []
            for document in documents:
                texts.append(document.page_content)
            self.add_documents(texts)

    def add_pdf_document(self, doc_path):
        pass

    def add_json_document(self, doc_path):
        pass

    def add_documents(self, texts: List[str], metadatas: dict = None):
        """Add a new document and its embedding to the database."""
        self.documentation_store.add_texts(texts, metadatas)

    def search_similar(self, query: str):
        """Search for the most similar documents to the query."""
        results = self.documentation_store.similarity_search_with_score(query, k=self.top_k)
        return results

    # def _clear_database(self):
    #     """Clear all documents from the database."""
    #     with sqlite3.connect(self.db_path) as conn:
    #         conn.execute("DELETE FROM documents")
    #         conn.commit()
