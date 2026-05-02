import { useState, useEffect } from "react";
import axios from "axios";
import PersonalityCard from "./PersonalityCard";

const API = "http://127.0.0.1:8000/api";

const TRAIT_META = {
  Openness:          { color: "#c9a84c", emoji: "🔭", low: "Prefer familiar, structured environments", high: "Curious, imaginative, open to new ideas" },
  Conscientiousness: { color: "#4c9ac9", emoji: "📋", low: "Flexible, spontaneous, go with the flow",    high: "Organised, disciplined, goal-oriented" },
  Extraversion:      { color: "#c94c7a", emoji: "⚡", low: "Introverted, energised by solitude",          high: "Outgoing, energised by people and action" },
  Agreeableness:     { color: "#4cc97a", emoji: "🤝", low: "Analytical, direct, logic over harmony",      high: "Cooperative, empathetic, values relationships" },
  Neuroticism:       { color: "#9a4cc9", emoji: "🌊", low: "Emotionally stable, calm under pressure",     high: "Emotionally sensitive, deeply reactive" },
};
const TRAIT_ORDER   = ["Openness","Conscientiousness","Extraversion","Agreeableness","Neuroticism"];
const SOURCE_LABELS = { onet: "Global", indian: "India", hybrid: "Hybrid" };
const SOURCE_COLORS = { onet: "#4c9ac9", indian: "#c9a84c", hybrid: "#4cc97a" };

function Bar({ pct, color = "var(--gold)", height = 3 }) {
  return (
    <div style={{ height, background: "rgba(201,168,76,0.1)", borderRadius: 2, overflow: "hidden" }}>
      <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: 2, transition: "width 1.2s ease" }} />
    </div>
  );
}

function card(extra = {}) {
  return {
    background: "var(--navy2)",
    border: "1px solid rgba(201,168,76,0.1)",
    borderRadius: "var(--radius)",
    padding: "24px",
    marginBottom: 16,
    ...extra,
  };
}

