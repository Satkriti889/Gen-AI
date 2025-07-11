import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("Google_API_KEY"))

# --- Page Configuration ---
st.set_page_config(page_title="Gemini Chat", layout="centered")
st.markdown("<h2 style='text-align: center; color: #00ffc8;'>💬 Chat Assistant</h2>", unsafe_allow_html=True)

# --- Initialize Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Custom CSS for Dark Theme and Chat Styling ---
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            margin-bottom: 10px;
        }
        .user-msg {
            background-color: #005C4B;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
            text-align: right;
            font-family: monospace;
        }
        .bot-msg {
            background-color: #262d36;
            color: #e0e0e0;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            text-align: left;
            font-family: monospace;
        }
        input {
            background-color: #1f1f1f !important;
            color: white !important;
        }
        .stTextInput > div > div > input {
            background-color: #1f1f1f;
            color: white;
        }
        .stButton>button {
            background-color: #e50914;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 8px 16px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Display Chat Messages ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in st.session_state.chat_history: # Removed reversed()
    if chat["role"] == "user":
        st.markdown(f"<div class='user-msg'>🧑‍💻 You: {chat['message']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>🤖 Chatbot: {chat['message']}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Input Handler Function ---
def handle_input():
    user_input = st.session_state.user_input.strip()
    if user_input == "":
        return
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(user_input)
        answer = response.text

        st.session_state.chat_history.append({"role": "user", "message": user_input})
        st.session_state.chat_history.append({"role": "gemini", "message": answer})
        st.session_state.user_input = "" # Clear the input box after sending
    except Exception as e:
        st.error(f"Error: {e}")

# --- User Input Box ---
st.text_input("Type your message and press Enter", key="user_input", on_change=handle_input)

# --- Clear Chat Button ---
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()