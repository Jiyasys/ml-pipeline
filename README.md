# 🚀 Edwiserr — AI Career Guidance Platform

An AI-powered personality assessment platform that evaluates users using the **OCEAN model** and maps results to an **MBTI-style personality type**.

Built with a modern full-stack architecture:

* ⚡ FastAPI (Backend)
* ⚛️ React + Vite (Frontend)

---

## 🧠 Features

* 🎯 Adaptive personality questionnaire
* 📊 OCEAN trait scoring (Big Five)
* 🔤 MBTI-style personality output
* 📈 Confidence scoring system
* ⚡ Real-time frontend–backend interaction
* 🧩 Clean and minimal UI

---

## 🏗️ Tech Stack

### Backend

* FastAPI
* Python 3.9+
* Uvicorn
* Pydantic

### Frontend

* React
* Vite
* JavaScript (ES6+)

---

## 📁 Project Structure

```bash
edwiserr/
│
├── backend/
│   ├── main.py
│   ├── routers/
│   │   └── personality.py
│   └── personality/
│       ├── questions.py
│       ├── scorer.py
│       └── confidence.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── Quiz.jsx
│   │   ├── Results.jsx
│   │   └── api.js
│
└── README.md
```

---

## ⚙️ Getting Started

### 🔹 1. Clone Repository

```bash
git clone <your-repo-url>
cd edwiserr
```

---

## 🧪 Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
```

Activate environment:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn
```

Run server:

```bash
uvicorn main:app --reload
```

Backend will run on:
👉 http://127.0.0.1:8000

Swagger docs:
👉 http://127.0.0.1:8000/docs

---

## 🎨 Frontend Setup (React)

Open new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:
👉 http://localhost:5173

---

## 🔗 API Integration

Frontend connects to backend via:

```js
const BASE = "http://127.0.0.1:8000/api/personality";
```

---

## 🔄 Application Flow

1. User selects profile (class_10 / class_12 / undergraduate / professional)
2. Frontend requests adaptive questions
3. User answers 25 questions
4. Answers sent to backend
5. Backend computes:

   * OCEAN scores
   * MBTI type
   * Confidence level
6. Results displayed visually

---

## 🔌 API Endpoints

### ▶️ Get Questions

```http
POST /api/personality/questions
```

```json
{
  "user_type": "undergraduate",
  "inst_id": "inst_001"
}
```

---

### ▶️ Submit Answers

```http
POST /api/personality/submit
```

```json
{
  "user_type": "undergraduate",
  "inst_id": "inst_001",
  "answers": {
    "O1": 4,
    "C2": 5
  }
}
```

---

## 📊 Sample Output

```json
{
  "ocean_scores": {
    "O": 78.5,
    "C": 65.2,
    "E": 52.1,
    "A": 70.3,
    "N": 40.6
  },
  "mbti_display": "ENFP",
  "confidence": {
    "overall": 0.82
  }
}
```

---

## ⚠️ Important Notes

* Backend must be running before frontend
* All questions must be answered before submission
* CORS is already configured in FastAPI

---

## 🚧 Future Improvements

* 🔐 Authentication system (JWT)
* 🗄️ Database integration
* 📊 Advanced analytics dashboard
* 🎯 Career recommendation engine
* 🌙 Dark mode UI

---


