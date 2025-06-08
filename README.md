# API for LLM

A FastAPI-based REST API that provides access to Ollama's Mistral model with API key authentication and credit-based usage tracking.

## Features

- 🔐 API key authentication with credit system
- 🤖 Integration with Ollama's Mistral model
- 📊 Usage tracking and credit management
- 🚀 FastAPI with automatic interactive documentation
- 🔄 Auto-reload development server

## Setup

### Prerequisites

- Python 3.8+
- Ollama installed and running
- Mistral model available in Ollama

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd API-For-LLM
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API key:
```bash
cp .env.example .env
```
Then edit `.env` and replace `your_secret_api_key_here` with your actual API key:
```
API_KEY=your_actual_secret_key
```

**⚠️ Important:** Never commit your `.env` file to version control. It contains sensitive information.

4. Run the server:
```bash
uvicorn main:app --reload
```

## Usage

### API Endpoints

#### POST /generate

Generate text using the Mistral model.

**Headers:**
- `x-api-key`: Your API key (required)

**Parameters:**
- `prompt`: The text prompt for generation (query parameter)

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/generate?prompt=Hello, how are you?" \
     -H "x-api-key: your_secret_api_key_here"
```

**Response:**
```json
{
  "response": "Generated text response from Mistral model"
}
```

### Interactive Documentation

Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI documentation.

## Credit System

- Each API key starts with 5 credits
- Each request consumes 1 credit
- When credits reach 0, the API key becomes invalid

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload
```

This enables auto-reload when code changes are detected.

### Testing

The project includes debug logging to help troubleshoot authentication issues.

## Security

- The `.env` file is excluded from version control to protect sensitive API keys
- Use the provided `.env.example` as a template for your local `.env` file
- Each API key has a limited number of credits to prevent abuse
- API key validation is performed on every request

## License

MIT License
