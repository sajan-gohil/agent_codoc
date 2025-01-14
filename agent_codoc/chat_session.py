import datetime
import uuid
import tiktoken
from agent_codoc.db_setup import initialize_db
from agent_codoc.rag_data_io import RAGDataIO
from langchain.schema.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

BASE_PROMPT = """
You are a customer support specialist for Crustdata's APIs. Your responses should be clear, accurate, and focused on helping users understand and work with the APIs.

Context from documentation:
{context}

Relevant questions and answers from previous chats:
{relevant_qa_context}

Chat history:
{chat_history}

Latest user question:
{question}

Please provide a helpful response that:
1. Directly addresses the user's question
2. Uses the relevant documentation context
3. Includes code examples only when appropriate. Eg: when the user asks for something specific to do with the API.
4. Is concise and clear
5. Maintains a professional and courteous tone

If any question asked seems like it is not related to crustdata API, please mention that the question is not related to the API and ask the user to provide more context or rephrase the question.
Your response:
"""


class ChatSession:

    def __init__(self):
        self.conn, self.cur = initialize_db()
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.load_db()
        self.rag_data_io = RAGDataIO(connection=self.conn,
                                     cursor=self.cur,
                                     top_k=10)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            max_retries=2
        )
        self.chat_history = []
        self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")

    def load_db(self):
        # Start a new session
        self.cur.execute(
            "INSERT INTO sessions (session_id, start_time) VALUES (?, ?)",
            (self.session_id, self.start_time))
        self.conn.commit()

    def add_message(self, message):
        self.cur.execute(
            "INSERT INTO chats (session_id, message, timestamp) VALUES (?, ?, ?)",
            (self.session_id, message,
             datetime.datetime.now().timestamp()))

        self.conn.commit()

    def get_chat_response(self,
                    question: str,
                    context: str = "",
                    relevant_qa_context: str = "",
                    chat_history: list = []):
        PROMPT = BASE_PROMPT  # ChatPromptTemplate.from_template(BASE_PROMPT)
        messages = PROMPT.format(
            context=context,
            relevant_qa_context=relevant_qa_context,
            chat_history=chat_history,
            question=question
        )
        response = self.llm.invoke(messages)
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=response.content))
        return response.content

    def get_message_context(self, message):
        # Get context from documentation
        context = self.rag_data_io.search_similar(message)
        # print(type(context))
        # Combine context texts till 8k tokens
        context_text = ""
        for doc in context:
            context_text += doc[0].page_content + "\n"
            if len(self.encoding.encode(context_text)) > 8000:
                break
        return context_text

    def process_message(self, message):
        # self.add_message(message)
        context = self.get_message_context(message)
        response = self.get_chat_response(
            question=message,
            context=context,
            relevant_qa_context="",
            chat_history=self.chat_history
        )
        self.add_message(f"User: {message} \n\n Response: {response}")
        return response

    def add_data(self, data):
        self.cur.execute("INSERT INTO rag_database (data) VALUES (?)",
                         (data, ))
        self.conn.commit()
