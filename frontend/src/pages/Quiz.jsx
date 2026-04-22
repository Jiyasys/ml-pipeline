import { useState, useEffect, useRef } from "react";
import axios from "axios";

const API    = "http://127.0.0.1:8000/api/personality";
const INST   = "inst_001";
const OPTS   = ["A", "B", "C", "D"];

const TRAIT_COLORS = {
  Openness:          "#c9a84c",
  Conscientiousness: "#4c9ac9",
  Extraversion:      "#c94c7a",
  Agreeableness:     "#4cc97a",
  Neuroticism:       "#9a4cc9",
};

export default function Quiz({ userType, onComplete }) {
  const [questions, setQuestions]     = useState([]);
  const [current, setCurrent]         = useState(0);
  const [answers, setAnswers]         = useState({});
  const [responseTimes, setResponseTimes] = useState({});  // {qid: ms}
  const [selected, setSelected]       = useState(null);
  const [loading, setLoading]         = useState(true);
  const [submitting, setSubmitting]   = useState(false);
  const [error, setError]             = useState(null);

  // Timestamp when current question was shown
  const questionStartRef = useRef(null);

  // Fetch questions on mount
  useEffect(() => {
    axios.post(`${API}/questions`, {
      user_type: userType,
      inst_id:   INST,
      mode:      "fast",
    })
    .then(res => {
      setQuestions(res.data.questions);
      setLoading(false);
      questionStartRef.current = Date.now();
    })
    .catch(() => {
      setError("Could not load questions. Is the backend running?");
      setLoading(false);
    });
  }, [userType]);

  // Reset timer whenever question index changes
  useEffect(() => {
    if (!loading) {
      questionStartRef.current = Date.now();
      // Restore previously selected answer if navigating back
      if (questions[current]) {
        setSelected(answers[questions[current].id] || null);
      }
    }
  }, [current, loading]);

  const q      = questions[current];
  const color  = TRAIT_COLORS[q?.trait] || "var(--gold)";
  const pct    = questions.length > 0
    ? Math.round((current / questions.length) * 100)
    : 0;

  const recordTime = (qid) => {
    const elapsed = Date.now() - (questionStartRef.current || Date.now());
    setResponseTimes(prev => ({ ...prev, [qid]: elapsed }));
  };

  const handleSelect = (opt) => setSelected(opt);

  const handleNext = async () => {
    if (!selected) return;

    // Record how long this question took
    recordTime(q.id);

    const newAnswers = { ...answers, [q.id]: selected };
    setAnswers(newAnswers);

    if (current + 1 < questions.length) {
      setCurrent(current + 1);
      setSelected(null);
    } else {
      // Last question — submit everything
      setSubmitting(true);
      try {
        // Merge the last timing record before submitting
        const finalTimes = {
          ...responseTimes,
          [q.id]: Date.now() - (questionStartRef.current || Date.now()),
        };
        const res = await axios.post(`${API}/submit`, {
          user_type:         userType,
          inst_id:           INST,
          answers:           newAnswers,
          response_times_ms: finalTimes,
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
    // Record time even when going back (counts as engagement)
    recordTime(q.id);
    setCurrent(current - 1);
  };

  // ── States ────────────────────────────────────────────────

  if (loading) return <QuizShell><Spinner text="Preparing your assessment…" /></QuizShell>;
  if (submitting) return <QuizShell><Spinner text="Analysing your responses…" /></QuizShell>;
  if (error) return (
    <QuizShell>
      <p style={{ color: "var(--danger)", fontSize: 14 }}>{error}</p>
    </QuizShell>
  );

  return (
    <div className="quiz">
      {/* Header */}
      <div className="quiz-header">
        <div className="quiz-logo">EDWISerr</div>
        <div className="quiz-meta">{current + 1} / {questions.length}</div>
      </div>

      {/* Progress bar */}
      <div className="quiz-progress-bar">
        <div
          className="quiz-progress-fill"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>

      {/* Body */}
      <div className="quiz-body">
        <div
          className="quiz-trait-tag"
          style={{ color, borderColor: `${color}44` }}
        >
          <span style={{
            width: 6, height: 6, borderRadius: "50%",
            background: color, display: "inline-block",
          }} />
          {q.trait} · {q.sub_dimension.replace(/_/g, " ")}
        </div>

        <div className="quiz-question">{q.scenario}</div>

        <div className="quiz-options">
          {OPTS.map(opt => (
            <button
              key={opt}
              className={`quiz-option${selected === opt ? " selected" : ""}`}
              onClick={() => handleSelect(opt)}
              style={selected === opt
                ? { borderColor: color, background: `${color}12` }
                : {}}
            >
              <span
                className="option-letter"
                style={selected === opt
                  ? { background: color, borderColor: color, color: "var(--navy)" }
                  : { color, borderColor: `${color}55` }}
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
            opacity:    selected ? 1 : 0.4,
            background: selected ? color : "var(--gold)",
            cursor:     selected ? "pointer" : "not-allowed",
          }}
        >
          {current + 1 === questions.length ? "See Results" : "Next"}
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3 8h10M9 4l4 4-4 4"
              stroke="currentColor" strokeWidth="1.5"
              strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
}

// ── Sub-components ────────────────────────────────────────────

function QuizShell({ children }) {
  return (
    <div className="quiz">
      <div className="quiz-header">
        <div className="quiz-logo">EDWISerr</div>
      </div>
      <div className="quiz-loading">{children}</div>
    </div>
  );
}

function Spinner({ text }) {
  return (
    <>
      <div className="spinner" />
      <span style={{ color: "var(--muted)", fontSize: 14 }}>{text}</span>
    </>
  );
}