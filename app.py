import streamlit as st
import time
import markdown
import re
import tiktoken
from dotenv import load_dotenv
from agent_codoc.chat_session import ChatSession
from agent_codoc.util_data.code_languages import CODE_LANGUAGES

load_dotenv()


# Streamlit app

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
        time.sleep(0.05)
        yield i+" "


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
                part = markdown.markdown(part).replace("\n", "<br>").replace(
                    "  ", "&nbsp;&nbsp;").replace(
                        "\t", "&nbsp;&nbsp;&nbsp;&nbsp;").replace(
                            "<li><br>",
                            "<li>").replace('<br><br>', '<br>')
            parts.append((part, "text", None))
    return parts

def display_message_parts(parts: list[tuple[str, str, str]], display_html=False, stream=False):
    for part, part_type, part_lang in parts:
        if part_type == "code":
            time.sleep(0.05)  # Sleep to make display less jarring
            st.code(part, language=part_lang)
            time.sleep(0.05)
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
    print("Creating messages")
    st.session_state['messages'] = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = ChatSession()

if "input_value" not in st.session_state:
    st.session_state["input_value"] = ""
    # st.session_state["input"] = ""

# Flag to indicate if the response is being generated
if "is_busy" not in st.session_state:
    st.session_state["is_busy"] = False

# print("m=", st.session_state.messages)
st.title("LLM Chat Interface")
st.write("**Chat History**")
st.divider()

# Markdown doesn't preserve multiple spaces (example: code blocks without backticks passed by user)
# We can't use streaming response here as it streams everything again with user interaction
for message in st.session_state.messages:
    st.divider()
    # print(message["content"])
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
    bot_response, context_docs, qa_context_docs = st.session_state.chat_session.process_message(user_message)

    # Add some context with the response if there is code in the response
    if bot_response.count("```") > 1:
        bot_response += "\n" + "="*30 + "\n\n**Some relevant snippets from the documentation which might help:**\n"
        for doc_index, doc in enumerate(context_docs[:3], 1):
            bot_response += "-" * 30 + "\n**Snippet " + str(doc_index) + ":**\n"
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
