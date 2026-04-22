# Edwiserr — Frontend

React + Vite UI. Four screens: Landing → User Type → Quiz → Results.

---

## Setup

```bash
cd frontend
npm install
npm install axios
npm run dev
# → http://localhost:5173
```

Backend must be running on `http://127.0.0.1:8000` before starting the quiz.

---

## Structure

```
frontend/src/
├── App.jsx           Screen router (landing → usertype → quiz → results)
├── index.css         Design system (CSS variables, shared components)
└── pages/
    ├── Landing.jsx   Hero page with stats
    ├── UserType.jsx  4-card user type selector
    ├── Quiz.jsx      One question at a time, live from API
    └── Results.jsx   OCEAN scores + confidence breakdown
```

---

## Screen Flow

```
Landing  →  UserType  →  Quiz (25Q)  →  Results
```

State lives in `App.jsx`. Each screen receives props and calls `onComplete` / `onSelect` to advance.

---

## Quiz Behaviour

- Fetches questions from `/api/personality/questions` on mount (`fast` mode = 25 questions)
- Records `Date.now()` when each question appears; computes elapsed ms on Next click
- Sends `answers` + `response_times_ms` to `/api/personality/submit`
- Progress bar and trait colour change per question trait

---

## Results Page

Shows:
- MBTI-style 4-letter label
- OCEAN score cards (0–100) with trait bars
- Confidence breakdown — Pillar 1 (alpha per trait), Pillar 2 (RT / straight-line / IRV)
- Raw JSON toggle
- Download profile as `.json`

---

## Design System

Defined in `index.css` via CSS variables:

| Variable | Value |
|---|---|
| `--navy` | `#0d1b2a` — background |
| `--gold` | `#c9a84c` — primary accent |
| `--cream` | `#f2ead8` — primary text |
| `--muted` | `#8a9ab0` — secondary text |

Fonts: `DM Serif Display` (headings) + `DM Sans` (body) via Google Fonts.

---

## API Config

Base URL set in `Quiz.jsx`:
```js
const API = "http://127.0.0.1:8000/api/personality";
```

Change this to your deployed backend URL before production.
