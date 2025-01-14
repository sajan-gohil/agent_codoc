import streamlit as st
import os
import uuid
import sqlite3
from dotenv import load_dotenv
from agent_codoc.chat_session import ChatSession
import markdown
import re

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


def convert_markdown_to_html(text: str) -> list[tuple[str, str]]:
    '''Process input text to a  format that streamlit can display as markdown or code'''
    # Split the text into code and text parts

    text = re.split(r"(```)", text, flags=re.MULTILINE)
    parts = []
    start = False
    # Simply doing based on the index of the code block requires lot of other checks
    for part in text:
        # Check if the part is a code block, add as code if it is
        if part == "```" and not start:
            start = True
            continue
        elif part == "```" and start:
            start = False
            continue
        if start:
            parts.append((part, "code"))
        else:
            part = markdown.markdown(part).replace("\n", "<br>").replace(
                "  ",
                "&nbsp;&nbsp;").replace("\t",
                                        "&nbsp;&nbsp;&nbsp;&nbsp;").replace(
                                            "<li><br>", "<li>")
            parts.append((part, "text"))
    return parts

# Chat interface
if 'messages' not in st.session_state:
    print("Creating messages")
    st.session_state['messages'] = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = ChatSession()

if "input_value" not in st.session_state:
    st.session_state["input_value"] = ""
    st.session_state["input"] = ""


# print("m=", st.session_state.messages)
st.title("LLM Chat Interface")
st.write("**Chat History**")
st.divider()
for message in st.session_state.messages:
    st.divider()
    print(message["content"])
    if message["role"] == "user":
        st.markdown("**You:** \n")
        message_parts = convert_markdown_to_html(message['content'])
        for part, part_type in message_parts:
            if part_type == "code":
                st.code(part)
            else:
                st.html(part)#, unsafe_allow_html=True)
    elif message["role"] == "bot":
        message_parts = convert_markdown_to_html(message['content'])
        st.markdown("**Response:** \n")
        for part, part_type in message_parts:
            if part_type == "code":
                st.code(part)
            else:
                st.html(part)#, unsafe_allow_html=True)
st.divider()

st.text_area("You: ", key="input")
user_input = st.session_state["input_value"]

if st.button("Send", on_click=submit) and user_input.strip() != "":
    # Append user input immediately to chat history
    st.session_state.messages.append({
        "role":
        "user",
        "content":
        user_input
    })

    # Reset the input field for the next message
    st.session_state["input_value"] = ""

    # Rerun the app to update the display with the user's message
    st.rerun()

# After rerun, generate the bot response
if len(st.session_state.messages
       ) > 0 and st.session_state.messages[-1]["role"] == "user":
    user_message = st.session_state.messages[-1]["content"]
    bot_response = st.session_state.chat_session.process_message(user_message)
    st.session_state.messages.append({
        "role":
        "bot",
        "content":
        bot_response
    })

    # Rerun again to display the bot's response
    st.rerun()
