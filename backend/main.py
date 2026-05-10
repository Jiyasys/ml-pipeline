# ============================================================
# EDWISERR — FastAPI Backend
# Entry point
# Run: uvicorn main:app --reload
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import personality
from routers import careers
from routers.insights_feedback import router as insights_router
from db.database import init_db
from routers import schools, sessions, questions

# ============================================================
# App
# ============================================================

app = FastAPI(
    title="Edwiserr API",
    description="AI-powered career navigation backend",
    version="1.0.0",
)
app.include_router(schools.router)
app.include_router(sessions.router)
app.include_router(questions.router)


# ============================================================
# Constants
# ============================================================

API_PREFIX = "/api/v1"

ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
]


# ============================================================
# Middleware
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Routers
# IMPORTANT:
# Routers themselves should NOT contain duplicated prefixes.
#
# Example:
#   careers.py      -> APIRouter()
#   personality.py  -> APIRouter()
#
# Prefixing is centralized here.
# ============================================================

app.include_router(
    personality.router,
    prefix=f"{API_PREFIX}/personality",
    tags=["Personality"],
)

app.include_router(
    careers.router,
    prefix=f"{API_PREFIX}/careers",
    tags=["Careers"],
)
app.include_router(insights_router, prefix=f"{API_PREFIX}/insights", tags=["Insights"])


# ============================================================
# Health Check
# ============================================================

@app.get("/")
def root():
    return {
        "status": "Edwiserr API is running",
        "version": "1.0.0",
    }
init_db()
