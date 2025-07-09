import os
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize FastAPI app
app = FastAPI(title="Gemini Chat API")

# Pydantic model for incoming request
class PromptRequest(BaseModel):
    prompt: str

# Gemini function
def ask_gemini(prompt_text: str) -> str:
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')

        # Full prompt with system instructions
        full_prompt = f"""[System Instruction: You are a helpful assistant of Canada project. Use formal language, don't be rude. Your response must be in JSON format with:
        "query": "",
        "response": "",
        "created_time": ""
        ]
        [User Question: {prompt_text}]"""

        # Generate response
        response = model.generate_content(full_prompt)
        ai_response = response.text.strip()

        # Remove Markdown code block (```json ... ```)
        cleaned_response = re.sub(r"^```json\n|```$", "", ai_response).strip()
        return cleaned_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini Error: {str(e)}")

# POST endpoint for chat
@app.post("/ask")
def get_gemini_response(request: PromptRequest):
    result = ask_gemini(request.prompt)
    return {"query": request.prompt, "gemini_response": result}

