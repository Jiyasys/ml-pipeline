import { useState } from "react";

const SCALE = [1, 2, 3, 4, 5];
const LABELS = { 1: "Strongly Disagree", 3: "Neutral", 5: "Strongly Agree" };

export default function Quiz({ questions, onSubmit }) {
  const [answers, setAnswers] = useState({});
  const [current, setCurrent] = useState(0);

  const q = questions[current];
  const total = questions.length;
  const answered = answers[q?.id];

  function select(val) {
    setAnswers((prev) => ({ ...prev, [q.id]: val }));
  }

  function next() {
    if (current < total - 1) setCurrent((c) => c + 1);
  }

  function prev() {
    if (current > 0) setCurrent((c) => c - 1);
  }

  function submit() {
    if (Object.keys(answers).length < total) {
      alert("Please answer all questions before submitting.");
      return;
    }
    onSubmit(answers);
  }

  if (!q) return null;

  return (
    <div style={styles.wrap}>
      <p style={styles.progress}>{current + 1} / {total}</p>
      <div style={styles.bar}>
        <div style={{ ...styles.fill, width: `${((current + 1) / total) * 100}%` }} />
      </div>

      <p style={styles.question}>{q.text}</p>

      <div style={styles.scale}>
        {SCALE.map((val) => (
          <button
            key={val}
            onClick={() => select(val)}
            style={{
              ...styles.scaleBtn,
              background: answered === val ? "#4f46e5" : "#f3f4f6",
              color: answered === val ? "#fff" : "#111",
            }}
          >
            {val}
          </button>
        ))}
      </div>
      <div style={styles.scaleLabels}>
        <span>Strongly Disagree</span>
        <span>Strongly Agree</span>
      </div>

      <div style={styles.nav}>
        <button onClick={prev} disabled={current === 0} style={styles.navBtn}>← Back</button>
        {current < total - 1 ? (
          <button onClick={next} disabled={!answered} style={styles.navBtn}>Next →</button>
        ) : (
          <button onClick={submit} style={{ ...styles.navBtn, background: "#4f46e5", color: "#fff" }}>
            Submit
          </button>
        )}
      </div>
    </div>
  );
}

const styles = {
  wrap: { maxWidth: 520, margin: "60px auto", fontFamily: "sans-serif", padding: "0 16px" },
  progress: { textAlign: "right", color: "#888", fontSize: 14 },
  bar: { height: 6, background: "#e5e7eb", borderRadius: 4, marginBottom: 32 },
  fill: { height: "100%", background: "#4f46e5", borderRadius: 4, transition: "width 0.3s" },
  question: { fontSize: 20, fontWeight: 600, marginBottom: 28, lineHeight: 1.5 },
  scale: { display: "flex", justifyContent: "center", gap: 12 },
  scaleBtn: { width: 48, height: 48, borderRadius: "50%", border: "none", fontSize: 16, cursor: "pointer" },
  scaleLabels: { display: "flex", justifyContent: "space-between", fontSize: 12, color: "#888", marginTop: 8 },
  nav: { display: "flex", justifyContent: "space-between", marginTop: 40 },
  navBtn: { padding: "10px 24px", borderRadius: 8, border: "1px solid #ccc", cursor: "pointer", fontSize: 15 },
};