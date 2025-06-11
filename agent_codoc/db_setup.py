import sqlite3
import sqlite_vec

def initialize_db():
    """Initialize database connection and create necessary tables."""
    try:
        # Initialize database connection
        conn = sqlite3.connect('chat_sessions.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Enable and load SQLite vector extension
        try:
            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
        finally:
            conn.enable_load_extension(False)

        # Create tables if they don't exist
        tables = [
            '''CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                start_time TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS chats (
                session_id TEXT,
                message TEXT,
                timestamp unixepoch DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES sessions(session_id)
            )''',
            '''CREATE TABLE IF NOT EXISTS rag_documentation_database (
                rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                timestamp unixepoch DEFAULT CURRENT_TIMESTAMP,
                metadata BLOB,
                text_embedding BLOB
            )''',
            '''CREATE TABLE IF NOT EXISTS rag_qa_database (
                rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                timestamp unixepoch DEFAULT CURRENT_TIMESTAMP,
                metadata BLOB,
                text_embedding BLOB
            )'''
        ]

        for table_sql in tables:
            cur.execute(table_sql)
        
        conn.commit()
        return conn, cur

    except sqlite3.Error as e:
        print(f"SQLite error during initialization: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during database initialization: {e}")
        raise

if __name__ == '__main__':
    from langchain_community.vectorstores import SQLiteVec
    from langchain_openai import OpenAIEmbeddings
    import dotenv
    dotenv.load_dotenv()

    initialize_db()
    # Check if sqlite_vec is loaded and langchain SQLiteVec is working
    conn, cur = initialize_db()
    # check SQLiteVec
    rag = SQLiteVec(
        table='rag_documentation_database',
        connection=conn,
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"))


    rag.add_texts(texts=["Hello, world2!", "This is a test2."])
    res = rag.similarity_search_with_score("Hello, world!", top_k=2)
    print(res)
