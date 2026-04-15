# 🎨 Edwiserr Frontend

Modern React-based UI for personality assessment powered by FastAPI backend.

---

## 🧠 Overview

Frontend application that:

* Collects user personality responses
* Displays questions interactively
* Shows OCEAN scores visually
* Displays MBTI-style personality result

---

## 🛠 Tech Stack

* **React**
* **Vite**
* **JavaScript (ES6+)**
* **Fetch API**

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── App.jsx
│   ├── Quiz.jsx
│   ├── Results.jsx
│   └── api.js
├── index.html
├── package.json
```

---

## ⚙️ Getting Started

### 1. Create project

```bash
npm create vite@latest frontend -- --template react
cd frontend
```

---

### 2. Install dependencies

```bash
npm install
```

---

### 3. Add source files

Replace the contents of `src/` with:

* `App.jsx`
* `Quiz.jsx`
* `Results.jsx`
* `api.js`

---

### 4. Start development server

```bash
npm run dev
```

---

## 🔗 Backend Integration

Ensure backend is running:

```
http://127.0.0.1:8000
```

API base configured in:

```js
const BASE = "http://127.0.0.1:8000/api/personality";
```

---

## 🔄 Application Flow

1. Select user type
2. Fetch questions from backend
3. Answer questionnaire
4. Submit responses
5. View results

---

## 🧩 Components

| Component   | Description                   |
| ----------- | ----------------------------- |
| App.jsx     | Controls flow and state       |
| Quiz.jsx    | Handles questions and answers |
| Results.jsx | Displays scores and results   |
| api.js      | API communication             |

---

## 📊 UI Features

* Step-by-step quiz navigation
* Progress bar
* Interactive rating scale (1–5)
* Score visualization
* Clean and minimal layout

---

## ⚠️ Important Notes

* Backend must be running before starting frontend
* All questions must be answered before submission
* CORS already configured in backend

---

## 🚧 Future Enhancements

* Charts (Recharts / Chart.js)
* Dark mode UI
* Authentication system
* Save user results
* Mobile responsiveness

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Built for seamless AI-driven user experience.
