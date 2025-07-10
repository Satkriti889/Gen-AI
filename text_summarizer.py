import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_gemini_system_prompt(prompt_text):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        full_prompt = (
            "[System Instruction: You are text summarizer, you summarize the given text by the user. "
            "You must summarize the text in a short paragraph. "
            '"query": "", "response": "", "created_time": "", ] '
            f"[User Question: {prompt_text}]"
        )
        response = model.generate_content(full_prompt)
        ai_response = response.text.strip()
        return ai_response
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit App UI
st.set_page_config(page_title="Gemini Text Summarizer", layout="centered")
st.title("📝 Gemini Text Summarizer")

with st.form("summarizer_form"):
    user_input = st.text_area("✍️ Enter the text to summarize", height=200)
    submitted = st.form_submit_button("Summarize")

    if submitted:
        if user_input.strip():
            with st.spinner("Summarizing..."):
                summary = ask_gemini_system_prompt(user_input)
            st.subheader("🔍 Summary")
            st.write(summary)
        else:
            st.error("Please enter some text to summarize.")
