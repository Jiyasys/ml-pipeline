const TRAIT_META = {
  Openness:          { color: "#c9a84c", emoji: "🔭", low: "Prefer familiar, structured environments", high: "Curious, imaginative, open to new ideas" },
  Conscientiousness: { color: "#4c9ac9", emoji: "📋", low: "Flexible, spontaneous, go with the flow",    high: "Organised, disciplined, goal-oriented" },
  Extraversion:      { color: "#c94c7a", emoji: "⚡", low: "Introverted, energised by solitude",          high: "Outgoing, energised by people and action" },
  Agreeableness:     { color: "#4cc97a", emoji: "🤝", low: "Analytical, direct, logic over harmony",      high: "Cooperative, empathetic, values relationships" },
  Neuroticism:       { color: "#9a4cc9", emoji: "🌊", low: "Emotionally stable, calm under pressure",     high: "Emotionally sensitive, deeply reactive" },
};
const TRAIT_ORDER = ["Openness","Conscientiousness","Extraversion","Agreeableness","Neuroticism"];

const card = {
  background:   "var(--navy2)",
  border:       "1px solid rgba(201,168,76,0.1)",
  borderRadius: "var(--radius)",
  padding:      "24px",
  marginBottom: 16,
};

function Bar({ pct, color = "var(--gold)", height = 3 }) {
  return (
    <div style={{ height, background: "rgba(201,168,76,0.1)", borderRadius: 2, overflow: "hidden" }}>
      <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: 2, transition: "width 1.2s ease" }} />
    </div>
  );
}

function PillarRow({ label, score, detail }) {
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 6 }}>
        <span style={{ color: "var(--cream2)" }}>{label}</span>
        <span style={{ color: "var(--gold)", fontWeight: 500 }}>{Math.round(score * 100)}%</span>
      </div>
      <Bar pct={score * 100} />
      {detail && <p style={{ fontSize: 11, color: "var(--muted)", marginTop: 4, fontStyle: "italic" }}>{detail}</p>}
    </div>
  );
}

