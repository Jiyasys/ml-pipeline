// InsightResonance.jsx
import { useState, useCallback, useRef } from "react";
import axios from "axios";

const BASE = import.meta.env.VITE_API_URL;

async function submitResonanceFeedback(payload) {
  // CORRECT
const response = await axios.post(
  `${BASE}/insights/feedback`,
  payload,
  { timeout: 8000 }
);
  return response.data;
}

const RESONANCE_OPTIONS = [
  {
    value: "strongly_resonates",
    label: "Strongly Resonates",
    icon: "◎",
    activeColor: "#c9a84c",
    activeBg: "rgba(201,168,76,0.12)",
    activeBorder: "rgba(201,168,76,0.45)",
  },
  {
    value: "somewhat_resonates",
    label: "Somewhat",
    icon: "◑",
    activeColor: "#4c9ac9",
    activeBg: "rgba(76,154,201,0.10)",
    activeBorder: "rgba(76,154,201,0.35)",
  },
  {
    value: "doesnt_feel_accurate",
    label: "Doesn't Feel Accurate",
    icon: "○",
    activeColor: "#8899aa",
    activeBg: "rgba(136,153,170,0.08)",
    activeBorder: "rgba(136,153,170,0.30)",
  },
];

export function InsightResonanceFeedback({
  insightId,
  insightTitle,
  insightText,
  responseSessionId,
  oceanScores,
  archetypeKey,
  userType,
  onFeedbackSent,
}) {
  const [selected, setSelected]   = useState(null);
  const [expanded, setExpanded]   = useState(false);
  const [textValue, setTextValue] = useState("");
  const [status, setStatus]       = useState("idle"); // idle | submitting | done | error
  const [submitted, setSubmitted] = useState(false);
  const textareaRef = useRef(null);

  const handleOptionClick = useCallback((value) => {
    if (submitted) return;
    setSelected(value);
    if (value === "doesnt_feel_accurate") setExpanded(true);
  }, [submitted]);

  const handleSubmit = useCallback(async () => {
    if (!selected || submitted || status === "submitting") return;

    const payload = {
      response_session_id: responseSessionId,
      insight_id:          insightId,
      insight_title:       insightTitle,
      insight_text:        insightText,
      feedback_level:      selected,
      feedback_text:       textValue.trim() || null,
      ocean_scores:        oceanScores,
      archetype_key:       archetypeKey,
      user_type:           userType ?? null,
      submitted_at:        new Date().toISOString(),
    };

    setStatus("submitting");

    try {
      await submitResonanceFeedback(payload);
      setStatus("done");
      setSubmitted(true);
      onFeedbackSent?.(payload);
    } catch (err) {
      console.error("[InsightResonance] submit error:", err?.response?.data || err.message);
      setStatus("error");
    }
  }, [selected, submitted, status, textValue, insightId, insightTitle, insightText,
      responseSessionId, oceanScores, archetypeKey, userType, onFeedbackSent]);

  if (submitted && status === "done") {
    return <ResonanceConfirmation selected={selected} />;
  }

  return (
    <div style={styles.wrapper}>
      <div style={styles.question}>Did this resonate with you?</div>

      <div style={styles.optionRow}>
        {RESONANCE_OPTIONS.map((opt) => {
          const isActive = selected === opt.value;
          return (
            <button
              key={opt.value}
              onClick={() => handleOptionClick(opt.value)}
              disabled={submitted}
              aria-pressed={isActive}
              style={{
                ...styles.optionBtn,
                ...(isActive ? {
                  color: opt.activeColor,
                  background: opt.activeBg,
                  borderColor: opt.activeBorder,
                } : {}),
              }}
            >
              <span style={styles.optionIcon}>{opt.icon}</span>
              <span style={styles.optionLabel}>{opt.label}</span>
            </button>
          );
        })}
      </div>

      {selected && !submitted && (
        <div style={styles.expandArea}>
          {!expanded ? (
            <button
              onClick={() => {
                setExpanded(true);
                setTimeout(() => textareaRef.current?.focus(), 80);
              }}
              style={styles.addNoteBtn}
            >
              + Add a note <span style={{ opacity: 0.5, fontSize: 11 }}>(optional)</span>
            </button>
          ) : (
            <div style={styles.textareaWrapper}>
              <textarea
                ref={textareaRef}
                value={textValue}
                onChange={(e) => setTextValue(e.target.value)}
                placeholder="Share what felt accurate or what missed the mark…"
                rows={3}
                maxLength={500}
                style={styles.textarea}
              />
              <div style={styles.charCount}>{textValue.length}/500</div>
            </div>
          )}

          <button
            onClick={handleSubmit}
            disabled={status === "submitting"}
            style={{ ...styles.submitBtn, opacity: status === "submitting" ? 0.6 : 1 }}
          >
            {status === "submitting" ? (
              <span style={styles.submittingInner}>
                <span style={styles.spinnerDot} /> Saving…
              </span>
            ) : "Save reflection"}
          </button>

          {status === "error" && (
            <p style={styles.errorMsg}>Couldn't save — try again in a moment.</p>
          )}
        </div>
      )}
    </div>
  );
}

