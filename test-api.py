"""
Test script for the FastAPI LLM API.

This script demonstrates how to make requests to the API endpoint
and serves as a simple integration test for the authentication
and text generation functionality.

Usage:
    python test-api.py

Requirements:
    - API server must be running on localhost:8000
    - Valid API key must be set in .env file
    - requests library must be installed
"""

# Import required libraries
import requests  # HTTP client for making API requests
from dotenv import load_dotenv  # Load environment variables from .env file
import os  # Access to environment variables

# Load environment variables from .env file
# This loads the API_KEY that will be used for authentication
load_dotenv()

# Configure the API request
# The prompt parameter is passed as a query parameter in the URL
url = "http://127.0.0.1:8000/generate?prompt=Tell me about Python"

# Set up headers for the API request
# x-api-key: Required for authentication (loaded from .env file)
# Content-Type: Specifies the format of the request body (though not used here)
headers = {
    "x-api-key": os.getenv("API_KEY"), 
    "Content-Type": "application/json"
}

# Make POST request to the API endpoint
# This will consume 1 credit from the API key's balance
response = requests.post(url, headers=headers)

# Print the JSON response from the API
# Expected format: {"response": "Generated text from Mistral model"}
print(response.json())