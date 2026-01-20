import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:8000/api"

def test_health():
    response = requests.get("http://127.0.0.1:8000/health")
    print(f"Health Check: {response.json()}")

def test_ingest():
    files = {'file': open('sample_info.txt', 'rb')}
    data = {'strategy': 'recursive', 'chunk_size': 200, 'chunk_overlap': 20}
    response = requests.post(f"{BASE_URL}/ingest", files=files, data=data)
    print(f"Ingest Response: {json.dumps(response.json(), indent=2)}")

def test_chat(session_id: str, query: str):
    data = {'query': query, 'session_id': session_id}
    response = requests.post(f"{BASE_URL}/chat", data=data)
    try:
        res_json = response.json()
        print(f"Chat (Q: {query}):\n{json.dumps(res_json, indent=2)}\n")
        return res_json
    except Exception as e:
        print(f"Error parsing JSON from chat: {e}")
        print(f"Raw response: {response.text}")
        return None

if __name__ == "__main__":
    # Note: Server must be running for this to work
    # Command: .\venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
    try:
        test_health()
        test_ingest()
        sid = str(uuid.uuid4())
        test_chat(sid, "What is AI?")
        test_chat(sid, "I want to book an interview. My name is Sudip, email is sudip@example.com, for Jan 25th at 2PM.")
    except Exception as e:
        print(f"Connection error (is the server running?): {e}")
