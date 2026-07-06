import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Page config
st.set_page_config(page_title="AI/ML Tutor", page_icon="🤖")

st.title("🤖 AI/ML Tutor Chatbot")

# Sidebar
st.sidebar.title("⚙️ Settings")
st.sidebar.write("This chatbot only answers AI/ML related questions.")

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# System prompt (domain restriction)
system_prompt = """
You are an AI/ML Tutor.

Rules:
- Only answer AI, ML, Deep Learning, NLP, Data Science, Python for AI.
- If question is outside topic, reply: "I only answer AI/ML related questions."
- Keep answers simple and beginner friendly with examples.
"""

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask AI/ML question...")

if user_input:
    # store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages
            ],
        )

        answer = response.choices[0].message.content

    except Exception as e:
        answer = "⚠️ Error generating response. Please check API key or model."

    # store assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)