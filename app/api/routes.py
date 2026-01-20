from fastapi import APIRouter, UploadFile, File, Depends, Form
from sqlmodel import Session
from app.db.session import get_session
from app.services.ingestion import ingestion_service
from app.services.rag import rag_service
from app.services.booking import booking_service
from typing import Optional

router = APIRouter()

@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    strategy: str = Form("recursive"),
    chunk_size: int = Form(500),
    chunk_overlap: int = Form(50),
    db: Session = Depends(get_session)
):
    content = await file.read()
    metadata = ingestion_service.process_document(
        content, file.filename, strategy, chunk_size, chunk_overlap, db
    )
    return {"message": "Document ingested successfully", "metadata": metadata}

@router.post("/chat")
async def chat(
    query: str = Form(...),
    session_id: str = Form(...),
    db: Session = Depends(get_session)
):
    # 1. Check for booking intent/info
    history = rag_service.memory.get_history(session_id)
    booking_info = booking_service.extract_booking_info(query, history)
    
    booking_status = ""
    if booking_info and any(v is not None for v in booking_info.model_dump().values()):
        saved_booking = booking_service.save_booking(booking_info, db)
        if saved_booking:
            booking_status = f" (Interview booked for {saved_booking.name} at {saved_booking.booking_time} on {saved_booking.booking_date})"

    # 2. Get RAG response
    response = rag_service.generate_answer(query, session_id)
    
    return {
        "answer": response + booking_status,
        "session_id": session_id,
        "booking_detected": booking_info.model_dump() if booking_info else None
    }
