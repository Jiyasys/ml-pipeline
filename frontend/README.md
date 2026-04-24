# Frontend README

# Edwiserr Frontend

Frontend application for **Edwiserr**, an AI-powered personality assessment and career guidance platform.

Built using **React + Vite** for fast performance, clean UI, and scalable development.

---

## 🚀 Features

* Modern responsive UI
* Landing page
* User type selection
* Dynamic assessment quiz
* Real-time progress tracking
* Option-based questionnaire flow
* Results dashboard
* OCEAN trait visualization
* Confidence score display
* API integration with FastAPI backend

---

## 🛠 Tech Stack

* React.js
* Vite
* JavaScript
* Axios
* Recharts
* CSS

---

## 📂 Folder Structure

```text
frontend/
│── public/
│── src/
│   ├── pages/
│   │   ├── Landing.jsx
│   │   ├── UserType.jsx
│   │   ├── Quiz.jsx
│   │   └── Results.jsx
│   ├── components/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
│── package.json
│── vite.config.js
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repo-link>
cd frontend
```

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

---

## 🌐 Local Development

Frontend runs on:

```text
http://localhost:5173
```

Make sure backend is running on:

```text
http://127.0.0.1:8000
```

---

## 🔌 Backend Integration

### Get Questions

```http
POST /api/personality/questions
```

### Submit Answers

```http
POST /api/personality/submit
```

### Clarification Questions

```http
POST /api/personality/clarify
```

---

## 📱 Pages Included

### 1. Landing Page

Introduction to platform and start button.

### 2. User Type Selection

Choose category:

* Class 10
* Class 12
* Undergraduate
* Professional

### 3. Quiz Interface

* One question at a time
* A / B / C / D options
* Progress bar
* Timer tracking

### 4. Results Dashboard

Displays:

* OCEAN Scores
* MBTI-style label
* Confidence score
* Trait charts
* Insights

---

## 🎨 UI Goals

* Clean modern design
* Premium psychology-tool feel
* Fast interactions
* Mobile responsive
* Easy navigation

---

## 📌 Commands

Run project:

```bash
npm run dev
```

Build project:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

---

## 🔮 Future Enhancements

* Dark mode
* Animations
* Login system
* Dashboard history
* Career recommendation UI
* PDF report download
