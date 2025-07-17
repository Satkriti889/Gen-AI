from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
import re

# Initialize FastAPI app
app = FastAPI(title="Simple Text Humanizer")

# Configure Google API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY environment variable is missing")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Input model
class TextRequest(BaseModel):
    text: str

# Output model (only humanized)
class TextResponse(BaseModel):
    humanized: str

# Prompt for Gemini
HUMANIZE_PROMPT = """
Rewrite this text to sound more natural and human-like while keeping the same meaning:

{text}
"""

@app.get("/")
async def home():
    return {"message": "Text Humanizer API. Use POST /humanize to get a result."}

@app.post("/humanize", response_model=TextResponse)
async def humanize_text(request: TextRequest):
    try:
        prompt = HUMANIZE_PROMPT.format(text=request.text)
        response = model.generate_content({
            "parts": [prompt]
        })

        candidate = response.candidates[0]

        # Try these attributes in order:
        humanized = None
        if hasattr(candidate, "output"):
            humanized = candidate.output.strip()
        elif hasattr(candidate, "text"):
            humanized = candidate.text.strip()
        elif hasattr(candidate, "message") and hasattr(candidate.message, "content"):
            humanized = candidate.message.content.strip()
        else:
            # fallback to regex extract from string
            s = str(candidate)
            match = re.search(r'text:\s*"([^"]+)"', s)
            humanized = match.group(1) if match else s

        return TextResponse(humanized=humanized)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
