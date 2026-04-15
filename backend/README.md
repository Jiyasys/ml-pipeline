# 🚀 Edwiserr Backend

AI-powered personality assessment API built with FastAPI using OCEAN model and MBTI mapping.

---

## 🧠 Overview

This backend provides:

* Adaptive personality questionnaire
* OCEAN trait scoring
* MBTI-style personality output
* Confidence scoring system
* RESTful API for frontend integration

---

## 🛠 Tech Stack

* **FastAPI**
* **Python 3.9+**
* **Uvicorn**
* **Pydantic**

---

## 📁 Project Structure

```
backend/
├── main.py
├── routers/
│   ├── __init__.py
│   └── personality.py
├── personality/
│   ├── __init__.py
│   ├── questions.py
│   ├── scorer.py
│   └── confidence.py
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd backend
```

---

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install fastapi uvicorn
```

---

### 4. Run the server

```bash
uvicorn main:app --reload
```

---

## 🌐 API Documentation

Once running:

👉 http://127.0.0.1:8000/docs

Interactive Swagger UI available.

---

## 🔌 API Endpoints

### ▶️ Get Questions

```http
POST /api/personality/questions
```

**Request:**

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

**Request:**

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

## 📊 Sample Response

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

## 🧪 Health Check

```http
GET /
```

Response:

```json
{
  "status": "Edwiserr API is running"
}
```

---

## ⚠️ Notes

* Adaptive questions vary based on user type
* Reverse scoring handled internally
* Confidence computed using statistical variance

---

## 🚧 Future Improvements

* Database integration (PostgreSQL / MongoDB)
* Authentication (JWT)
* Recommendation engine
* Deployment (Docker + Cloud)

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Built for scalable AI-driven career guidance.
