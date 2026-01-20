from typing import Optional, Dict
from pydantic import BaseModel, EmailStr
from groq import Groq
from app.core.config import settings
from sqlmodel import Session
from app.db.models import InterviewBooking
import json

class BookingDetails(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    date: Optional[str] = None
    time: Optional[str] = None

class BookingService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def extract_booking_info(self, query: str, history: list) -> Optional[BookingDetails]:
        prompt = f"""Extract interview booking information (name, email, date, time) from the user's latest query and conversation history.
Return a JSON object with keys: "name", "email", "date", "time". 
Use null if a field is not found.
Do not include any other text.

History:
{json.dumps(history[-5:])}

Query: {query}
"""
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=settings.LLM_MODEL,
        )
        try:
            content = response.choices[0].message.content
            # Basic parsing - LLM might wrap in markdown blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            data = json.loads(content)
            return BookingDetails(**data)
        except Exception as e:
            print(f"Extraction error: {e}")
            return None

    def save_booking(self, details: BookingDetails, db: Session):
        if all([details.name, details.email, details.date, details.time]):
            booking = InterviewBooking(
                name=details.name,
                email=details.email,
                booking_date=details.date,
                booking_time=details.time
            )
            db.add(booking)
            db.commit()
            db.refresh(booking)
            return booking
        return None

booking_service = BookingService()