export default function Results({ profile, onViewCareers, onRetake }) {
  const [topCareers, setTopCareers] = useState([]);
  const [careerLoad, setCareerLoad] = useState(true);

  useEffect(() => {
    if (!profile?.ocean_scores) return;
    axios.post(`${API}/careers/recommend`, {
      ocean_scores:  profile.ocean_scores,
      user_type:     profile.user_type,
      top_n:         3,
      min_fit_score: 60,
    })
    .then(r => { setTopCareers(r.data.recommendations || []); setCareerLoad(false); })
    .catch(() => setCareerLoad(false));
  }, [profile]);

  if (!profile) return null;

  const { ocean_scores, mbti_display, confidence, questions_answered } = profile;
  const overall = confidence?.overall ?? 0;
  const p1      = confidence?.pillar_1 ?? {};
  const p2      = confidence?.pillar_2 ?? {};
  const p3      = confidence?.pillar_3 ?? {};

  return (
    <div className="results">

      {/* ── Header ─────────────────────────────────────────── */}
      <div className="results-header">
        <div className="section-eyebrow">Your Personality Profile</div>
        <div className="mbti-badge">{mbti_display}</div>
        <h2 className="results-title">Assessment Complete</h2>
        <p className="results-sub">{questions_answered} questions · 5 personality dimensions</p>

        <div className="confidence-bar-wrap" style={{ marginTop: 24 }}>
          <div className="confidence-label">
            <span>Profile confidence</span>
            <span style={{ color: overall >= 0.75 ? "var(--gold)" : "var(--danger)" }}>
              {Math.round(overall * 100)}%{overall < 0.75 ? " ⚠" : ""}
            </span>
          </div>
          <div className="confidence-bar">
            <div className="confidence-fill" style={{ width: `${overall * 100}%` }} />
          </div>
          {profile.needs_clarification && (
            <p style={{ fontSize: 12, color: "var(--muted)", marginTop: 6, fontStyle: "italic", textAlign: "center" }}>
              Consider a follow-up assessment for higher accuracy
            </p>
          )}
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

      {/* ── MBTI Label ─────────────────────────────────────── */}
      <div style={card()}>
        <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 16 }}>
          MBTI-Style Profile
        </div>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          {[
            { l: mbti_display[0], m: mbti_display[0] === "E" ? "Extraverted" : "Introverted" },
            { l: mbti_display[1], m: mbti_display[1] === "N" ? "Intuitive"   : "Sensing"     },
            { l: mbti_display[2], m: mbti_display[2] === "F" ? "Feeling"     : "Thinking"    },
            { l: mbti_display[3], m: mbti_display[3] === "J" ? "Judging"     : "Perceiving"  },
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
          Derived from OCEAN scores for display only.
        </p>
      </div>

      {/* ── Personality Summary Card ────────────────────────── */}
      <PersonalityCard mbtiType={mbti_display} />

      {/* ── Confidence Breakdown ───────────────────────────── */}
      <div style={card()}>
        <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 20 }}>
          Confidence Breakdown
        </div>

        {/* P1 */}
        <div style={{ marginBottom: 18 }}>
          <div style={{ fontSize: 13, color: "var(--gold)", marginBottom: 12, fontWeight: 500 }}>
            P1 — {p1.label ?? "Internal Consistency"}
          </div>
          {TRAIT_ORDER.map(trait => (
            <div key={trait} style={{ marginBottom: 10 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 5 }}>
                <span style={{ color: "var(--cream2)" }}>{trait}</span>
                <span style={{ color: "var(--gold)" }}>
                  α={p1.alphas?.[trait] ?? "—"}  {Math.round((p1.scores?.[trait] ?? 0) * 100)}%
                </span>
              </div>
              <Bar pct={(p1.scores?.[trait] ?? 0) * 100} />
            </div>
          ))}
        </div>

        <div style={{ height: 1, background: "rgba(201,168,76,0.08)", margin: "16px 0" }} />

        {/* P2 */}
        <div style={{ marginBottom: 18 }}>
          <div style={{ fontSize: 13, color: "var(--gold)", marginBottom: 12, fontWeight: 500 }}>
            P2 — {p2.label ?? "Behavioral Quality"}
          </div>
          {[
            { label: "Response time",   score: p2.rt_score  ?? 0.5, detail: `${p2.rt_flags ?? 0} flagged`         },
            { label: "Straight-lining", score: p2.str_score ?? 0.5, detail: `max run: ${p2.max_run ?? 0}`         },
            { label: "Variability",     score: p2.irv_score ?? 0.5, detail: `IRV: ${(p2.irv ?? 0).toFixed(2)}`   },
          ].map(({ label, score, detail }) => (
            <div key={label} style={{ marginBottom: 10 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 5 }}>
                <span style={{ color: "var(--cream2)" }}>{label}</span>
                <span style={{ color: "var(--gold)" }}>{detail}  {Math.round(score * 100)}%</span>
              </div>
              <Bar pct={score * 100} />
            </div>
          ))}
        </div>

        <div style={{ height: 1, background: "rgba(201,168,76,0.08)", margin: "16px 0" }} />

        {/* P3 */}
        <div>
          <div style={{ fontSize: 13, color: "var(--muted)", fontWeight: 500, marginBottom: 8 }}>
            P3 — Statistical Stability
          </div>
          <p style={{ fontSize: 12, color: "var(--muted)", fontStyle: "italic" }}>
            {p3.note ?? "Pending calibration data"}
          </p>
        </div>
      </div>

      {/* ── Top 3 Career Teasers ────────────────────────────── */}
      <div style={card()}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
          <div>
            <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 4 }}>
              Career Matches
            </div>
            <div style={{ fontFamily: "'DM Serif Display',serif", fontSize: 20, color: "var(--cream)" }}>
              Top Recommendations
            </div>
          </div>
          <button
            className="btn-primary"
            onClick={onViewCareers}
            style={{ fontSize: 13, padding: "10px 20px" }}
          >
            View All
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>

        {careerLoad ? (
          <div style={{ display: "flex", alignItems: "center", gap: 12, padding: "16px 0" }}>
            <div className="spinner" style={{ width: 24, height: 24 }} />
            <span style={{ fontSize: 13, color: "var(--muted)" }}>Finding your matches…</span>
          </div>
        ) : topCareers.length === 0 ? (
          <p style={{ fontSize: 13, color: "var(--muted)" }}>No career data available.</p>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {topCareers.map((career, i) => (
              <CareerTeaser key={career.id} career={career} rank={i + 1} />
            ))}
          </div>
        )}
      </div>

      {/* ── Raw JSON ───────────────────────────────────────── */}
      <details style={{ marginBottom: 24 }}>
        <summary style={{ cursor: "pointer", fontSize: 13, color: "var(--muted)", padding: "12px 0", listStyle: "none" }}>
          View raw profile JSON ↓
        </summary>
        <pre style={{
          marginTop: 12, background: "var(--navy2)",
          border: "1px solid rgba(201,168,76,0.1)", borderRadius: "var(--radius)",
          padding: 20, fontSize: 11, color: "var(--cream2)", overflow: "auto", lineHeight: 1.7,
        }}>
          {JSON.stringify(profile, null, 2)}
        </pre>
      </details>

      {/* ── Actions ────────────────────────────────────────── */}
      <div className="results-actions">
        <button className="btn-ghost" onClick={onRetake}>← Retake</button>
        <button className="btn-ghost" onClick={onViewCareers}>All Careers →</button>
        <button className="btn-primary" onClick={() => {
          const blob = new Blob([JSON.stringify(profile, null, 2)], { type: "application/json" });
          const a    = document.createElement("a");
          a.href     = URL.createObjectURL(blob);
          a.download = `edwiserr_${mbti_display}.json`;
          a.click();
        }}>
          Download
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
            <path d="M8 2v8M4 7l4 4 4-4M2 13h12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>

    </div>
  );
}

