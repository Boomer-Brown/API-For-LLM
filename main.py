"""
FastAPI-based REST API for Ollama's Mistral model with API key authentication.

This API provides a simple interface to interact with Ollama's Mistral language model
while implementing a credit-based usage system and API key authentication.

Architecture Overview:
1. FastAPI serves as the web framework for REST API endpoints
2. API key authentication is handled via HTTP headers
3. Credit system prevents abuse by limiting requests per API key
4. Ollama client communicates with locally running Mistral model
5. Environment variables store sensitive configuration data

Key Components:
- verify_api_key(): Dependency injection for authentication
- generate(): Main endpoint for text generation
- API_KEY_CREDITS: In-memory storage for credit tracking

Security Features:
- API key validation on every request
- Credit-based rate limiting
- Environment variable protection of secrets

Dependencies:
- FastAPI: Web framework
- Ollama: LLM client library
- python-dotenv: Environment variable management
- uvicorn: ASGI server for running FastAPI
"""

# FastAPI framework imports for creating the REST API
from fastapi import FastAPI, Header, HTTPException, Depends
# Ollama client for interfacing with the Mistral model
import ollama
# Operating system interface for environment variables
import os
# Load environment variables from .env file
from dotenv import load_dotenv

# Load environment variables from .env file into the application
load_dotenv()

# Dictionary to track API keys and their remaining credits
# Each API key starts with 5 credits, decremented with each request
# Format: {api_key: remaining_credits}
# Note: In production, this should be stored in a database for persistence
API_KEY_CREDITS = {os.getenv("API_KEY"): 5}

# Create FastAPI application instance
app = FastAPI(
    title="LLM API with Authentication",
    description="A REST API for Ollama's Mistral model with credit-based usage tracking",
    version="1.0.0"
)

def verify_api_key(x_api_key: str = Header(None)):
    """
    Dependency function to verify API key and check available credits.
    
    Args:
        x_api_key (str): API key provided in the 'x-api-key' header
        
    Returns:
        str: The validated API key
        
    Raises:
        HTTPException: 401 error if API key is invalid or has no credits remaining
    """
    # Debug logging to help troubleshoot authentication issues
    print(f"Received API key: '{x_api_key}'")
    print(f"Available API keys: {list(API_KEY_CREDITS.keys())}")
    print(f"API_KEY_CREDITS: {API_KEY_CREDITS}")
    
    # Get the credit count for the provided API key (defaults to 0 if key not found)
    credits = API_KEY_CREDITS.get(x_api_key, 0)
    print(f"Credits for this key: {credits}")
    
    # Reject request if API key is invalid or has no credits
    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API key, or no credits")

    return x_api_key

@app.post("/generate")
def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):
    """
    Generate text using Ollama's Mistral model.
    
    This endpoint accepts a text prompt and returns AI-generated text.
    It requires authentication via API key and consumes 1 credit per request.
    
    Args:
        prompt (str): The text prompt to send to the AI model
        x_api_key (str): API key for authentication (injected via dependency)
        
    Returns:
        dict: JSON response containing the generated text
        
    Raises:
        HTTPException: 401 if API key is invalid or no credits remaining
    """
    # Deduct one credit from the API key's balance
    API_KEY_CREDITS[x_api_key] -= 1
    
    # Send the prompt to Ollama's Mistral model and get response
    # The messages format follows the chat completion API standard
    response = ollama.chat(
        model="mistral", 
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract the generated text from the response and return it
    return {"response": response["message"]["content"]}


# Optional: Add a main block for easy development testing
# This allows running the script directly with: python main.py
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI application with uvicorn server
    # host="0.0.0.0" makes it accessible from other machines (use "127.0.0.1" for localhost only)
    # port=8000 is the default port for FastAPI applications
    # reload=True enables auto-reload during development
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