export default function Results({ profile, onRetake }) {
  if (!profile) return null;

  const { ocean_scores, mbti_display, confidence, questions_answered } = profile;
  const overall = confidence?.overall ?? 0;
  const p1      = confidence?.pillar_1 ?? {};
  const p2      = confidence?.pillar_2 ?? {};
  const p3      = confidence?.pillar_3 ?? {};

  // Behavioral flags for display
  const rtFlags  = p2.rt_flags  ?? 0;
  const maxRun   = p2.max_run   ?? 0;
  const irv      = p2.irv       ?? 0;

  return (
    <div className="results">

      {/* ── Header ─────────────────────────────────────────── */}
      <div className="results-header">
        <div className="section-eyebrow">Your Personality Profile</div>
        <div className="mbti-badge">{mbti_display}</div>
        <h2 className="results-title">Assessment Complete</h2>
        <p className="results-sub">{questions_answered} questions across 5 personality dimensions</p>

        <div className="confidence-bar-wrap" style={{ marginTop: 24 }}>
          <div className="confidence-label">
            <span>Overall confidence</span>
            <span style={{ color: overall >= 0.75 ? "var(--gold)" : "var(--danger)" }}>
              {Math.round(overall * 100)}%
              {overall < 0.75 && " ⚠ low"}
            </span>
          </div>
          <div className="confidence-bar">
            <div className="confidence-fill" style={{ width: `${overall * 100}%` }} />
          </div>
        </div>
      </div>

      {/* ── OCEAN Cards ────────────────────────────────────── */}
      <div className="ocean-grid">
        {TRAIT_ORDER.map((trait, i) => {
          const score = ocean_scores[trait] ?? 50;
          const meta  = TRAIT_META[trait];
          const conf  = confidence?.per_trait?.[trait];
          return (
            <div key={trait} className="ocean-card" style={{ animationDelay: `${i * 0.1}s` }}>
              <div style={{ fontSize: 22, marginBottom: 8 }}>{meta.emoji}</div>
              <div className="ocean-trait">{trait}</div>
              <div className="ocean-score" style={{ color: meta.color }}>{score}</div>
              <Bar pct={score} color={meta.color} />
              <div className="ocean-subdim">{score >= 50 ? meta.high : meta.low}</div>
              {conf !== undefined && (
                <div style={{ fontSize: 11, color: "var(--muted)", marginTop: 8 }}>
                  confidence {Math.round(conf * 100)}%
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* ── Confidence Breakdown ───────────────────────────── */}
      <div style={card}>
        <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 20 }}>
          Confidence Breakdown
        </div>

        {/* Pillar 1 */}
        <div style={{ marginBottom: 20 }}>
          <div style={{ fontSize: 13, color: "var(--gold)", marginBottom: 12, fontWeight: 500 }}>
            P1 — {p1.label ?? "Internal Consistency"}
          </div>
          {TRAIT_ORDER.map(trait => (
            <PillarRow
              key={trait}
              label={trait}
              score={p1.scores?.[trait] ?? 0.5}
              detail={`α = ${p1.alphas?.[trait] ?? "—"}`}
            />
          ))}
        </div>

        {/* Divider */}
        <div style={{ height: 1, background: "rgba(201,168,76,0.08)", margin: "16px 0" }} />

        {/* Pillar 2 */}
        <div style={{ marginBottom: 20 }}>
          <div style={{ fontSize: 13, color: "var(--gold)", marginBottom: 12, fontWeight: 500 }}>
            P2 — {p2.label ?? "Behavioral Quality"}
          </div>
          <PillarRow label="Response time quality"  score={p2.rt_score  ?? 0.5} detail={`${rtFlags} flagged responses`} />
          <PillarRow label="Straight-lining check"  score={p2.str_score ?? 0.5} detail={`Longest same-option run: ${maxRun}`} />
          <PillarRow label="Response variability"   score={p2.irv_score ?? 0.5} detail={`IRV = ${irv.toFixed(2)} (higher = more varied)`} />
        </div>

        {/* Divider */}
        <div style={{ height: 1, background: "rgba(201,168,76,0.08)", margin: "16px 0" }} />

        {/* Pillar 3 */}
        <div>
          <div style={{ fontSize: 13, color: "var(--muted)", marginBottom: 12, fontWeight: 500 }}>
            P3 — {p3.label ?? "Statistical Stability"}
          </div>
          <div style={{ fontSize: 12, color: "var(--muted)", fontStyle: "italic" }}>
            {p3.note ?? "Pending calibration data"}
          </div>
        </div>
      </div>

      {/* ── MBTI Label ─────────────────────────────────────── */}
      <div style={card}>
        <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 16 }}>
          MBTI-Style Profile
        </div>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          {[
            { l: mbti_display[0], m: mbti_display[0] === "E" ? "Extraverted"  : "Introverted" },
            { l: mbti_display[1], m: mbti_display[1] === "N" ? "Intuitive"    : "Sensing"     },
            { l: mbti_display[2], m: mbti_display[2] === "F" ? "Feeling"      : "Thinking"    },
            { l: mbti_display[3], m: mbti_display[3] === "J" ? "Judging"      : "Perceiving"  },
          ].map(({ l, m }) => (
            <div key={l} style={{
              display: "flex", alignItems: "center", gap: 8,
              background: "rgba(201,168,76,0.06)",
              border: "1px solid rgba(201,168,76,0.15)",
              borderRadius: 8, padding: "8px 16px",
            }}>
              <span style={{ fontFamily: "'DM Serif Display',serif", fontSize: 22, color: "var(--gold)" }}>{l}</span>
              <span style={{ fontSize: 13, color: "var(--muted)" }}>{m}</span>
            </div>
          ))}
        </div>
        <p style={{ fontSize: 11, color: "var(--muted)", marginTop: 12, fontStyle: "italic" }}>
          Derived from OCEAN scores for display only. Your full profile above is more accurate.
        </p>
      </div>

      {/* ── Raw Data ───────────────────────────────────────── */}
      <details style={{ marginBottom: 24 }}>
        <summary style={{ cursor: "pointer", fontSize: 13, color: "var(--muted)", padding: "12px 0", listStyle: "none" }}>
          View raw profile JSON ↓
        </summary>
        <pre style={{
          marginTop: 12,
          background: "var(--navy2)",
          border: "1px solid rgba(201,168,76,0.1)",
          borderRadius: "var(--radius)",
          padding: 20, fontSize: 11,
          color: "var(--cream2)", overflow: "auto", lineHeight: 1.7,
        }}>
          {JSON.stringify(profile, null, 2)}
        </pre>
      </details>

      {/* ── Actions ────────────────────────────────────────── */}
      <div className="results-actions">
        <button className="btn-ghost" onClick={onRetake}>← Retake Assessment</button>
        <button className="btn-primary" onClick={() => {
          const blob = new Blob([JSON.stringify(profile, null, 2)], { type: "application/json" });
          const a    = document.createElement("a");
          a.href     = URL.createObjectURL(blob);
          a.download = `edwiserr_${mbti_display}.json`;
          a.click();
        }}>
          Download Profile
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M8 2v8M4 7l4 4 4-4M2 13h12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>

    </div>
  );
}