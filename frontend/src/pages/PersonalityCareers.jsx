// ============================================================
// EDWISERR — PersonalityCareers.jsx
// OCEAN → Archetypes → Careers
// ============================================================

const TRAIT_META = {
  Openness: {
    label: "Openness",
    color: "rgba(138,110,200,0.85)",
    blurb: "curiosity, imagination, and openness to new experiences",
  },

  Conscientiousness: {
    label: "Conscientiousness",
    color: "rgba(201,168,76,0.85)",
    blurb: "organisation, discipline, and goal-directed thinking",
  },

  Extraversion: {
    label: "Extraversion",
    color: "rgba(76,160,201,0.85)",
    blurb: "social energy, expressiveness, and outward engagement",
  },

  Agreeableness: {
    label: "Agreeableness",
    color: "rgba(76,201,140,0.85)",
    blurb: "cooperation, empathy, and interpersonal warmth",
  },

  Neuroticism: {
    label: "Neuroticism",
    color: "rgba(201,100,76,0.85)",
    blurb: "emotional sensitivity and stress responsiveness",
  },
};


// ============================================================
// Helpers
// ============================================================

function clampPercent(value) {
  const num = Number(value);

  if (Number.isNaN(num)) return 0;

  return Math.round(Math.max(0, Math.min(100, num)));
}


// ============================================================
// TraitBar
// ============================================================

function TraitBar({ trait, value }) {
  const meta = TRAIT_META[trait] || {};
  const pct = clampPercent(value);

  return (
    <div style={{ marginBottom: 10 }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: 4,
        }}
      >
        <span
          style={{
            fontSize: 12,
            color: "var(--cream2)",
            letterSpacing: "0.04em",
          }}
        >
          {meta.label || trait}
        </span>

        <span
          style={{
            fontSize: 11,
            color: "var(--muted)",
          }}
        >
          {pct}%
        </span>
      </div>

      <div
        style={{
          height: 6,
          borderRadius: 99,
          background: "rgba(255,255,255,0.06)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${pct}%`,
            borderRadius: 99,
            background: meta.color || "var(--gold)",
            transition: "width 0.6s ease",
          }}
        />
      </div>
    </div>
  );
}


// ============================================================
// SectionLabel
// ============================================================

function SectionLabel({ children }) {
  return (
    <div
      style={{
        fontSize: 10,
        letterSpacing: "0.18em",
        textTransform: "uppercase",
        color: "var(--gold)",
        marginBottom: 12,
        opacity: 0.9,
      }}
    >
      {children}
    </div>
  );
}


// ============================================================
// Card
// ============================================================

function Card({ children, style }) {
  return (
    <div
      style={{
        background: "rgba(201,168,76,0.04)",
        border: "1px solid rgba(201,168,76,0.09)",
        borderRadius: 10,
        padding: "14px 16px",
        ...style,
      }}
    >
      {children}
    </div>
  );
}


// ============================================================
// Main Component
// ============================================================

