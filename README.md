

# Edwiserr – AI Career Guidance Platform

**Edwiserr** is an AI-powered psychometric assessment and career recommendation platform designed for students and professionals.

The system evaluates personality traits using the **OCEAN Five Factor Model**, calculates confidence scores, and recommends careers aligned with the user's behavioral profile.

Built with **React + FastAPI** for modern scalable full-stack deployment.

---

## 🚀 Key Features

* Personality Assessment Engine
* OCEAN Trait Scoring
* MBTI-style Display Label
* Confidence Score Analytics
* Adaptive Question Flow
* Career Recommendation Engine
* Modern Interactive Dashboard
* FastAPI REST APIs
* React Frontend UI
* Scalable Architecture

---

## 🛠 Tech Stack

### Frontend

* React.js
* Vite
* Axios
* Recharts
* CSS

### Backend

* Python
* FastAPI
* Uvicorn
* Pandas
* NumPy
* Pydantic

---

## 📂 Project Structure

```text id="b0dx43"
edwiserr/
│── README.md
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
│
└── backend/
    ├── main.py
    ├── routers/
    ├── personality/
    ├── careers/
    ├── venv/
    └── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash id="s2q6c5"
git clone <your-repo-link>
cd edwiserr
```

---

## ▶️ Run Backend

```bash id="0rx8e6"
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend URL:

```text id="7cv7xk"
http://127.0.0.1:8000
```

API Docs:

```text id="q8ccu4"
http://127.0.0.1:8000/docs
```

---

## ▶️ Run Frontend

```bash id="w9gll3"
cd frontend
npm install
npm run dev
```

Frontend URL:

```text id="pj5s8p"
http://localhost:5173
```

---

## 🧠 How It Works

### Step 1 – User Selection

Choose user type:

* Class 10
* Class 12
* Undergraduate
* Professional

### Step 2 – Assessment

Users answer scenario-based personality questions.

### Step 3 – Analysis

Backend computes:

* OCEAN Scores
* MBTI-style Label
* Confidence Score

### Step 4 – Recommendation

System suggests careers best aligned with the user profile.

---

## 📊 Personality Traits Used

* **O** – Openness
* **C** – Conscientiousness
* **E** – Extraversion
* **A** – Agreeableness
* **N** – Neuroticism

---

## 🎯 Sample Career Outputs

* Software Engineer
* Data Scientist
* Product Manager
* UX Designer
* Entrepreneur
* Analyst
* Healthcare Professional
* Creative Strategist

---

## 🔌 Main APIs

### Personality

```http id="i5l5gh"
POST /api/personality/questions
POST /api/personality/submit
POST /api/personality/clarify
```

### Careers

```http id="7w1mbr"
POST /api/careers/recommend
GET /api/careers/profiles
```

---

## 📌 Development Commands

### Frontend

```bash id="hmzz81"
npm run dev
npm run build
```

### Backend

```bash id="9nobor"
uvicorn main:app --reload
```

---

## 🔒 Future Scope

* Login / Authentication
* User History Dashboard
* Resume-based Career Matching
* AI Chat Guidance
* PDF Reports
* Admin Analytics Panel
* O*NET Live Career Integration


**Edwiserr – AI-powered Career Guidance using Psychometric Intelligence**
(https://ml-pipeline-omega.vercel.app/)
