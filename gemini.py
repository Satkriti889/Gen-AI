import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# os.environ["GEMINI_API_KEY"] = "AIzaSyD60cXm-ABUVzfBNd9keBZL5OC5Mq3nSz4"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_gemini(prompt_text):
    
    try:
        model= genai.GenerativeModel('gemini-2.5-flash')

        response = model.generate_content(prompt_text)

        return response.text.strip()
    except Exception as e:
        return f"An error occoured : {e}"
    
prompt = "Guess the random number between 1 and 50."
response_text = ask_gemini(prompt)

print("---My Prompt---")
print(prompt)
print("\n---GPT's RESPONSE---")
print(response_text)
