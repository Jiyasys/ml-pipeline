import { useState, useEffect } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000/api/personality";
const INST_ID = "inst_001";
const OPTIONS = ["A", "B", "C", "D"];

const TRAIT_COLORS = {
  Openness:          "#c9a84c",
  Conscientiousness: "#4c9ac9",
  Extraversion:      "#c94c7a",
  Agreeableness:     "#4cc97a",
  Neuroticism:       "#9a4cc9",
};

export default function Quiz({ userType, onComplete }) {
  const [questions, setQuestions]   = useState([]);
  const [current, setCurrent]       = useState(0);
  const [answers, setAnswers]       = useState({});
  const [selected, setSelected]     = useState(null);
  const [loading, setLoading]       = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError]           = useState(null);

  // Fetch questions on mount
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const res = await axios.post(`${API}/questions`, {
          user_type: userType,
          inst_id:   INST_ID,
          mode:      "fast",   // 25 questions
        });
        setQuestions(res.data.questions);
        setLoading(false);
      } catch (e) {
        setError("Could not load questions. Is the backend running?");
        setLoading(false);
      }
    };
    fetchQuestions();
  }, [userType]);

  const q = questions[current];
  const progress = questions.length > 0
    ? Math.round((current / questions.length) * 100)
    : 0;

  const handleSelect = (option) => {
    setSelected(option);
  };

  const handleNext = async () => {
    if (!selected) return;

    const newAnswers = { ...answers, [q.id]: selected };
    setAnswers(newAnswers);
    setSelected(null);

    if (current + 1 < questions.length) {
      setCurrent(current + 1);
    } else {
      // All answered — submit
      setSubmitting(true);
      try {
        const res = await axios.post(`${API}/submit`, {
          user_type: userType,
          inst_id:   INST_ID,
          answers:   newAnswers,
        });
        onComplete(res.data);
      } catch (e) {
        setError("Submission failed. Please try again.");
        setSubmitting(false);
      }
    }
  };

  const handleBack = () => {
    if (current === 0) return;
    const prevQ = questions[current - 1];
    setSelected(answers[prevQ.id] || null);
    setCurrent(current - 1);
  };

  // ── Loading state
  if (loading) {
    return (
      <div className="quiz">
        <div className="quiz-header">
          <div className="quiz-logo">EDWISerr</div>
        </div>
        <div className="quiz-loading">
          <div className="spinner" />
          <span style={{ color: "var(--muted)", fontSize: 14 }}>
            Preparing your assessment…
          </span>
        </div>
      </div>
    );
  }

  // ── Submitting state
  if (submitting) {
    return (
      <div className="quiz">
        <div className="quiz-header">
          <div className="quiz-logo">EDWISerr</div>
        </div>
        <div className="quiz-loading">
          <div className="spinner" />
          <span style={{ color: "var(--muted)", fontSize: 14 }}>
            Analysing your responses…
          </span>
        </div>
      </div>
    );
  }

  // ── Error state
  if (error) {
    return (
      <div className="quiz">
        <div className="quiz-header">
          <div className="quiz-logo">EDWISerr</div>
        </div>
        <div className="quiz-loading">
          <span style={{ color: "var(--danger)", fontSize: 14 }}>{error}</span>
        </div>
      </div>
    );
  }

  const traitColor = TRAIT_COLORS[q?.trait] || "var(--gold)";

  return (
    <div className="quiz">
      {/* Header */}
      <div className="quiz-header">
        <div className="quiz-logo">EDWISerr</div>
        <div className="quiz-meta">
          {current + 1} / {questions.length}
        </div>
      </div>

      {/* Progress */}
      <div className="quiz-progress-bar">
        <div
          className="quiz-progress-fill"
          style={{ width: `${progress}%`, background: traitColor }}
        />
      </div>

      {/* Question body */}
      <div className="quiz-body">
        <div
          className="quiz-trait-tag"
          style={{ color: traitColor, borderColor: `${traitColor}44` }}
        >
          <span style={{
            width: 6, height: 6, borderRadius: "50%",
            background: traitColor, display: "inline-block"
          }} />
          {q.trait} · {q.sub_dimension.replace(/_/g, " ")}
        </div>

        <div className="quiz-question">{q.scenario}</div>

        <div className="quiz-options">
          {OPTIONS.map((opt) => (
            <button
              key={opt}
              className={`quiz-option${selected === opt ? " selected" : ""}`}
              onClick={() => handleSelect(opt)}
              style={selected === opt ? {
                borderColor: traitColor,
                background: `${traitColor}12`,
              } : {}}
            >
              <span
                className="option-letter"
                style={selected === opt ? {
                  background: traitColor,
                  borderColor: traitColor,
                  color: "var(--navy)",
                } : { color: traitColor, borderColor: `${traitColor}55` }}
              >
                {opt}
              </span>
              <span className="option-text">{q[`option_${opt}`]}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="quiz-footer">
        <button
          className="btn-ghost"
          onClick={handleBack}
          disabled={current === 0}
          style={{ opacity: current === 0 ? 0.3 : 1 }}
        >
          ← Back
        </button>

        <button
          className="btn-primary"
          onClick={handleNext}
          disabled={!selected}
          style={{
            opacity: selected ? 1 : 0.4,
            background: selected ? traitColor : "var(--gold)",
            cursor: selected ? "pointer" : "not-allowed",
          }}
        >
          {current + 1 === questions.length ? "See Results" : "Next"}
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
}