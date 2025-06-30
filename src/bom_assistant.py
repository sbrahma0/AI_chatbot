import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
from pathlib import Path

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Setup Groq client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

st.set_page_config(page_title="BOM Assistant - Requirement Extraction", layout="wide")
st.title("🧠 BOM Assistant — Interactive Requirement Extraction")

# System prompt for requirement extraction conversation
SYSTEM_PROMPT = """
You are a helpful assistant tasked with understanding and finalizing the Bill of Materials (BOM) requirements for a factory.

You will have a conversation with the user to:
- Identify sites, stations, reference projects, target projects.
- Understand modifications requested.
- Ask clarifying questions if anything is unclear or missing.
- Repeat back a summary of the requirements.
- Confirm when the requirements are final and complete.

Respond concisely and clearly. Only confirm completion when you are sure the user has provided all necessary info.
"""

# Initialize session state variables
if "requirement_chat" not in st.session_state:
    st.session_state.requirement_chat = [{"role": "system", "content": SYSTEM_PROMPT}]

if "requirements_finalized" not in st.session_state:
    st.session_state.requirements_finalized = False

# Display the chat messages
for msg in st.session_state.requirement_chat:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message(msg["role"]).markdown(msg["content"])
# Handle user input for BOM requirements

if not st.session_state.requirements_finalized:
    user_input = st.chat_input("Provide BOM requirements or answer questions:")
    if user_input:
        # Show the user message immediately
        st.chat_message("user").markdown(user_input)

        # Append user message AFTER showing it (for persistence in next reruns)
        st.session_state.requirement_chat.append({"role": "user", "content": user_input})

        # Query the LLM
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.requirement_chat
        )
        assistant_reply = response.choices[0].message.content

        # Append assistant response
        st.session_state.requirement_chat.append({"role": "assistant", "content": assistant_reply})

        # Show assistant reply immediately
        st.chat_message("assistant").markdown(assistant_reply)

        # Confirmation detection
        confirm_phrases = [
            "requirements are final",
            "requirements are complete",
            "I have all the information",
            "confirming the requirements"
        ]
        if any(phrase.lower() in assistant_reply.lower() for phrase in confirm_phrases):
            st.session_state.requirements_finalized = True
            st.success("✅ Requirements finalized! You can now proceed to BOM generation.")

else:
    st.info("Requirements are finalized. Implement BOM generation here.")
    # Here you can call your BOM generation function/module,
    # passing the chat history or parsed final requirements.
