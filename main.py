from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from app import router as chat_router

# Create the main router
router = APIRouter()

# Initialize FastAPI app with metadata
app = FastAPI(
    title="drugboard.ai llm · rag application",
    version="1.0.0",
    description="A FastAPI application for drugboard.ai with LLM and RAG capabilities",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic health check endpoint
@router.get("/", tags=["health"])
async def health_check():
    return {"status": "healthy", "message": "Welcome to drugboard.ai API"}

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "message": str(exc)},
    )

# Include routers
app.include_router(router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        workers=1     # Number of worker processes
    )