const BASE = "http://127.0.0.1:8000/api/personality";

export async function fetchQuestions(user_type, inst_id) {
  const res = await fetch(`${BASE}/questions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_type, inst_id }),
  });
  return res.json();
}

export async function submitAnswers(user_type, inst_id, answers) {
  const res = await fetch(`${BASE}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_type, inst_id, answers }),
  });
  return res.json();
}