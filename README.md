# Edwiserr — AI-Powered Career Navigation

Personality-driven career counselling system. Users complete a scenario-based assessment, receive an OCEAN personality profile, and get matched to careers, universities, and courses.

---

## Repo Structure

```
edwiserr/
├── backend/        FastAPI + ML (Python)
├── frontend/       React + Vite (JavaScript)
└── README.md
```

---

## Quick Start

**1. Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install fastapi uvicorn pandas numpy openpyxl
uvicorn main:app --reload
# → http://127.0.0.1:8000/docs
```

**2. Frontend**
```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

Both must run simultaneously. Backend on `8000`, frontend on `5173`.

---

## Current Scope

| Module | Status |
|---|---|
| Personality Engine (OCEAN scoring) | ✅ Done |
| Confidence Engine (Pillar 1 + 2) | ✅ Done |
| Career Recommendation Engine | 🔜 Phase 2 |
| University Ranking | 🔜 Phase 3 |
| AI Counselling Layer | 🔜 Phase 4 |
| Statistical Stability (Pillar 3) | 🔜 Needs calibration data |

---

## Team Split

| Role | Scope |
|---|---|
| ML Engineer | `backend/personality/` — scoring, confidence, selector |
| Backend | `backend/routers/`, `main.py`, deployment |
| Frontend | `frontend/src/` |
