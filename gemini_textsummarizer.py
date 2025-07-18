import google.generativeai as genai
import os 
from dotenv import load_dotenv
import re
#set your api key

# Load environment variables from .env file
load_dotenv()
# Configure Gemini AI with API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_gemini_system_prompt(prompt_text):
    try:
        model=genai.GenerativeModel("gemini-2.5-pro")
        full_prompt=f"""[System Instruction: You are text summarizer, you summarize the given text by the user. You must summarize the text in a short paragraph.
        "query":   "" ,
        "response":  ""   ,
        "created_time":   ""  ,
        ]
        [User Question: {prompt_text}]"""

        response=model.generate_content(full_prompt)
        ai_response=response.text.strip()
        refined_response=re.sub(r"(^json\n|$)","",ai_response).strip()
        return refined_response
    
    except Exception as e:
        return f"An error occured: {e}"
    
print("Welcome to the text summarizer.")
prompt = input("Enter the text to summarize: ")
response_text = ask_gemini_system_prompt(prompt)

print("---My Prompt---")
print(prompt)
print("---GPT's Response---")
print(response_text)