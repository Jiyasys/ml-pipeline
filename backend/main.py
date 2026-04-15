# ============================================================
# EDWISERR — FastAPI Backend
# Entry point
# Run: uvicorn main:app --reload
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import personality

app = FastAPI(
    title="Edwiserr API",
    description="AI-powered career navigation backend",
    version="1.0.0"
)

# Allow React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(personality.router, prefix="/api/personality", tags=["Personality"])

@app.get("/")
def root():
    return {"status": "Edwiserr API is running"}