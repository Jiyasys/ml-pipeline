# Edwiserr — Backend

FastAPI backend. Handles personality scoring, confidence calculation, and question selection.

---

## Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn pandas numpy openpyxl
uvicorn main:app --reload
```

Swagger docs at `http://127.0.0.1:8000/docs`

---

## Structure

```
backend/
├── main.py                  Entry point, CORS config
├── routers/
│   └── personality.py       API endpoints
└── personality/
    ├── questions.py         375 questions + sub-dimension registry
    ├── scorer.py            OCEAN scoring + confidence engine
    ├── selector.py          Adaptive question selection
    └── confidence.py        (legacy — superseded by scorer.py)
```

---

## API Endpoints

### `POST /api/personality/questions`
Returns adaptive question set. Weights are never exposed to frontend.

```json
{ "user_type": "undergraduate", "inst_id": "inst_001", "mode": "fast" }
```

Modes: `fast` (25Q) · `standard` (75Q) · `full` (375Q)

---

### `POST /api/personality/submit`
Accepts answers + response times. Returns full OCEAN profile.

```json
{
  "user_type": "undergraduate",
  "inst_id": "inst_001",
  "answers": { "O1": "C", "ST1": "A" },
  "response_times_ms": { "O1": 4200, "ST1": 8100 }
}
```

---

### `POST /api/personality/clarify`
Returns 2 targeted questions for traits with lowest confidence.

---

## Scoring Logic

**OCEAN Scores (0–100)**
Each question has pre-assigned option weights (0.1–0.9). Score = average weight × 100. Neuroticism is inverted so 100 = emotionally stable across all traits.

**Confidence Engine — 3 Pillars**

| Pillar | Weight | Method |
|---|---|---|
| P1 Internal Consistency | 40% | Cronbach's alpha per trait |
| P2 Behavioral Quality | 35% | RT flags + straight-lining + IRV |
| P3 Statistical Stability | 25% | Stubbed — needs calibration data |

```
Confidence(trait)   = 0.40×C1 + 0.35×C2 + 0.25×C3
Confidence(overall) = mean across all 5 traits
Threshold           = 0.75 → below triggers clarification questions
```

**P2 Behavioral flags**
- RT < 1.5s → rushing (full penalty)
- RT 1.5–3s → fast (small penalty)
- RT > 90s → distracted (moderate penalty)
- ≥4 same consecutive options → straight-lining suspect
- ≥7 same consecutive options → strong IER signal

---

## Dataset

`personality/questions.py` — generated from `Personality_fixed.xlsx`

- 375 questions · 5 traits · 5 sub-dimensions each · 15 questions per sub-dimension
- Neuroticism weights are inverted (A=0.9 high distress → D=0.1 low distress)

---

## Institution Config

`inst_001` — General (all user types)
`inst_002` — Engineering college
`inst_003` — Arts & Commerce college

Add new institutions in `selector.py` → `USER_TYPE_SUBDIM_BOOST`.