function ResonanceConfirmation({ selected }) {
  const labels = {
    strongly_resonates:   "Noted — this felt accurate.",
    somewhat_resonates:   "Noted — partially aligned.",
    doesnt_feel_accurate: "Noted — we'll use this to improve.",
  };
  return (
    <div style={styles.confirmWrapper}>
      <span style={styles.confirmDot}>✓</span>
      <span style={styles.confirmText}>{labels[selected] ?? "Reflection saved."}</span>
    </div>
  );
}

const styles = {
  wrapper: {
    marginTop: 20,
    paddingTop: 18,
    borderTop: "1px solid rgba(201,168,76,0.08)",
  },
  question: {
    fontSize: 12,
    color: "var(--muted, #8899aa)",
    marginBottom: 12,
    letterSpacing: "0.02em",
  },
  optionRow: {
    display: "flex",
    gap: 8,
    flexWrap: "wrap",
  },
  optionBtn: {
    display: "flex",
    alignItems: "center",
    gap: 6,
    padding: "6px 14px",
    background: "transparent",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: 999,
    cursor: "pointer",
    fontSize: 12,
    color: "var(--cream2, #c8d4e0)",
    transition: "all 0.18s ease",
    outline: "none",
    whiteSpace: "nowrap",
  },
  optionIcon: { fontSize: 13, lineHeight: 1 },
  optionLabel: { fontFamily: "'DM Sans', sans-serif" },
  expandArea: {
    marginTop: 12,
    display: "flex",
    flexDirection: "column",
    gap: 10,
    alignItems: "flex-start",
  },
  addNoteBtn: {
    background: "transparent",
    border: "none",
    cursor: "pointer",
    fontSize: 12,
    color: "var(--muted, #8899aa)",
    padding: 0,
    transition: "color 0.15s",
  },
  textareaWrapper: { width: "100%", position: "relative" },
  textarea: {
    width: "100%",
    background: "rgba(255,255,255,0.03)",
    border: "1px solid rgba(201,168,76,0.15)",
    borderRadius: 10,
    padding: "10px 14px",
    fontSize: 13,
    color: "var(--cream2, #c8d4e0)",
    resize: "vertical",
    outline: "none",
    lineHeight: 1.65,
    boxSizing: "border-box",
    fontFamily: "inherit",
  },
  charCount: {
    fontSize: 10,
    color: "var(--muted, #8899aa)",
    textAlign: "right",
    marginTop: 4,
  },
  submitBtn: {
    background: "rgba(201,168,76,0.10)",
    border: "1px solid rgba(201,168,76,0.28)",
    borderRadius: 8,
    padding: "7px 18px",
    fontSize: 12,
    color: "var(--gold, #c9a84c)",
    cursor: "pointer",
    transition: "all 0.18s",
    letterSpacing: "0.03em",
  },
  submittingInner: { display: "flex", alignItems: "center", gap: 7 },
  spinnerDot: {
    display: "inline-block",
    width: 8,
    height: 8,
    borderRadius: "50%",
    border: "1.5px solid rgba(201,168,76,0.4)",
    borderTopColor: "var(--gold, #c9a84c)",
    animation: "edwiserrSpin 0.7s linear infinite",
  },
  errorMsg: { fontSize: 12, color: "#c94c4c", margin: 0 },
  confirmWrapper: {
    marginTop: 16,
    paddingTop: 14,
    borderTop: "1px solid rgba(201,168,76,0.08)",
    display: "flex",
    alignItems: "center",
    gap: 8,
  },
  confirmDot: { fontSize: 13, color: "var(--gold, #c9a84c)" },
  confirmText: { fontSize: 12, color: "var(--muted, #8899aa)", fontStyle: "italic" },
};