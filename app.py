"""Streamlit app"""
import streamlit as st
import time
import markdown
import re
import tiktoken
from dotenv import load_dotenv
from agent_codoc.chat_session import ChatSession
from agent_codoc.util_data.code_languages import CODE_LANGUAGES
from agent_codoc.workflow_graph import create_workflow_graph, AgentState
import os
from openai import OpenAI
from openai.types.chat import ChatCompletion
import PyPDF2

load_dotenv()

# Available OpenAI models
OPENAI_MODELS = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo-preview",
    "o3-mini",
    "o4-mini"
]

def validate_api_key(api_key: str) -> bool:
    """Test if the provided API key is valid by making a simple request."""
    try:
        client = OpenAI(api_key=api_key)
        # Make a minimal request to test the key
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        return isinstance(response, ChatCompletion)
    except Exception as e:
        st.error(f"Invalid API key: {str(e)}")
        return False

def add_message(user_input, bot_response):
    """Add a message to the chat history"""
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "bot", "content": bot_response})


def submit():
    """Used to change state of input bar when send is pressed"""
    st.session_state.input_value = st.session_state.input
    st.session_state.input = ''


def generate_stream(text: str):
    for i in text.split(" "):
        time.sleep(0.03)
        yield i + " "


def postprocess_string(text: str) -> str:
    replacements = {
        "\n": "<br>",
        "  ": "&nbsp;&nbsp;",
        "\t": "&nbsp;&nbsp;&nbsp;&nbsp;",
        "<li><br>": "<li>",
        "<br><br>": "<br>",
        "<h1>": "<h3>",
        "</h1>": "</h3>",
        "<h2>": "<h3>",
        "</h2>": "</h3>",
        "<code>": "",
        "</code>": "",
        "<pre>": "",
        "</pre>": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def format_display_message(text: str, get_html=False) -> list[tuple[str, str, str]]:
    """Process input text to a  format that streamlit can display as markdown or code"""
    # Split the text into code and text parts
    text = re.split(r"(```\w*)", text, flags=re.MULTILINE)
    parts = []
    start = False
    current_lang = None
    # Simply doing based on the index of the code block requires lot of other checks
    for part in text:
        # Check if the part is a code block, add as code if it is
        if part.startswith("```") and not start:
            start = True
            current_lang = part[3:] if part[3:] in CODE_LANGUAGES else None
            continue
        elif part.startswith("```") and start:
            start = False
            current_lang = None
            continue
        if start:
            parts.append((part, "code", current_lang))
        else:
            if get_html:
                # Check if a table exists in the text. If so, keep it as is
                sub_parts = []
                tables_exist = False
                if len(re.findall(r'\|\n *\|', part, flags=re.MULTILINE)) > 1:
                    tables_exist = True
                if not tables_exist:
                    sub_parts = [part]
                else:
                    running_part = ""
                    is_table = False
                    # Check start/end of every line to determine if it is a table
                    for line in part.split("\n"):
                        if line.strip().startswith("|") and line.strip(
                        ).endswith("|") and is_table:
                            running_part += line.strip() + "\n"
                        elif line.strip().startswith("|") and line.strip(
                        ).endswith("|") and not is_table:
                            is_table = True
                            sub_parts.append(running_part)
                            running_part = "\n" + line.strip() + "\n"
                        elif ((not line.strip().startswith(
                                "|"
                        )) or (not line.strip().endswith("|"))) and is_table:
                            is_table = False
                            sub_parts.append(running_part)
                            running_part = "\n" + line + "\n"
                        else:
                            running_part += line + "\n"
                    if running_part:
                        sub_parts.append(running_part)

                # Segregate parts with table and without table
                for sub_part in sub_parts:
                    if len(sub_part) == 0:
                        parts.append(("<br>", "text", None))
                        continue
                    if len(sub_part.strip())>0 and sub_part.strip()[0] == "|" and sub_part.strip(
                    )[-1] == "|":
                        parts.append(("\n"+sub_part, "markdown", None))
                    else:
                        # TODO: Change to regex based substitution
                        sub_part = postprocess_string(markdown.markdown(sub_part))
                        parts.append((sub_part, "text", None))
            else:
                parts.append((part, "text", None))
    return parts


def display_message_parts(parts: list[tuple[str, str, str]], display_html=False, stream=False):
    for part, part_type, part_lang in parts:
        if part_type == "code":
            time.sleep(0.05)  # Sleep to make display less jarring
            st.code(part, language=part_lang)
            time.sleep(0.05)
        elif part_type == "markdown":
            st.markdown(part)#, unsafe_allow_html=True)
        else:
            if display_html:
                st.html(part)
            else:
                if stream:
                    st.write_stream(generate_stream(part))
                else:
                    st.markdown(part)


# Chat interface
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = ChatSession()

if "agent_graph" not in st.session_state:
    st.session_state.agent_graph = create_workflow_graph(
        chat_session=st.session_state.chat_session,
        rag_data_io=st.session_state.chat_session.rag_data_io
    )

if "input_value" not in st.session_state:
    st.session_state["input_value"] = ""
    # st.session_state["input"] = ""

# Flag to indicate if the response is being generated
if "is_busy" not in st.session_state:
    st.session_state["is_busy"] = False

st.title("LLM Chat Interface")

# Create sidebar for model selection and API key
with st.sidebar:
    st.write("### Settings")
    # Initialize session state variables if they don't exist
    if "current_model" not in st.session_state:
        st.session_state.current_model = "gpt-4o-mini"
    if "current_api_key" not in st.session_state:
        st.session_state.current_api_key = None

    # Add API key input
    api_key = st.text_input(
        "OpenAI API Key (Not necessary for current model)",
        type="password",
        help="Enter your OpenAI API key. Required when changing models.",
        key="api_key_input"
    )

    # Add model selection dropdown
    selected_model = st.selectbox(
        "Select Model",
        options=OPENAI_MODELS,
        index=OPENAI_MODELS.index(st.session_state.current_model),
        key="model_selector"
    )

    # Handle API key and model changes
    if api_key:
        if validate_api_key(api_key):
            os.environ["OPENAI_API_KEY"] = api_key
            if st.session_state.current_api_key != api_key:
                st.session_state.current_api_key = api_key
                st.success("API key validated and updated successfully")
        else:
            st.error("Invalid API key")
            # st.stop()

    # Handle model change
    if selected_model != st.session_state.current_model:
        if not api_key:
            st.error("Please provide an OpenAI API key to change the model")
            # st.stop()
        else:
            if validate_api_key(api_key):
                st.session_state.chat_session.change_model(selected_model)
                st.session_state.current_model = selected_model
                st.success(f"Model changed to {selected_model}")
            else:
                st.error("Invalid API key")
                st.session_state.current_model = st.session_state.current_model
                # st.stop()

    st.divider()
    st.write("### Add New Documentation from URL")
    doc_url = st.text_input("Enter documentation or github URL:", key="doc_url_input")
    if st.button("Add Documentation from URL"):
        if doc_url:
            with st.spinner("Adding document..."):
                try:
                    st.session_state.chat_session.rag_data_io.add_url_document(doc_url)
                    st.success("Document added successfully from URL!")
                except RuntimeError as e:
                    st.error(f"Failed to add document: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter a valid URL.")

    st.divider()
    st.write("### Add New Documentation from File")
    uploaded_file = st.file_uploader("Upload documentation file",
                                     type=['txt', 'md', 'pdf'],
                                     key="file_uploader")

if uploaded_file is not None:
    # Read file content
    file_content = uploaded_file.read()
    
    # For PDF files, we need to convert to text
    if uploaded_file.type == "application/pdf":
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            file_content = ""
            for page in pdf_reader.pages:
                file_content += page.extract_text() + "\n\n\n"
        except Exception as e:
            st.error(f"Failed to read PDF file: {e}")
            st.stop()
    else:
        # For text and markdown files
        file_content = file_content.decode('utf-8')
    
    # Count tokens
    encoding = tiktoken.encoding_for_model("text-embedding-3-small")
    num_tokens = len(encoding.encode(file_content))
    
    if num_tokens > 16000:
        st.error(f"File is too large ({num_tokens} tokens). Maximum allowed is 16000 tokens.")
    else:
        if st.button("Add File to Documentation"):
            with st.spinner("Adding document..."):
                try:
                    # Check if exact content already exists
                    if uploaded_file.type == "application/pdf":
                        st.session_state.chat_session.rag_data_io.add_pdf_document(file_content)
                    elif uploaded_file.name.endswith('.md'):
                        st.session_state.chat_session.rag_data_io.add_markdown_document_from_text(file_content)
                    else:
                        st.session_state.chat_session.rag_data_io.add_text_document_from_text(file_content)
                    st.success("Document added successfully!")
                except Exception as e:
                    st.error(f"Failed to add document: {e}")

st.write("## **Chat History**")
st.divider()

# Markdown doesn't preserve multiple spaces (example: code blocks without backticks passed by user)
# We can't use streaming response here as it streams everything again with user interaction
for message in st.session_state.messages:
    st.divider()
    if message["role"] == "user":
        message_parts = format_display_message(message['content'], get_html=True)
        with st.chat_message("user"):
            display_message_parts(message_parts, display_html=True)
    elif message["role"] == "bot":
        message_parts = format_display_message(message['content'], get_html=True)
        with st.chat_message("assistant"):
            display_message_parts(message_parts, display_html=True)

st.divider()

if st.session_state["is_busy"]:
    st.chat_input("You: ", key="input", disabled=True)
else:
    st.chat_input("You: ", key="input")
    user_input = st.session_state["input"]
    # Assert user input is smaller than 4k tokens
    if user_input and user_input.strip() != "":
        user_input = user_input.encode("utf-8").decode("utf-8")
        if len(tiktoken.encoding_for_model("gpt-4o-mini").encode(
                user_input)) > 4000:
            st.error("Input too long. Please keep it under 4000 tokens.")
            user_input = ""
            st.stop()
        # Append user input immediately to chat history
        st.session_state.messages.append({
            "role":
            "user",
            "content":
            user_input
        })
        # Reset the input field for the next message
        st.session_state["input_value"] = ""
        st.session_state["is_busy"] = True
        with st.chat_message("user"):
            display_message_parts(format_display_message(user_input), display_html=True)
        # Rerun the app to update the display with the user's message
        # Show a spinner to indicate that the response is being generated
        st.rerun()

# After rerun, generate the response
if st.session_state["is_busy"] and len(st.session_state.messages
       ) > 0 and st.session_state.messages[-1]["role"] == "user":
    user_message = st.session_state.messages[-1]["content"]
    with st.spinner("Fetching Info..."):
        # (bot_response, context_docs, qa_context_docs
        #  ) = st.session_state.chat_session.process_message(user_message)
        agent_state = st.session_state.agent_graph.invoke({"question": user_message})
        bot_response = agent_state["response"]
        context_docs, qa_context_docs = agent_state["context_docs"], agent_state["qa_context_docs"]
    
    # with st.spinner("Evaluating code..."):
    #     code_eval = st.session_state.chat_session.evaluate_code(bot_response, user_message)

    # Add some context with the response if there is code in the response
    if bot_response.count("```") > 1:
        bot_response += "\n\n" + "= "*30 + "\n\n## **Some relevant snippets from the documentation which might help:**\n"
        for doc_index, doc in enumerate(context_docs[:1], 1):
            bot_response += "\n\n" + "- " * 30 + "\n\n**Snippet " + str(doc_index) + ":**\n"
            bot_response += f"\n{doc}"

    st.session_state.messages.append({
        "role":
        "bot",
        "content":
        bot_response
    })
    st.session_state["is_busy"] = False
    # We can stream bot response here but user message before this requires proper formatting
    with st.chat_message("assistant"):
        display_message_parts(format_display_message(bot_response),
                              display_html=False,
                              stream=True)
    # Rerun again to display the bot's response
    st.rerun()
