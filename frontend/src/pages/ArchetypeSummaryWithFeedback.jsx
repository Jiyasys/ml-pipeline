// ArchetypeSummaryWithFeedback.jsx
import { useState, useCallback } from "react";
import { InsightResonanceFeedback } from "./InsightResonance";

function slugify(title) {
  return title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}

function card(extra = {}) {
  return {
    background: "var(--navy2, #0d1b2a)",
    border: "1px solid rgba(201,168,76,0.14)",
    borderRadius: "var(--radius, 14px)",
    padding: "28px",
    marginBottom: 20,
    transition: "border-color 0.2s ease",
    ...extra,
  };
}

function InsightCard({ insight, index, archetype, responseSessionId, oceanScores, userType, onFeedbackSent }) {
  const insightId = slugify(insight.title);
  const [hasFeedback, setHasFeedback] = useState(false);

  const handleFeedback = useCallback((payload) => {
    setHasFeedback(true);
    onFeedbackSent?.(insightId, payload);
  }, [insightId, onFeedbackSent]);

  return (
    <div style={{ ...card(), borderColor: hasFeedback ? "rgba(201,168,76,0.22)" : "rgba(201,168,76,0.14)" }}>
      <div style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
        <div style={{
          minWidth: 24, height: 24, borderRadius: "50%",
          background: "rgba(201,168,76,0.12)", border: "1px solid rgba(201,168,76,0.3)",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 11, color: "var(--gold, #c9a84c)", fontWeight: 700,
          marginTop: 1, flexShrink: 0,
        }}>
          {index + 1}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{
            fontSize: 14, fontWeight: 600, color: "var(--cream, #e8dcc8)",
            marginBottom: 5, fontFamily: "'DM Serif Display', serif",
          }}>
            {insight.title}
          </div>
          <p style={{ fontSize: 13, color: "var(--muted, #8899aa)", margin: 0, lineHeight: 1.75 }}>
            {insight.body}
          </p>
        </div>
      </div>

      <InsightResonanceFeedback
        insightId={insightId}
        insightTitle={insight.title}
        insightText={insight.body}
        responseSessionId={responseSessionId}
        oceanScores={oceanScores}
        archetypeKey={archetype?.key}
        userType={userType}
        onFeedbackSent={handleFeedback}
      />
    </div>
  );
}

export function ArchetypeSummaryWithFeedback({ archetype, responseSessionId, oceanScores, userType }) {
  const [feedbackLog, setFeedbackLog] = useState({});

  const handleFeedbackSent = useCallback((insightId, payload) => {
    setFeedbackLog((prev) => ({ ...prev, [insightId]: payload.feedback_level }));
  }, []);

  if (!archetype?.insights) return null;

  const respondedCount = Object.keys(feedbackLog).length;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16, paddingLeft: 2 }}>
        <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted, #8899aa)" }}>
          What this means for you
        </div>
        {respondedCount > 0 && (
          <div style={{ fontSize: 11, color: "var(--muted, #8899aa)" }}>
            {respondedCount} / {archetype.insights.length} reflected
          </div>
        )}
      </div>

      {archetype.insights.map((insight, i) => (
        <InsightCard
          key={slugify(insight.title)}
          insight={insight}
          index={i}
          archetype={archetype}
          responseSessionId={responseSessionId}
          oceanScores={oceanScores}
          userType={userType}
          onFeedbackSent={handleFeedbackSent}
        />
      ))}
    </div>
  );
}