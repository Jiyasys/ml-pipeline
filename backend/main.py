# ============================================================
# EDWISERR — FastAPI Backend (Supabase edition)
# Run: uvicorn main:app --reload
# ============================================================

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import personality
from routers import careers
from routers.insights_feedback import router as insights_router
from routers.schools   import router as schools_router
from routers.sessions  import router as sessions_router
from routers.questions import router as questions_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)

app = FastAPI(
    title="Edwiserr API",
    description="AI-powered career navigation backend — Supabase edition",
    version="2.0.0",
)

API_PREFIX = "/api/v1"

# ── CORS — covers every way a local browser might call the API ────────────────
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Existing routers ──────────────────────────────────────────────────────────
app.include_router(personality.router, prefix=f"{API_PREFIX}/personality", tags=["Personality"])
app.include_router(careers.router,     prefix=f"{API_PREFIX}/careers",     tags=["Careers"])

# ── Supabase-backed routers ───────────────────────────────────────────────────
app.include_router(insights_router,  prefix=API_PREFIX)
app.include_router(schools_router,   prefix=API_PREFIX)
app.include_router(sessions_router,  prefix=API_PREFIX)
app.include_router(questions_router, prefix=API_PREFIX)

# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "Edwiserr API is running", "version": "2.0.0"}