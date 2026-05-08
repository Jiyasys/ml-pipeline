import { useState, useEffect } from "react";
import axios from "axios";
import PersonalityCareers from "./PersonalityCareers";

const API = import.meta.env.VITE_API_URL;

const TRAIT_META = {
  Openness: {
    color: "#c9a84c",
    emoji: "🔭",
    low: "Tends toward familiar, structured environments",
    high: "Tends toward curiosity, imagination, and new ideas",
  },
  Conscientiousness: {
    color: "#4c9ac9",
    emoji: "📋",
    low: "Tends toward flexibility and spontaneity",
    high: "Tends toward organisation, discipline, and goal focus",
  },
  Extraversion: {
    color: "#c94c7a",
    emoji: "⚡",
    low: "Tends to recharge through solitude",
    high: "Tends to be energised by people and social engagement",
  },
  Agreeableness: {
    color: "#4cc97a",
    emoji: "🤝",
    low: "Tends toward analytical, direct communication",
    high: "Tends toward cooperation and valuing relationships",
  },
  Neuroticism: {
    color: "#9a4cc9",
    emoji: "🌊",
    low: "Tends toward emotional steadiness under pressure",
    high: "Tends toward emotional sensitivity and depth of feeling",
  },
};

const TRAIT_ORDER = [
  "Openness",
  "Conscientiousness",
  "Extraversion",
  "Agreeableness",
  "Neuroticism",
];

const SOURCE_LABELS = {
  onet: "Global",
  indian: "India",
  hybrid: "Hybrid",
};

const SOURCE_COLORS = {
  onet: "#4c9ac9",
  indian: "#c9a84c",
  hybrid: "#4cc97a",
};

const LOW_CONFIDENCE_THRESHOLD = 0.65;

// ── Helpers ───────────────────────────────────────────────

function confidenceLabel(v) {
  if (v >= 0.8) return "high";
  if (v >= 0.65) return "moderate";
  return "low";
}

function interpretationStrength(v) {
  if (v >= 0.8) return "strongly suggest";
  if (v >= 0.65) return "suggest";
  return "broadly indicate";
}

/** Normalise 0–1 or 0–100 → 0–100 */
function norm(v) {
  if (v == null || Number.isNaN(v)) return 0;

  const n = Number(v);

  return Math.max(
    0,
    Math.min(100, Math.round(n <= 1 ? n * 100 : n))
  );
}

/** Sanitised export */
function buildExport(profile, topCareers) {
  return {
    ocean_scores: profile.ocean_scores,
    archetypes: profile.archetypes,
    recommendations: topCareers.map((c) => ({
      id: c.id,
      name: c.name,
      fit_score: norm(c.fit_score),
      source: c.source,
    })),
    generated_at: new Date().toISOString(),
  };
}

function clearAssessmentSession() {
  try {
    localStorage.removeItem("edwiserr_quiz_session");
  } catch {}

  try {
    sessionStorage.removeItem("edwiserr_quiz_session");
  } catch {}
}

// ── Shared primitives ────────────────────────────────────

