from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from datetime import datetime
import json

class DocumentMetadata(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    chunking_strategy: str
    file_type: str
    num_chunks: int

class InterviewBooking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    booking_date: str
    booking_time: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
