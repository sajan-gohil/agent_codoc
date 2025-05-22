"""Streamlit app"""
import streamlit as st
import time
import markdown
import re
import tiktoken
from dotenv import load_dotenv
from agent_codoc.chat_session import ChatSession
from agent_codoc.util_data.code_languages import CODE_LANGUAGES

load_dotenv()

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

if "input_value" not in st.session_state:
    st.session_state["input_value"] = ""
    # st.session_state["input"] = ""

# Flag to indicate if the response is being generated
if "is_busy" not in st.session_state:
    st.session_state["is_busy"] = False

st.title("LLM Chat Interface")

st.write("### Add Documentation from URL")
doc_url = st.text_input("Enter documentation URL (Markdown or Text):", key="doc_url_input")
if st.button("Add Documentation from URL"):
    if doc_url:
        try:
            st.session_state.chat_session.rag_data_io.add_url_document(doc_url)
            st.success("Document added from URL!")
        except Exception as e:
            st.error(f"Failed to add document: {e}")
    else:
        st.warning("Please enter a valid URL.")

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
        (bot_response, context_docs, qa_context_docs
         ) = st.session_state.chat_session.process_message(user_message)

    # Add some context with the response if there is code in the response
    if bot_response.count("```") > 1:
        bot_response += "\n\n" + "= "*30 + "\n\n## **Some relevant snippets from the documentation which might help:**\n"
        for doc_index, doc in enumerate(context_docs[:2], 1):
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
