import { useEffect, useMemo, useRef, useState, useCallback } from "react";
import axios from "axios";

const BASE = import.meta.env.VITE_API_URL;
const API = `${BASE}/personality`;
const SESSIONS = `${BASE}/sessions`;

const QUIZ_MODE = "fast";
const LOW_CONFIDENCE_THRESHOLD = 0.65;

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function randomSeed() {
  return Math.floor(Math.random() * 1_000_000);
}

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

  const sessionIdRef = useRef(null);
  // Promise that resolves once the session is created
  // So submit can wait for it without blocking question loading
  const sessionPromiseRef = useRef(null);
  const sessionSeedRef = useRef(randomSeed());
  const questionStartRef = useRef(Date.now());
  const hiddenAtRef = useRef(null);
  const loadedRef = useRef(false);

  const currentQuestion = questions[current] ?? null;

  const progress = useMemo(() => {
    if (!questions.length) return 0;
    return ((current + 1) / questions.length) * 100;
  }, [current, questions.length]);

  useEffect(() => {
    setSelected(answers[questions[current]?.id] ?? null);
  }, [current]); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Visibility tracking ───────────────────────────────────────────────────
  useEffect(() => {
    const handleVisibility = () => {
      if (document.hidden) {
        hiddenAtRef.current = Date.now();
      } else if (hiddenAtRef.current) {
        questionStartRef.current += Date.now() - hiddenAtRef.current;
        hiddenAtRef.current = null;
      }
    };
    document.addEventListener("visibilitychange", handleVisibility);
    return () => document.removeEventListener("visibilitychange", handleVisibility);
  }, []);

  // ── Create DB session — starts in background, stores a Promise ────────────
  // Quiz loads immediately. Submit awaits this Promise before saving answers.
  const createSession = useCallback(() => {
    sessionPromiseRef.current = axios.post(SESSIONS, {
      student_identifier: `anon-${Date.now()}`,
    })
      .then(res => {
        sessionIdRef.current = res.data.id;
        console.log("[Quiz] session created:", sessionIdRef.current);
        return res.data.id;
      })
      .catch(err => {
        console.warn("[Quiz] session create failed (non-fatal):", err?.response?.data || err);
        return null;
      });
  }, []);

  // ── Save answers — waits for session Promise first ────────────────────────
    // Wait for session to finish creating (usually already done by submit time)
    const saveAnswersToDB = useCallback(async (answersMap) => {
        console.log("[DB] sessionPromiseRef:", sessionPromiseRef.current);
        console.log("[DB] sessionIdRef:", sessionIdRef.current);
        console.log("[DB] answersMap keys:", Object.keys(answersMap).length);
  
        const sessionId = await sessionPromiseRef.current;
        console.log("[DB] sessionId after await:", sessionId);
        if (!sessionId) return;

    const answers = Object.entries(answersMap).map(([question_set_id, selected_answer]) => ({
      question_set_id,
      selected_answer,
    }));

    axios.post(`${SESSIONS}/${sessionId}/answers`, { answers })
      .then(() => console.log("[Quiz] saved", answers.length, "answers"))
      .catch(err => console.warn("[Quiz] save answers failed:", err?.response?.data || err));
  }, []);

  // ── Mark session submitted ────────────────────────────────────────────────
  const markSubmitted = useCallback(async () => {
    const sessionId = await sessionPromiseRef.current;
    if (!sessionId) return;

    axios.post(`${SESSIONS}/${sessionId}/submit`)
      .then(() => console.log("[Quiz] session submitted:", sessionId))
      .catch(err => console.warn("[Quiz] mark submitted failed:", err?.response?.data || err));
  }, []);

  // ── Load questions — fast, session starts in background ──────────────────
  const loadQuestions = useCallback(async () => {
    try {
      setLoading(true);
      setError("");
      sessionSeedRef.current = randomSeed();

      const res = await axios.post(`${API}/questions`, {
        user_type: userType,
        inst_id: "frontend-web",
        mode: QUIZ_MODE,
        seed: sessionSeedRef.current,
      });

      const raw = res.data.questions || [];
      if (raw.length === 0) {
        setError("No questions returned from server.");
        return;
      }

      setQuestions(shuffle(raw));
      setCurrent(0);
      setAnswers({});
      setResponseTimes({});
      setSelected(null);
      questionStartRef.current = Date.now();

      // Start session creation in background — stores a Promise
      createSession();

    } catch (err) {
      console.error("[Quiz] load error:", err?.response?.data || err);
      setError("Could not load questions. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [userType, createSession]);

  useEffect(() => {
    if (loadedRef.current) return;
    loadedRef.current = true;
    loadQuestions();
  }, [loadQuestions]);

  // ── Submit ────────────────────────────────────────────────────────────────
  const submitAssessment = useCallback(async (finalAnswers, finalTimes, isClarification = false) => {
    try {
      setSubmitting(true);
      setError("");

      // Run scoring + DB saves concurrently
      // saveAnswersToDB awaits session Promise internally — no race condition
      const [profileRes] = await Promise.all([
        axios.post(`${API}/submit`, {
          user_type: userType,
          inst_id: "frontend-web",
          mode: QUIZ_MODE,
          answers: finalAnswers,
          response_times_ms: finalTimes,
        }),
        saveAnswersToDB(finalAnswers),
        markSubmitted(),
      ]);

      const profile = profileRes.data;
      const overallConfidence = profile?.confidence?.overall ?? 1;

      profile.response_session_id = sessionIdRef.current ?? null;

      if (!isClarification && overallConfidence < LOW_CONFIDENCE_THRESHOLD) {
        try {
          const clarifyRes = await axios.post(`${API}/clarify`, {
            user_type: userType,
            ocean_scores: profile.ocean_scores,
            confidences: {
              Openness: profile.confidence?.Openness ?? 1,
              Conscientiousness: profile.confidence?.Conscientiousness ?? 1,
              Extraversion: profile.confidence?.Extraversion ?? 1,
              Agreeableness: profile.confidence?.Agreeableness ?? 1,
              Neuroticism: profile.confidence?.Neuroticism ?? 1,
            },
            existing_answers: finalAnswers,
          });

          const clarifyQs = clarifyRes.data?.clarification_questions || [];
          if (clarifyQs.length > 0) {
            setClarificationMode(true);
            setQuestions(clarifyQs);
            setCurrent(0);
            setSelected(null);
            questionStartRef.current = Date.now();
            return;
          }
        } catch (clarifyErr) {
          console.warn("[Quiz] clarification failed, proceeding:", clarifyErr);
        }
      }

      onComplete(profile);
    } catch (err) {
      console.error("[Quiz] submit error:", err?.response?.data || err);
      const detail = err?.response?.data?.detail;
      setError(
        typeof detail === "string"
          ? `Submission failed: ${detail}`
          : "Could not submit. Please retry."
      );
    } finally {
      setSubmitting(false);
    }
  }, [userType, onComplete, saveAnswersToDB, markSubmitted]);

  // ── Answer ────────────────────────────────────────────────────────────────
  const handleAnswer = useCallback(async () => {
    if (!selected || !currentQuestion || submitting) return;

    const qid = currentQuestion.id;
    const elapsed = Math.min(Date.now() - questionStartRef.current, 30000);

    const updatedAnswers = { ...answers, [qid]: selected };
    const updatedTimes = { ...responseTimes, [qid]: elapsed };

    setAnswers(updatedAnswers);
    setResponseTimes(updatedTimes);

    if (current < questions.length - 1) {
      setCurrent((prev) => prev + 1);
      questionStartRef.current = Date.now();
      return;
    }

    await submitAssessment(updatedAnswers, updatedTimes, clarificationMode);
  }, [
    selected, currentQuestion, submitting, answers, responseTimes,
    current, questions.length, clarificationMode, submitAssessment,
  ]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleBack = useCallback(() => {
    if (current === 0 || submitting) return;
    setCurrent((prev) => prev - 1);
    questionStartRef.current = Date.now();
  }, [current, submitting]);

  const handleRetry = useCallback(() => {
    loadedRef.current = false;
    sessionIdRef.current = null;
    sessionPromiseRef.current = null;
    loadQuestions();
  }, [loadQuestions]);

  if (loading) return <div className="quiz-loading">Loading questions…</div>;
  if (error) return <div className="quiz-error"><p>{error}</p><button onClick={handleRetry}>Retry</button></div>;
  if (!currentQuestion) return <div className="quiz-error">No questions available.</div>;

  return (
    <div className="quiz">
      <div className="quiz-header">
        <div className="quiz-progress-wrap">
          <div className="quiz-progress" style={{ width: `${progress}%` }} />
        </div>
        <div className="quiz-counter">Question {current + 1} / {questions.length}</div>
        {clarificationMode && (
          <div className="clarify-banner">A few extra questions to sharpen your results.</div>
        )}
      </div>

      <div className="quiz-card">
        <div className="quiz-topic">{currentQuestion.trait}</div>
        <div className="quiz-subtopic">{currentQuestion.sub_dimension}</div>
        <div className="quiz-scenario">{currentQuestion.scenario}</div>

        <div className="quiz-options">
          {["A", "B", "C", "D"].map((key) => (
            <button
              key={key}
              className={`quiz-option${selected === key ? " selected" : ""}`}
              onClick={() => !submitting && setSelected(key)}
              disabled={submitting}
            >
              {currentQuestion[`option_${key}`]}
            </button>
          ))}
        </div>

        <div className="quiz-actions">
          <button onClick={handleBack} disabled={current === 0 || submitting}>Back</button>
          <button onClick={handleAnswer} disabled={!selected || submitting}>
            {submitting ? "Submitting…" : current === questions.length - 1 ? "Finish" : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
}