const TRAIT_META = {
  Openness: {
    color: "#c9a84c",
    emoji: "🔭",
    low:  "Prefer familiar, structured environments",
    high: "Curious, imaginative, open to new ideas",
  },
  Conscientiousness: {
    color: "#4c9ac9",
    emoji: "📋",
    low:  "Flexible, spontaneous, go with the flow",
    high: "Organised, disciplined, goal-oriented",
  },
  Extraversion: {
    color: "#c94c7a",
    emoji: "⚡",
    low:  "Introverted, reflective, energised by solitude",
    high: "Outgoing, energised by people and action",
  },
  Agreeableness: {
    color: "#4cc97a",
    emoji: "🤝",
    low:  "Analytical, direct, prioritise logic over harmony",
    high: "Cooperative, empathetic, values relationships",
  },
  Neuroticism: {
    color: "#9a4cc9",
    emoji: "🌊",
    low:  "Emotionally stable, calm under pressure",
    high: "Emotionally sensitive, deeply reactive",
  },
};

const TRAIT_ORDER = [
  "Openness",
  "Conscientiousness",
  "Extraversion",
  "Agreeableness",
  "Neuroticism",
];

function ScoreBar({ score, color }) {
  return (
    <div className="ocean-bar-wrap">
      <div
        className="ocean-bar-fill"
        style={{ width: `${score}%`, background: color }}
      />
    </div>
  );
}

export default function Results({ profile, onRetake }) {
  if (!profile) return null;

  const { ocean_scores, mbti_display, confidence } = profile;
  const overallConf = Math.round((confidence?.overall || 0) * 100);

  return (
    <div className="results">
      {/* Header */}
      <div className="results-header">
        <div className="section-eyebrow">Your Personality Profile</div>

        <div className="mbti-badge">{mbti_display}</div>

        <h2 className="results-title">Assessment Complete</h2>
        <p className="results-sub">
          Based on your scenario responses across 5 personality dimensions
        </p>

        {/* Confidence */}
        <div className="confidence-bar-wrap">
          <div className="confidence-label">
            <span>Profile confidence</span>
            <span style={{ color: "var(--gold)" }}>{overallConf}%</span>
          </div>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{ width: `${overallConf}%` }}
            />
          </div>
          {profile.needs_clarification && (
            <p style={{
              fontSize: 12, color: "var(--muted)",
              marginTop: 8, fontStyle: "italic", textAlign: "center"
            }}>
              Consider a follow-up assessment for higher accuracy
            </p>
          )}
        </div>
      </div>

      {/* OCEAN Cards */}
      <div className="ocean-grid">
        {TRAIT_ORDER.map((trait, i) => {
          const score = ocean_scores[trait] ?? 50;
          const meta  = TRAIT_META[trait];
          const desc  = score >= 50 ? meta.high : meta.low;

          return (
            <div
              key={trait}
              className="ocean-card"
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <div style={{ fontSize: 24, marginBottom: 10 }}>{meta.emoji}</div>
              <div className="ocean-trait">{trait}</div>
              <div className="ocean-score" style={{ color: meta.color }}>
                {score}
              </div>
              <ScoreBar score={score} color={meta.color} />
              <div className="ocean-subdim">{desc}</div>
            </div>
          );
        })}
      </div>

      {/* MBTI explainer */}
      <div style={{
        background: "var(--navy2)",
        border: "1px solid rgba(201,168,76,0.12)",
        borderRadius: "var(--radius-lg)",
        padding: "28px 32px",
        marginBottom: 24,
      }}>
        <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 12 }}>
          MBTI-Style Profile
        </div>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          {[
            { letter: mbti_display[0], meaning: mbti_display[0] === "E" ? "Extraverted" : "Introverted" },
            { letter: mbti_display[1], meaning: mbti_display[1] === "N" ? "Intuitive" : "Sensing" },
            { letter: mbti_display[2], meaning: mbti_display[2] === "F" ? "Feeling" : "Thinking" },
            { letter: mbti_display[3], meaning: mbti_display[3] === "J" ? "Judging" : "Perceiving" },
          ].map(({ letter, meaning }) => (
            <div key={letter} style={{
              display: "flex", alignItems: "center", gap: 8,
              background: "rgba(201,168,76,0.06)",
              border: "1px solid rgba(201,168,76,0.15)",
              borderRadius: 8, padding: "8px 16px",
            }}>
              <span style={{
                fontFamily: "'DM Serif Display', serif",
                fontSize: 22, color: "var(--gold)",
              }}>{letter}</span>
              <span style={{ fontSize: 13, color: "var(--muted)" }}>{meaning}</span>
            </div>
          ))}
        </div>
        <p style={{ fontSize: 12, color: "var(--muted)", marginTop: 14, fontStyle: "italic" }}>
          MBTI label is derived from your OCEAN scores for display purposes. Your full profile above is more accurate.
        </p>
      </div>

      {/* Raw data toggle */}
      <details style={{ marginBottom: 24 }}>
        <summary style={{
          cursor: "pointer", fontSize: 13, color: "var(--muted)",
          padding: "12px 0", listStyle: "none",
        }}>
          View raw profile data ↓
        </summary>
        <pre style={{
          marginTop: 12,
          background: "var(--navy2)",
          border: "1px solid rgba(201,168,76,0.1)",
          borderRadius: "var(--radius)",
          padding: 20,
          fontSize: 12,
          color: "var(--cream2)",
          overflow: "auto",
          lineHeight: 1.7,
        }}>
          {JSON.stringify(profile, null, 2)}
        </pre>
      </details>

      {/* Actions */}
      <div className="results-actions">
        <button className="btn-ghost" onClick={onRetake}>
          ← Retake Assessment
        </button>
        <button
          className="btn-primary"
          onClick={() => {
            const blob = new Blob([JSON.stringify(profile, null, 2)], { type: "application/json" });
            const url  = URL.createObjectURL(blob);
            const a    = document.createElement("a");
            a.href     = url;
            a.download = `edwiserr_profile_${mbti_display}.json`;
            a.click();
          }}
        >
          Download Profile
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M8 2v8M4 7l4 4 4-4M2 13h12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
}