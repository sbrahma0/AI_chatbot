# src/main.py

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime

# Load env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GROQ_API_KEY")

# Groq client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

st.set_page_config(page_title="Groq Chatbot", layout="wide")
st.title("🦙 Groq Chatbot with LLaMA 3")
st.caption("Multi-session support | Powered by LLaMA 3 70B via Groq")

# --- Session storage ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {}  # {session_name: message_history}
    st.session_state.current_session = None

# --- Start a new chat ---
def new_chat():
    name = f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    st.session_state.sessions[name] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state.current_session = name

# --- Sidebar: List of sessions ---
st.sidebar.title("💾 Saved Sessions")
if st.sidebar.button("➕ New Chat"):
    new_chat()

# If there are sessions, show list
if st.session_state.sessions:
    for name in st.session_state.sessions:
        if st.sidebar.button(name):
            st.session_state.current_session = name

# Handle current session
if not st.session_state.current_session:
    new_chat()

current_session = st.session_state.current_session
messages = st.session_state.sessions[current_session]

# --- Display chat history ---
for msg in messages[1:]:  # skip system
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input ---
if prompt := st.chat_input("Ask something..."):
    messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    messages.append({"role": "assistant", "content": reply})