export default function PersonalityCareers({
  ocean_scores = {},
  confidence = { overall: 1 },
  archetypes = [],
  recommendations = [],
  onClarify = null,
}) {

  // ───────────────────────────────────────────────────────────
  // Sorted traits
  // ───────────────────────────────────────────────────────────

  const sortedTraits = [...Object.entries(ocean_scores)]
    .sort(([, a], [, b]) => b - a);

  const topTwo = sortedTraits.slice(0, 2);


  // ───────────────────────────────────────────────────────────
  // Archetypes
  // ───────────────────────────────────────────────────────────

  const topArchetypes = [...archetypes]
    .sort((a, b) => (b.score || 0) - (a.score || 0))
    .slice(0, 3);


  // ───────────────────────────────────────────────────────────
  // Recommendations
  // ───────────────────────────────────────────────────────────

  const topRecs = [...recommendations]
    .sort((a, b) => (b.fit_score || 0) - (a.fit_score || 0))
    .slice(0, 5);


  // ───────────────────────────────────────────────────────────
  // Confidence
  // ───────────────────────────────────────────────────────────

  const confidenceValue = Number(confidence?.overall ?? 1);

  const lowConfidence = confidenceValue < 0.65;


  // ==========================================================
  // Render
  // ==========================================================

  return (
    <div
      role="region"
      aria-label="Personality and Career Profile"
      style={{
        background: "var(--navy2)",
        border: "1px solid rgba(201,168,76,0.15)",
        borderRadius: "var(--radius-lg)",
        overflow: "hidden",
        marginBottom: 16,
      }}
    >

      {/* ======================================================
          Header
      ====================================================== */}

      <div
        style={{
          background:
            "linear-gradient(135deg, rgba(201,168,76,0.1) 0%, rgba(13,27,42,0) 60%)",

          borderBottom: "1px solid rgba(201,168,76,0.1)",
          padding: "28px 28px 22px",
        }}
      >

        <div
          style={{
            fontSize: 11,
            letterSpacing: "0.2em",
            textTransform: "uppercase",
            color: "var(--gold)",
            marginBottom: 10,
          }}
        >
          Personality Profile
        </div>


        {/* Top Traits */}

        {topTwo.length > 0 && (
          <>
            <div
              style={{
                fontFamily: "'DM Serif Display', serif",
                fontSize: 20,
                color: "var(--cream)",
                marginBottom: 6,
                lineHeight: 1.3,
              }}
            >
              Your profile shows strong patterns in{" "}

              {topTwo.map(([trait], idx) => (
                <span key={trait}>
                  <span style={{ color: "var(--gold)" }}>
                    {TRAIT_META[trait]?.label || trait}
                  </span>

                  {idx < topTwo.length - 1 ? " and " : ""}
                </span>
              ))}
            </div>

            <p
              style={{
                fontSize: 13,
                color: "var(--muted)",
                lineHeight: 1.7,
                margin: 0,
              }}
            >
              {topTwo
                .map(([trait]) => TRAIT_META[trait]?.blurb)
                .filter(Boolean)
                .join(", and ")}
              .
            </p>
          </>
        )}


        {/* Low Confidence */}

        {lowConfidence && (
          <div
            role="status"
            aria-live="polite"
            style={{
              marginTop: 14,
              fontSize: 12,
              color: "var(--muted)",
              background: "rgba(201,168,76,0.06)",
              border: "1px solid rgba(201,168,76,0.12)",
              borderRadius: 6,
              padding: "10px 12px",
              lineHeight: 1.7,
            }}
          >
            <div style={{ marginBottom: onClarify ? 10 : 0 }}>
              These results may benefit from additional clarification
              questions for better accuracy.
            </div>

            {typeof onClarify === "function" && (
              <button
                onClick={onClarify}
                style={{
                  background: "rgba(201,168,76,0.12)",
                  color: "var(--gold)",
                  border: "1px solid rgba(201,168,76,0.2)",
                  borderRadius: 6,
                  padding: "6px 12px",
                  cursor: "pointer",
                  fontSize: 11,
                  letterSpacing: "0.04em",
                }}
              >
                Improve Accuracy
              </button>
            )}
          </div>
        )}
      </div>


      {/* ======================================================
          Body
      ====================================================== */}

      <div style={{ padding: "22px 28px" }}>

        {/* ====================================================
            Trait Overview
        ==================================================== */}

        {sortedTraits.length > 0 && (
          <div style={{ marginBottom: 26 }}>
            <SectionLabel>Trait Overview</SectionLabel>

            <div>
              {sortedTraits.map(([trait, value]) => (
                <TraitBar
                  key={trait}
                  trait={trait}
                  value={value}
                />
              ))}
            </div>
          </div>
        )}


        {/* ====================================================
            Archetypes
        ==================================================== */}

        {topArchetypes.length > 0 && (
          <div style={{ marginBottom: 26 }}>
            <SectionLabel>Closest Archetypes</SectionLabel>

            <p
              style={{
                fontSize: 12,
                color: "var(--muted)",
                marginBottom: 12,
                lineHeight: 1.6,
              }}
            >
              Your responses most closely align with the following
              patterns — these are tendencies, not fixed categories.
            </p>

            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 8,
              }}
            >

              {topArchetypes.map((a, idx) => {

                const scorePct = clampPercent(a.score);

                return (
                  <Card key={a.name || idx}>

                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "flex-start",
                        gap: 8,
                      }}
                    >

                      <div>
                        <div
                          style={{
                            fontFamily: "'DM Serif Display', serif",
                            fontSize: 15,
                            color: "var(--cream)",
                            marginBottom: a.description ? 4 : 0,
                          }}
                        >
                          {a.name}
                        </div>

                        {a.description && (
                          <div
                            style={{
                              fontSize: 12,
                              color: "var(--muted)",
                              lineHeight: 1.65,
                            }}
                          >
                            {a.description}
                          </div>
                        )}
                      </div>


                      <div
                        style={{
                          fontSize: 11,
                          color: "var(--gold)",
                          background: "rgba(201,168,76,0.1)",
                          border: "1px solid rgba(201,168,76,0.2)",
                          borderRadius: 4,
                          padding: "2px 8px",
                          whiteSpace: "nowrap",
                          flexShrink: 0,
                        }}
                      >
                        {scorePct}% match
                      </div>

                    </div>
                  </Card>
                );
              })}
            </div>
          </div>
        )}


        {/* ====================================================
            Career Directions
        ==================================================== */}

        {topRecs.length > 0 && (
          <div>

            <SectionLabel>Aligned Career Directions</SectionLabel>

            <p
              style={{
                fontSize: 12,
                color: "var(--muted)",
                marginBottom: 12,
                lineHeight: 1.6,
              }}
            >
              Based on your trait profile, you tend to thrive in
              environments that emphasise the following areas.
            </p>

            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 8,
              }}
            >

              {topRecs.map((r, idx) => {

                const fitPct = clampPercent(r.fit_score);

                return (
                  <Card
                    key={r.name || idx}
                    style={{ padding: "12px 16px" }}
                  >

                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 12,
                      }}
                    >

                      {/* Circular Fit Indicator */}

                      <div
                        style={{
                          width: 36,
                          height: 36,
                          borderRadius: "50%",
                          flexShrink: 0,

                          background:
                            `conic-gradient(
                              var(--gold) ${fitPct * 3.6}deg,
                              rgba(255,255,255,0.06) 0deg
                            )`,

                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                        }}
                      >

                        <div
                          style={{
                            width: 26,
                            height: 26,
                            borderRadius: "50%",
                            background: "var(--navy2)",

                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",

                            fontSize: 9,
                            color: "var(--gold)",
                            fontWeight: 600,
                          }}
                        >
                          {fitPct}%
                        </div>

                      </div>


                      {/* Career Text */}

                      <div
                        style={{
                          flex: 1,
                          minWidth: 0,
                        }}
                      >

                        <div
                          style={{
                            fontSize: 13,
                            color: "var(--cream)",
                            marginBottom: 2,
                          }}
                        >
                          {r.name}
                        </div>

                        {r.category && (
                          <div
                            style={{
                              fontSize: 10,
                              color: "var(--gold)",
                              letterSpacing: "0.08em",
                              textTransform: "uppercase",
                              opacity: 0.75,
                            }}
                          >
                            {r.category}
                          </div>
                        )}

                      </div>
                    </div>
                  </Card>
                );
              })}
            </div>
          </div>
        )}


        {/* ====================================================
            Footer
        ==================================================== */}

        <div
          style={{
            borderTop: "1px solid rgba(201,168,76,0.08)",
            marginTop: 22,
            paddingTop: 14,

            fontSize: 11,
            color: "var(--muted)",
            fontStyle: "italic",
            lineHeight: 1.7,
            opacity: 0.7,
          }}
        >
          This profile reflects patterns in your responses and is
          intended as a guide — not a fixed identity.
          Traits and preferences can shift over time and across contexts.
        </div>

      </div>
    </div>
  );
}