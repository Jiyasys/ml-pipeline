# Backend README

# Edwiserr Backend

Backend service for **Edwiserr**, an AI-powered personality assessment and career guidance platform.

Built using **FastAPI + Python** to provide scalable APIs, psychometric scoring logic, confidence analytics, career recommendation logic, and frontend integration.

---

## 🚀 Features

* FastAPI REST APIs
* Adaptive personality question engine
* OCEAN personality scoring
* MBTI-style display label generation
* Confidence score system
* Response behavior analytics
* Clarification question flow
* Career recommendation engine
* Career profile matching
* Swagger API documentation
* Frontend integration ready

---

## 🛠 Tech Stack

* Python
* FastAPI
* Uvicorn
* Pydantic
* Pandas
* NumPy

---

## 📂 Folder Structure

```text
backend/
│── main.py
│── README.md
│── venv/
│
├── routers/
│   ├── __init__.py
│   ├── personality.py
│   └── careers.py
│
├── personality/
│   ├── confidence.py
│   ├── questions.py
│   ├── scorer.py
│   └── selector.py
│
└── careers/
    ├── __init__.py
    ├── profiles.py
    └── recommender.py
```

---

## ⚙️ Installation

Clone repository and move to backend folder:

```bash
git clone <your-repo-link>
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Mac / Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Server

```bash
uvicorn main:app --reload
```

---

## 🌐 Local Development

Backend runs on:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## 🔌 API Endpoints

### Root Health Check

```http
GET /
```

### Personality Questions

```http
POST /api/personality/questions
```

### Submit Personality Answers

```http
POST /api/personality/submit
```

### Clarification Questions

```http
POST /api/personality/clarify
```

### Career Recommendations

```http
POST /api/careers/recommend
```

### Career Profiles

```http
GET /api/careers/profiles
```

---

## 🧠 Core Modules

## personality/

### questions.py

Stores psychometric dataset, scenarios, options, weights, and trait mappings.

### selector.py

Adaptive question selection based on user type and mode.

### scorer.py

Calculates:

* OCEAN scores
* Trait averages
* MBTI-style label
* Personality profile

### confidence.py

Measures:

* Internal consistency
* Response timing behavior
* Straight-line detection
* Confidence scoring

---

## careers/

### profiles.py

Stores career benchmark profiles and domain mappings.

### recommender.py

Matches user personality profile with careers using scoring logic.

### routers/careers.py

Career recommendation API routes.

---

## 📊 Personality Model

Uses **OCEAN Five Factor Model**:

* Openness
* Conscientiousness
* Extraversion
* Agreeableness
* Neuroticism

---

## 🎯 Career Engine

Generates recommendations such as:

* Software Engineer
* Data Scientist
* Product Manager
* Designer
* Entrepreneur
* Analyst
* Healthcare Roles
* Creative Careers

Based on user personality fit.

---

## 📌 Commands

Run server:

```bash
uvicorn main:app --reload
```

Install packages:

```bash
pip install -r requirements.txt
```

Freeze dependencies:

```bash
pip freeze > requirements.txt
```

---

## 🔒 Future Enhancements

* JWT Authentication
* Database integration
* User assessment history
* PDF report export
* AI chatbot guidance
* Admin analytics dashboard
* Real-world O*NET integration

---


AI-powered Career Guidance System using Psychometric Intelligence.
