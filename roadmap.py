import os
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI(title="Gemini Chat API")

class PromptRequest(BaseModel):
    prompt: str

def ask_gemini(prompt_text: str) -> str:
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')

        full_prompt = f"""[System Instruction: Create clear, step-by-step roadmaps based on the user's
        profession. Break tasks into small steps, and keep it simple and easy to follow.
        Your response must be in JSON format:
        {{
            "query": "{prompt_text}",
            "response": {{
                "title": "Roadmap for {prompt_text}",
                "description": [
                    {{"step_1": "Description of step 1"}},
                    {{"step_2": "Description of step 2"}},
                    {{"step_3": "Description of step 3"}}
                ],
                "created_time": "YYYY-MM-DD"
            }}
        }}
        ]"""

        response = model.generate_content(full_prompt)
        ai_response = response.text.strip()

        cleaned_response = re.sub(r"^```json\n|```$", "", ai_response).strip()
        return cleaned_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini Error: {str(e)}")

@app.post("/ask")
def get_gemini_response(request: PromptRequest):
    result = ask_gemini(request.prompt)
    return {"query": request.prompt, "gemini_response": result}