function CareerTeaser({ career, rank }) {
  const srcColor = SOURCE_COLORS[career.source] || "var(--gold)";
  const srcLabel = SOURCE_LABELS[career.source] || career.source;
  const fitColor = career.fit_score >= 90 ? "#4cc97a" : career.fit_score >= 80 ? "#c9a84c" : "#4c9ac9";

  return (
    <div style={{
      display: "flex", alignItems: "center", gap: 16,
      background: "rgba(201,168,76,0.04)",
      border: "1px solid rgba(201,168,76,0.1)",
      borderRadius: 10, padding: "14px 16px",
    }}>
      <div style={{
        width: 32, height: 32, minWidth: 32, borderRadius: "50%",
        background: "rgba(201,168,76,0.1)",
        display: "flex", alignItems: "center", justifyContent: "center",
        fontFamily: "'DM Serif Display',serif", fontSize: 14, color: "var(--gold)",
      }}>
        {rank}
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4, flexWrap: "wrap" }}>
          <span style={{ fontSize: 14, color: "var(--cream)", fontWeight: 500 }}>{career.name}</span>
          <span style={{
            fontSize: 10, letterSpacing: "0.1em", textTransform: "uppercase",
            color: srcColor, border: `1px solid ${srcColor}44`,
            borderRadius: 4, padding: "2px 6px",
          }}>{srcLabel}</span>
        </div>
        <div style={{ fontSize: 12, color: "var(--muted)", lineHeight: 1.5 }}>
          {career.explanation?.split('.')[0]}.
        </div>
        {career.entrance_exam && (
          <div style={{ fontSize: 11, color: "var(--gold)", marginTop: 4, opacity: 0.8 }}>
            📋 {career.entrance_exam}
          </div>
        )}
      </div>
      <div style={{
        fontFamily: "'DM Serif Display',serif", fontSize: 22,
        color: fitColor, minWidth: 48, textAlign: "right",
      }}>
        {career.fit_score}
      </div>
    </div>
  );
}