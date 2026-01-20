from fastapi import FastAPI
from fastapi.responses import JSONResponse
import traceback
from app.core.config import settings
from app.db.session import create_db_and_tables

app = FastAPI(title=settings.PROJECT_NAME)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "error_message": str(exc),
            "traceback": traceback.format_exc()
        }
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG & Ingestion API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Routes will be included here
from app.api.routes import router
app.include_router(router, prefix="/api")
