from fastapi import FastAPI, Header, HTTPException, Depends
import ollama
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_CREDITS = {os.getenv("API_KEY"): 5}

app = FastAPI()

def verify_api_key(x_api_key: str = Header(None)):
    print(f"Received API key: '{x_api_key}'")
    print(f"Available API keys: {list(API_KEY_CREDITS.keys())}")
    print(f"API_KEY_CREDITS: {API_KEY_CREDITS}")
    
    credits = API_KEY_CREDITS.get(x_api_key, 0)
    print(f"Credits for this key: {credits}")
    
    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API key, or no credits")

    return x_api_key

@app.post("/generate")
def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):
    API_KEY_CREDITS[x_api_key] -= 1
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return {"response": response["message"]["content"]}