function Bar({
  pct,
  color = "var(--gold)",
  height = 3,
}) {
  return (
    <div
      style={{
        height,
        background: "rgba(201,168,76,0.1)",
        borderRadius: 2,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          height: "100%",
          width: `${pct}%`,
          background: color,
          borderRadius: 2,
          transition: "width 1.2s ease",
        }}
      />
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

// ── Display components ───────────────────────────────────

function LowConfidenceNotice() {
  return (
    <div
      style={{
        background: "rgba(201,168,76,0.06)",
        border: "1px solid rgba(201,168,76,0.15)",
        borderRadius: 8,
        padding: "12px 16px",
        marginBottom: 16,
        fontSize: 13,
        color: "var(--muted)",
        lineHeight: 1.6,
      }}
    >
      These results reflect broader tendencies and may
      benefit from additional exploration. Patterns
      become clearer with more responses over time.
    </div>
  );
}

function DerivationNote({ overall }) {
  const strength = interpretationStrength(overall);

  return (
    <p
      style={{
        fontSize: 12,
        color: "var(--muted)",
        lineHeight: 1.7,
        marginTop: 12,
        fontStyle: "italic",
      }}
    >
      Your responses were mapped into broader
      personality trait patterns and compared against
      behavioral archetypes and work-style preferences.
      The results {strength} patterns across five
      dimensions — combinations of these traits,
      rather than any single score, shape the overall
      picture.
    </p>
  );
}

function TraitNeutralityNote() {
  return (
    <p
      style={{
        fontSize: 12,
        color: "var(--muted)",
        lineHeight: 1.6,
        marginTop: 10,
        fontStyle: "italic",
      }}
    >
      No trait position is inherently better or worse —
      different patterns suit different environments
      and working styles.
    </p>
  );
}

// ── Main component ───────────────────────────────────────

export default function Results({
  profile,userType,
  onViewCareers,
  onRetake,
}) {
  const [topCareers, setTopCareers] = useState([]);
  const [careerLoad, setCareerLoad] = useState(true);
  const [showDetails, setShowDetails] =
    useState(false);

  useEffect(() => {
    if (!profile?.ocean_scores) return;

    let cancelled = false;

    setCareerLoad(true);

    axios
      .post(`${API}/careers/recommend`, {
        ocean_scores: profile.ocean_scores,
        user_type: profile.user_type,
        top_n: 5,
      })
      .then((r) => {
        if (cancelled) return;

        setTopCareers(
          r.data?.recommendations || []
        );

        setCareerLoad(false);
      })
      .catch(() => {
        if (cancelled) return;
        setCareerLoad(false);
      });

    return () => {
      cancelled = true;
    };
  }, [profile]);

  if (!profile) return null;

  const {
    ocean_scores,
    archetype_display,
    archetypes,
    confidence,
    questions_answered,
  } = profile;

  const overall = confidence?.overall ?? 0;

  const confLevel =
    confidenceLabel(overall);

  const isLowConf =
    overall < LOW_CONFIDENCE_THRESHOLD;

  const p1 = confidence?.pillar_1 ?? {};
  const p2 = confidence?.pillar_2 ?? {};
  const p3 = confidence?.pillar_3 ?? {};

  const handleRetake = () => {
    clearAssessmentSession();
    onRetake?.();
  };

  const handleDownload = () => {
    const blob = new Blob(
      [
        JSON.stringify(
          buildExport(profile, topCareers),
          null,
          2
        ),
      ],
      {
        type: "application/json",
      }
    );

    const a = document.createElement("a");

    a.href = URL.createObjectURL(blob);

    a.download = "edwiserr_profile.json";

    a.click();

    URL.revokeObjectURL(a.href);
  };

  return (
    <div className="results">
      {/* ── Header ───────────────────────────── */}
      <div className="results-header">
        <div className="section-eyebrow">
          Behavioral Profile Overview
        </div>

        {archetype_display && (
          <div className="profile-badge">
            {archetype_display}
          </div>
        )}

        <h2 className="results-title">
          Profile Summary
        </h2>

        <p className="results-sub">
          {questions_answered} questions · 5
          personality dimensions
        </p>
      </div>

      {/* ── Low confidence notice ───────────── */}
      {isLowConf && <LowConfidenceNotice />}

      {/* ── Personality summary ─────────────── */}
      <PersonalityCareers
        ocean_scores={ocean_scores}
        confidence={confidence}
        archetypes={archetypes || []}
        recommendations={topCareers}
      />

      {/* ── Derivation note ─────────────────── */}
      <div style={card({ padding: "18px 24px" })}>
        <div
          style={{
            fontSize: 11,
            letterSpacing: "0.15em",
            textTransform: "uppercase",
            color: "var(--muted)",
            marginBottom: 6,
          }}
        >
          How these results are derived
        </div>

        <DerivationNote overall={overall} />
      </div>

      {/* ── Career preview ──────────────────── */}
      <div style={card()}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: 8,
          }}
        >
          <div>
            <div
              style={{
                fontSize: 11,
                letterSpacing: "0.15em",
                textTransform: "uppercase",
                color: "var(--muted)",
                marginBottom: 4,
              }}
            >
              Career Alignment
            </div>

            <div
              style={{
                fontFamily:
                  "'DM Serif Display', serif",
                fontSize: 20,
                color: "var(--cream)",
              }}
            >
              Likely Fit Areas
            </div>
          </div>

          <button
            className="btn-primary"
            onClick={onViewCareers}
            style={{
              fontSize: 13,
              padding: "10px 20px",
            }}
          >
            Explore All
          </button>
        </div>

        <p
          style={{
            fontSize: 12,
            color: "var(--muted)",
            lineHeight: 1.6,
            marginBottom: 16,
          }}
        >
          These directions reflect environments and
          roles that tend to align with your
          behavioral patterns — not prescriptions for
          a fixed path.
        </p>

        {careerLoad ? (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              padding: "16px 0",
            }}
          >
            <div
              className="spinner"
              style={{
                width: 24,
                height: 24,
              }}
            />

            <span
              style={{
                fontSize: 13,
                color: "var(--muted)",
              }}
            >
              Finding aligned areas…
            </span>
          </div>
        ) : topCareers.length === 0 ? (
          <p
            style={{
              fontSize: 13,
              color: "var(--muted)",
            }}
          >
            No strong alignment patterns emerged yet.
            Additional exploration may improve
            recommendations.
          </p>
        ) : (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 12,
            }}
          >
            {topCareers.map((career, i) => (
              <CareerTeaser
                key={career.id}
                career={career}
                rank={i + 1}
                isLowConf={isLowConf}
              />
            ))}
          </div>
        )}
      </div>

      {/* ── Actions ─────────────────────────── */}
      <div
        className="results-actions"
        style={{ marginBottom: 32 }}
      >
        <button
          className="btn-ghost"
          onClick={handleRetake}
        >
          ← Retake
        </button>

        <button
          className="btn-ghost"
          onClick={onViewCareers}
        >
          Explore Careers →
        </button>

        <button
          className="btn-primary"
          onClick={handleDownload}
        >
          Download
        </button>
      </div>

      {/* ── Advanced toggle ─────────────────── */}
      <div
        style={{
          borderTop:
            "1px solid rgba(201,168,76,0.08)",
          paddingTop: 20,
          marginBottom: showDetails ? 0 : 40,
        }}
      >
        <button
          onClick={() =>
            setShowDetails((v) => !v)
          }
          style={{
            background: "transparent",
            border:
              "1px solid rgba(201,168,76,0.15)",
            borderRadius: 8,
            padding: "8px 18px",
            cursor: "pointer",
            fontSize: 12,
            color: "var(--muted)",
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          <span style={{ fontSize: 14 }}>
            {showDetails ? "🔒" : "🔓"}
          </span>

          {showDetails
            ? "Hide advanced details"
            : "Advanced details"}
        </button>
      </div>

      {/* ── Advanced details ────────────────── */}
      {showDetails && (
        <div
          style={{
            marginTop: 20,
            paddingBottom: 40,
          }}
        >
          {/* OCEAN */}
          <div
            style={{
              fontSize: 11,
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              color: "var(--muted)",
              marginBottom: 6,
            }}
          >
            OCEAN Trait Scores (0–100)
          </div>

          <TraitNeutralityNote />

          <div
            className="ocean-grid"
            style={{
              marginBottom: 16,
              marginTop: 12,
            }}
          >
            {TRAIT_ORDER.map((trait, i) => {
              const score = norm(
                ocean_scores?.[trait]
              );

              const meta = TRAIT_META[trait];

              const conf =
                confidence?.per_trait?.[trait];

              return (
                <div
                  key={trait}
                  className="ocean-card"
                  style={{
                    animationDelay: `${
                      i * 0.1
                    }s`,
                  }}
                >
                  <div
                    style={{
                      fontSize: 22,
                      marginBottom: 8,
                    }}
                  >
                    {meta.emoji}
                  </div>

                  <div className="ocean-trait">
                    {trait}
                  </div>

                  <div
                    className="ocean-score"
                    style={{
                      color: meta.color,
                    }}
                  >
                    {score}
                  </div>

                  <Bar
                    pct={score}
                    color={meta.color}
                  />

                  <div className="ocean-subdim">
                    {score >= 50
                      ? meta.high
                      : meta.low}
                  </div>

                  {conf != null && (
                    <div
                      style={{
                        fontSize: 11,
                        color: "var(--muted)",
                        marginTop: 8,
                      }}
                    >
                      conf {norm(conf)}%
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Confidence */}
          <div style={card()}>
            <div
              style={{
                fontSize: 11,
                letterSpacing: "0.15em",
                textTransform: "uppercase",
                color: "var(--muted)",
                marginBottom: 16,
              }}
            >
              Overall Confidence —{" "}
              {norm(overall)}% ({confLevel})
            </div>

            <Bar
              pct={norm(overall)}
              height={4}
            />

            {isLowConf && (
              <p
                style={{
                  fontSize: 12,
                  color: "var(--muted)",
                  marginTop: 10,
                  fontStyle: "italic",
                }}
              >
                Confidence is below the range where
                interpretations are most stable.
                Results should be read as broader
                tendencies.
              </p>
            )}

            <div
              style={{
                height: 1,
                background:
                  "rgba(201,168,76,0.08)",
                margin: "20px 0",
              }}
            />

            {/* P1 */}
            {Object.keys(p1).length > 0 && (
              <div style={{ marginBottom: 18 }}>
                <div
                  style={{
                    fontSize: 13,
                    color: "var(--gold)",
                    marginBottom: 12,
                    fontWeight: 500,
                  }}
                >
                  P1 —{" "}
                  {p1.label ??
                    "Internal Consistency"}
                </div>

                {TRAIT_ORDER.map((trait) => {
                  const pct = norm(
                    p1.scores?.[trait] ?? 0
                  );

                  return (
                    <div
                      key={trait}
                      style={{
                        marginBottom: 10,
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent:
                            "space-between",
                          fontSize: 12,
                          marginBottom: 5,
                        }}
                      >
                        <span
                          style={{
                            color: "var(--cream2)",
                          }}
                        >
                          {trait}
                        </span>

                        <span
                          style={{
                            color: "var(--gold)",
                          }}
                        >
                          {pct}%
                        </span>
                      </div>

                      <Bar pct={pct} />
                    </div>
                  );
                })}
              </div>
            )}

            {/* P2 */}
            {Object.keys(p2).length > 0 && (
              <>
                <div
                  style={{
                    height: 1,
                    background:
                      "rgba(201,168,76,0.08)",
                    margin: "16px 0",
                  }}
                />

                <div style={{ marginBottom: 18 }}>
                  <div
                    style={{
                      fontSize: 13,
                      color: "var(--gold)",
                      marginBottom: 12,
                      fontWeight: 500,
                    }}
                  >
                    P2 —{" "}
                    {p2.label ??
                      "Behavioral Quality"}
                  </div>

                  {[
                    {
                      label: "Response time",
                      score:
                        p2.rt_score ?? 0.5,
                    },
                    {
                      label: "Straight-lining",
                      score:
                        p2.str_score ?? 0.5,
                    },
                    {
                      label: "Variability",
                      score:
                        p2.irv_score ?? 0.5,
                    },
                  ].map(({ label, score }) => (
                    <div
                      key={label}
                      style={{
                        marginBottom: 10,
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent:
                            "space-between",
                          fontSize: 12,
                          marginBottom: 5,
                        }}
                      >
                        <span
                          style={{
                            color: "var(--cream2)",
                          }}
                        >
                          {label}
                        </span>

                        <span
                          style={{
                            color: "var(--gold)",
                          }}
                        >
                          {norm(score)}%
                        </span>
                      </div>

                      <Bar
                        pct={norm(score)}
                      />
                    </div>
                  ))}
                </div>
              </>
            )}

            {/* P3 */}
            <div
              style={{
                height: 1,
                background:
                  "rgba(201,168,76,0.08)",
                margin: "16px 0",
              }}
            />

            <div>
              <div
                style={{
                  fontSize: 13,
                  color: "var(--muted)",
                  fontWeight: 500,
                  marginBottom: 8,
                }}
              >
                P3 — Statistical Stability
              </div>

              <p
                style={{
                  fontSize: 12,
                  color: "var(--muted)",
                  fontStyle: "italic",
                }}
              >
                {p3.note ??
                  "Pending calibration data"}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ── Career teaser ────────────────────────────────────────

function CareerTeaser({
  career,
  rank,
  isLowConf,
}) {
  const srcColor =
    SOURCE_COLORS[career.source] ||
    "var(--gold)";

  const srcLabel =
    SOURCE_LABELS[career.source] ||
    career.source;

  const fitScore = norm(career.fit_score);

  const fitColor =
    fitScore >= 90
      ? "#4cc97a"
      : fitScore >= 80
      ? "#c9a84c"
      : "#4c9ac9";

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 16,
        background:
          "rgba(201,168,76,0.04)",
        border:
          "1px solid rgba(201,168,76,0.1)",
        borderRadius: 10,
        padding: "14px 16px",
      }}
    >
      <div
        style={{
          width: 32,
          height: 32,
          minWidth: 32,
          borderRadius: "50%",
          background:
            "rgba(201,168,76,0.1)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontFamily:
            "'DM Serif Display', serif",
          fontSize: 14,
          color: "var(--gold)",
        }}
      >
        {rank}
      </div>

      <div
        style={{
          flex: 1,
          minWidth: 0,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            marginBottom: 4,
            flexWrap: "wrap",
          }}
        >
          <span
            style={{
              fontSize: 14,
              color: "var(--cream)",
              fontWeight: 500,
            }}
          >
            {career.name}
          </span>

          <span
            style={{
              fontSize: 10,
              letterSpacing: "0.1em",
              textTransform: "uppercase",
              color: srcColor,
              border: `1px solid ${srcColor}44`,
              borderRadius: 4,
              padding: "2px 6px",
            }}
          >
            {srcLabel}
          </span>
        </div>

        <div
          style={{
            fontSize: 12,
            color: "var(--muted)",
            lineHeight: 1.5,
          }}
        >
          {career.explanation
            ?.split(".")[0] || ""}
          .
        </div>

        {career.entrance_exam && (
          <div
            style={{
              fontSize: 11,
              color: "var(--gold)",
              marginTop: 4,
              opacity: 0.8,
            }}
          >
            📋 {career.entrance_exam}
          </div>
        )}

        {isLowConf && (
          <div
            style={{
              fontSize: 11,
              color: "var(--muted)",
              marginTop: 4,
              fontStyle: "italic",
            }}
          >
            Alignment confidence is moderate —
            treat this as a possible direction,
            not a definitive match.
          </div>
        )}
      </div>

      <div
        style={{
          fontFamily:
            "'DM Serif Display', serif",
          fontSize: 22,
          color: fitColor,
          minWidth: 48,
          textAlign: "right",
        }}
      >
        {fitScore}
      </div>
    </div>
  );
}