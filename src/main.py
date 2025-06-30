# src/main.py

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env from current directory (src)
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GROQ_API_KEY")

# Groq client (OpenAI compatible)
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

# Streamlit UI setup
st.set_page_config(page_title="Groq Chatbot", layout="centered")
st.title("🦙 Chat with LLaMA 3 (Groq)")
st.caption("Fast and Free via Groq API")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Display past messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get LLM reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
