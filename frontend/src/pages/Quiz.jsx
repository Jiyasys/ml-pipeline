import { useEffect, useMemo, useRef, useState } from "react";
import axios from "axios";

const BASE = import.meta.env.VITE_API_URL;
const API = `${BASE}/personality`;

const LOW_CONFIDENCE_THRESHOLD = 0.65;

export default function Quiz({ userType, onComplete }) {
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);

  const [answers, setAnswers] = useState({});
  const [responseTimes, setResponseTimes] = useState({});

  const [selected, setSelected] = useState(null);

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const [error, setError] = useState("");

  const [clarificationMode, setClarificationMode] = useState(false);

  const questionStartRef = useRef(Date.now());
  const hiddenAtRef = useRef(null);

  const currentQuestion = questions[current];

  const progress = useMemo(() => {
    if (!questions.length) return 0;
    return ((current + 1) / questions.length) * 100;
  }, [current, questions.length]);

  // ───────────────────────────────────────────────────────────
  // Load Questions
  // ───────────────────────────────────────────────────────────

  const loadQuestions = async () => {
    try {
      setLoading(true);
      setError("");

      const res = await axios.post(`${API}/questions`, {
        user_type: userType,
        inst_id: "frontend-web",
        mode: "fast",
        seed: 42,
      });

      setQuestions(res.data.questions || []);
      setCurrent(0);

      questionStartRef.current = Date.now();
    } catch (err) {
      console.error(err?.response?.data || err);

      setError("Could not load questions. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // ───────────────────────────────────────────────────────────
  // Visibility Handling
  // ───────────────────────────────────────────────────────────

  useEffect(() => {
    const handleVisibility = () => {
      if (document.hidden) {
        hiddenAtRef.current = Date.now();
      } else {
        if (hiddenAtRef.current) {
          const hiddenDuration =
            Date.now() - hiddenAtRef.current;

          questionStartRef.current += hiddenDuration;

          hiddenAtRef.current = null;
        }
      }
    };

    document.addEventListener(
      "visibilitychange",
      handleVisibility
    );

    return () => {
      document.removeEventListener(
        "visibilitychange",
        handleVisibility
      );
    };
  }, []);

  // ───────────────────────────────────────────────────────────
  // Initial Load
  // ───────────────────────────────────────────────────────────

  useEffect(() => {
    loadQuestions();
  }, []);

  // ───────────────────────────────────────────────────────────
  // Helpers
  // ───────────────────────────────────────────────────────────

  const recordTime = (qid) => {
    const elapsed =
      Date.now() - questionStartRef.current;

    // Ignore absurd outliers
    if (elapsed > 30000) return;

    setResponseTimes((prev) => ({
      ...prev,
      [qid]: elapsed,
    }));
  };

  const moveNext = () => {
    setSelected(null);

    if (current < questions.length - 1) {
      setCurrent((prev) => prev + 1);
      questionStartRef.current = Date.now();
    }
  };

  // ───────────────────────────────────────────────────────────
  // Submit Logic
  // ───────────────────────────────────────────────────────────

  const submitAssessment = async (
    finalAnswers,
    finalTimes,
    isClarification = false
  ) => {
    try {
      setSubmitting(true);
      setError("");

      const profileRes = await axios.post(
        `${API}/submit`,
        {
          user_type: userType,
          inst_id: "frontend-web",
          mode: "fast",
          answers: finalAnswers,
          response_times_ms: finalTimes,
        }
      );

      const profile = profileRes.data;

      const overallConfidence =
        profile?.confidence?.overall ?? 1;

      // Clarification round
      if (
        !isClarification &&
        overallConfidence < LOW_CONFIDENCE_THRESHOLD
      ) {
        const clarifyRes = await axios.post(
          `${API}/clarify`,
          {
            user_type: userType,
            ocean_scores: profile.ocean_scores,
            confidences: {
              Openness:
                profile.confidence.Openness,
              Conscientiousness:
                profile.confidence
                  .Conscientiousness,
              Extraversion:
                profile.confidence
                  .Extraversion,
              Agreeableness:
                profile.confidence
                  .Agreeableness,
              Neuroticism:
                profile.confidence
                  .Neuroticism,
            },
            existing_answers: finalAnswers,
          }
        );

        const clarifyQuestions =
          clarifyRes.data
            ?.clarification_questions || [];

        if (clarifyQuestions.length > 0) {
          setClarificationMode(true);

          setQuestions(clarifyQuestions);
          setCurrent(0);

          questionStartRef.current = Date.now();

          return;
        }
      }

      onComplete(profile);
    } catch (err) {
      console.error(err?.response?.data || err);

      setError(
        "Could not submit assessment. Please retry."
      );
    } finally {
      setSubmitting(false);
    }
  };

  // ───────────────────────────────────────────────────────────
  // Answer Handling
  // ───────────────────────────────────────────────────────────

  const handleAnswer = async () => {
    if (!selected || !currentQuestion) return;

    const qid = currentQuestion.id;

    recordTime(qid);

    const updatedAnswers = {
      ...answers,
      [qid]: selected,
    };

    setAnswers(updatedAnswers);

    const updatedTimes = {
      ...responseTimes,
      [qid]:
        Date.now() - questionStartRef.current,
    };

    setResponseTimes(updatedTimes);

    const isLast =
      current === questions.length - 1;

    if (!isLast) {
      moveNext();
      return;
    }

    await submitAssessment(
      updatedAnswers,
      updatedTimes,
      clarificationMode
    );
  };

  // ───────────────────────────────────────────────────────────
  // Back
  // ───────────────────────────────────────────────────────────

  const handleBack = () => {
    if (current === 0) return;

    setCurrent((prev) => prev - 1);

    questionStartRef.current = Date.now();

    const prevQ =
      questions[current - 1];

    setSelected(
      answers[prevQ?.id] || null
    );
  };

  // ───────────────────────────────────────────────────────────
  // Loading
  // ───────────────────────────────────────────────────────────

  if (loading) {
    return (
      <div className="quiz-loading">
        Loading questions...
      </div>
    );
  }

  // ───────────────────────────────────────────────────────────
  // Error
  // ───────────────────────────────────────────────────────────

  if (error) {
    return (
      <div className="quiz-error">
        <p>{error}</p>

        <button onClick={loadQuestions}>
          Retry
        </button>
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="quiz-error">
        No questions available.
      </div>
    );
  }

  // ───────────────────────────────────────────────────────────
  // Render
  // ───────────────────────────────────────────────────────────

  return (
    <div className="quiz">
      <div className="quiz-header">
        <div className="quiz-progress-wrap">
          <div
            className="quiz-progress"
            style={{
              width: `${progress}%`,
            }}
          />
        </div>

        <div className="quiz-counter">
          Question {current + 1} /{" "}
          {questions.length}
        </div>

        {clarificationMode && (
          <div className="clarify-banner">
            Additional clarification
            questions to improve confidence.
          </div>
        )}
      </div>

      <div className="quiz-card">
        <div className="quiz-scenario">
          {currentQuestion.scenario}
        </div>

        <div className="quiz-options">
          {["A", "B", "C", "D"].map(
            (key) => (
              <button
                key={key}
                className={`quiz-option ${
                  selected === key
                    ? "selected"
                    : ""
                }`}
                onClick={() =>
                  setSelected(key)
                }
                disabled={submitting}
              >
                {
                  currentQuestion[
                    `option_${key}`
                  ]
                }
              </button>
            )
          )}
        </div>

        <div className="quiz-actions">
          <button
            onClick={handleBack}
            disabled={
              current === 0 ||
              submitting
            }
          >
            Back
          </button>

          <button
            onClick={handleAnswer}
            disabled={
              !selected || submitting
            }
          >
            {submitting
              ? "Submitting..."
              : current ===
                questions.length - 1
              ? "Finish"
              : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
}