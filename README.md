# RAG Backend with Interview Booking

A robust FastAPI backend that handles document ingestion and multi-turn conversational RAG with built-in agentic interview booking capabilities.

## Features
- **Document Ingestion**: Upload PDF/TXT files, extract text, and index using Qdrant.
- **Conversational RAG**: Context-aware chat using Groq (Llama 3.1 8B).
- **Interview Booking**: Automatically extracts name, email, date, and time from natural language and saves to SQLite.
- **Portability**: Automatic in-memory fallbacks for Qdrant and Redis.

## Getting Started

### 1. Clone the Repo
```bash
git clone git@github.com:Sudip7878/Task.git
cd Task
```

### 2. Setup Environment
Create a `.env` file in the root directory and add your Groq API Key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

pip install -r requirements.txt
```

### 4. Run the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 5. Access Documentation
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Running the Demo
You can run the unified test suite to verify the end-to-end flow:
```bash
python scripts/test_api.py
```

## Note on Dependencies
The app includes automatic fallbacks for **Redis** (chat history) and **Qdrant** (vector search). If these services are not running locally, the app will use in-memory storage, making it very easy to test without complex infrastructure.
