import redis
import json
from typing import List, Dict, Any, Optional
from groq import Groq
from app.core.config import settings
from app.utils.vector_store import vector_store

class ChatMemory:
    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=settings.REDIS_HOST, 
                port=settings.REDIS_PORT, 
                db=0, 
                decode_responses=True,
                socket_connect_timeout=1 # Fast fail
            )
            self.redis.ping()
        except Exception:
            # Fallback to in-memory dict for demo if Redis is unavailable
            print("Redis unavailable, using in-memory chat history")
            self.redis = None
            self._history = {}

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        if self.redis:
            history = self.redis.get(f"chat:{session_id}")
            return json.loads(history) if history else []
        return self._history.get(session_id, [])

    def add_message(self, session_id: str, role: str, content: str):
        history = self.get_history(session_id)
        history.append({"role": role, "content": content})
        # Keep last 10 messages
        history = history[-10:]
        if self.redis:
            self.redis.set(f"chat:{session_id}", json.dumps(history), ex=3600) # 1 hour expiry
        else:
            self._history[session_id] = history

class RAGService:
    def __init__(self):
        self.memory = ChatMemory()
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate_answer(self, query: str, session_id: str) -> str:
        # 1. Get History
        history = self.memory.get_history(session_id)
        
        # 2. Retrieval - using vector store search
        search_results = vector_store.search(query, limit=3)
        context = "\n---\n".join([res["text"] for res in search_results])
        
        # 3. Construct Prompt
        system_prompt = f"""You are a helpful assistant. Use the following context to answer the user's question.
If the context doesn't contain the answer, use your general knowledge but mention it's not in the documents.
Keep track of the conversation history.

Context:
{context}
"""
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": query})
        
        # 4. LLM Call
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=settings.LLM_MODEL,
        )
        answer = chat_completion.choices[0].message.content
        
        # 5. Save history
        self.memory.add_message(session_id, "user", query)
        self.memory.add_message(session_id, "assistant", answer)
        
        return answer

rag_service = RAGService()
