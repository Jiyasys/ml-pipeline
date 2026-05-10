import { useState, useMemo } from "react";

// ── Constants ────────────────────────────────────────────────

const SOURCE_LABELS = {
  onet:   "Global",
  indian: "India",
  hybrid: "Hybrid",
};

const SOURCE_COLORS = {
  onet:   "#4c9ac9",
  indian: "#c9a84c",
  hybrid: "#4cc97a",
};

const TRAIT_COLORS = {
  Openness:          "#c9a84c",
  Conscientiousness: "#4c9ac9",
  Extraversion:      "#c94c7a",
  Agreeableness:     "#4cc97a",
  Neuroticism:       "#9a4cc9",
};

// ── Helpers ──────────────────────────────────────────────────

function normalizeScore(v) {
  if (v == null || Number.isNaN(v)) return 0;
  const n = Number(v);
  return Math.max(0, Math.min(100, n <= 1 ? Math.round(n * 100) : Math.round(n)));
}

/**
 * Normalize a career object to a consistent shape so CareerCard never
 * blows up on missing fields regardless of which backend shape was stored.
 * Handles both the FastAPI CareerSummary shape (career_id / title) and the
 * direct recommender output shape (id / name).
 */
function normalizeCareer(c) {
  if (!c || typeof c !== "object") return null;
  return {
    id:           c.id           || c.career_id || "",
    name:         c.name         || c.title     || "Unknown",
    category:     c.category     || "",
    source:       c.source       || "onet",
    fit_score:    c.fit_score    != null ? c.fit_score : 0,
    description:  c.description  || c.explanation || "",
    explanation:  c.explanation  || c.description || "",
    entrance_exam: c.entrance_exam || null,
    work_style:   Array.isArray(c.work_style)   ? c.work_style   : [],
    tags:         Array.isArray(c.tags)          ? c.tags         : [],
    traits:       c.traits       || null,
    matched_traits:  Array.isArray(c.matched_traits)  ? c.matched_traits  : [],
    mismatch_traits: Array.isArray(c.mismatch_traits) ? c.mismatch_traits : [],
  };
}

// ── Sub-components ───────────────────────────────────────────

function FitBadge({ score }) {
  const value = normalizeScore(score);
  const color =
    value >= 90 ? "#4cc97a"
    : value >= 80 ? "#c9a84c"
    : "#4c9ac9";
  return (
    <div style={{ minWidth: 60, textAlign: "center" }}>
      <div
        style={{
          fontFamily: "'DM Serif Display', serif",
          fontSize: 28,
          lineHeight: 1,
          color,
        }}
      >
        {value}
      </div>
      <div
        style={{
          fontSize: 10,
          color: "var(--muted, #8899aa)",
          textTransform: "uppercase",
          letterSpacing: "0.08em",
        }}
      >
        fit
      </div>
    </div>
  );
}

function SourceTag({ source }) {
  const color = SOURCE_COLORS[source] || "var(--gold, #c9a84c)";
  return (
    <span
      style={{
        fontSize: 10,
        textTransform: "uppercase",
        letterSpacing: "0.1em",
        color,
        border: `1px solid ${color}44`,
        borderRadius: 999,
        padding: "4px 10px",
      }}
    >
      {SOURCE_LABELS[source] || source}
    </span>
  );
}

function CareerCard({ career }) {
  const c   = normalizeCareer(career);
  if (!c) return null;
  const fit = normalizeScore(c.fit_score);

  return (
    <div
      className="career-card"
      style={{
        background: "var(--navy2, #0d1b2a)",
        border: "1px solid rgba(201,168,76,0.12)",
        borderRadius: "var(--radius, 14px)",
        padding: "22px",
        marginBottom: 16,
        transition: "transform 0.2s ease",
      }}
    >
      <div style={{ display: "flex", gap: 18, alignItems: "flex-start" }}>
        <FitBadge score={fit} />

        <div style={{ flex: 1 }}>
          {/* ── Title + source ─── */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              flexWrap: "wrap",
              marginBottom: 8,
            }}
          >
            <h3
              style={{
                margin: 0,
                fontSize: 20,
                color: "var(--cream, #e8dcc8)",
                fontFamily: "'DM Serif Display', serif",
              }}
            >
              {c.name}
            </h3>
            <SourceTag source={c.source} />
          </div>

          {/* ── Description ─── */}
          {(c.description || c.explanation) && (
            <p
              style={{
                fontSize: 14,
                lineHeight: 1.7,
                color: "var(--muted, #8899aa)",
                marginBottom: 14,
              }}
            >
              {c.description || c.explanation}
            </p>
          )}

          {/* ── Entrance exam ─── */}
          {c.entrance_exam && (
            <div
              style={{
                fontSize: 12,
                color: "var(--gold, #c9a84c)",
                marginBottom: 12,
              }}
            >
              📋 {c.entrance_exam}
            </div>
          )}

          {/* ── Tags ─── */}
          {c.tags.length > 0 && (
            <div
              style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 12 }}
            >
              {c.tags.map((tag) => (
                <span
                  key={tag}
                  style={{
                    fontSize: 11,
                    background: "rgba(255,255,255,0.04)",
                    border: "1px solid rgba(255,255,255,0.08)",
                    borderRadius: 999,
                    padding: "4px 10px",
                    color: "var(--muted, #8899aa)",
                  }}
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* ── Work-style tags (from recommender) ─── */}
          {c.work_style.length > 0 && (
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 12 }}>
              {c.work_style.map((style) => (
                <span
                  key={style}
                  style={{
                    fontSize: 11,
                    background: "rgba(201,168,76,0.07)",
                    border: "1px solid rgba(201,168,76,0.18)",
                    borderRadius: 999,
                    padding: "4px 10px",
                    color: "rgba(201,168,76,0.75)",
                    textTransform: "capitalize",
                  }}
                >
                  {style.replace(/_/g, " ")}
                </span>
              ))}
            </div>
          )}

          {/* ── Trait bars (optional — present in detail shape) ─── */}
          {c.traits && Object.keys(c.traits).length > 0 && (
            <div style={{ marginTop: 16 }}>
              {Object.entries(c.traits).map(([trait, value]) => (
                <div key={trait} style={{ marginBottom: 10 }}>
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      fontSize: 11,
                      marginBottom: 4,
                    }}
                  >
                    <span style={{ color: "var(--cream2, #c8d4e0)" }}>{trait}</span>
                    <span style={{ color: "var(--muted, #8899aa)" }}>
                      {Math.round(value)}
                    </span>
                  </div>
                  <div
                    style={{
                      height: 4,
                      borderRadius: 999,
                      background: "rgba(255,255,255,0.06)",
                      overflow: "hidden",
                    }}
                  >
                    <div
                      style={{
                        width: `${value}%`,
                        height: "100%",
                        background: TRAIT_COLORS[trait] || "var(--gold, #c9a84c)",
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* ── Matched / mismatch trait chips ─── */}
          {(c.matched_traits.length > 0 || c.mismatch_traits.length > 0) && (
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 12 }}>
              {c.matched_traits.map((t) => (
                <span
                  key={`match-${t}`}
                  style={{
                    fontSize: 10,
                    background: "rgba(76,201,122,0.08)",
                    border: "1px solid rgba(76,201,122,0.25)",
                    borderRadius: 999,
                    padding: "3px 9px",
                    color: "#4cc97a",
                  }}
                >
                  ✓ {t}
                </span>
              ))}
              {c.mismatch_traits.map((t) => (
                <span
                  key={`mismatch-${t}`}
                  style={{
                    fontSize: 10,
                    background: "rgba(201,76,76,0.08)",
                    border: "1px solid rgba(201,76,76,0.2)",
                    borderRadius: 999,
                    padding: "3px 9px",
                    color: "#c94c4c",
                  }}
                >
                  ↑ {t}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Careers screen ───────────────────────────────────────────

/**
 * Props:
 *   recommendations — array stored in App.jsx state (fetched once by Results.jsx)
 *   onBack          — () => void  → navigate back to Results screen
 *
 * This component is RENDER-ONLY. It never fetches from the API.
 * All data arrives via props.
 */
export default function Careers({ recommendations, onBack }) {
  const [sortBy,       setSortBy]       = useState("fit");
  const [sourceFilter, setSourceFilter] = useState("All");

  // Normalize the incoming array once so the rest of this component
  // can assume a consistent shape regardless of which backend payload
  // was stored upstream.
  const normalized = useMemo(() => {
    if (!Array.isArray(recommendations)) return [];
    return recommendations.map(normalizeCareer).filter(Boolean);
  }, [recommendations]);

  const filtered = useMemo(() => {
    let data = [...normalized];

    if (sourceFilter !== "All") {
      data = data.filter((c) => c.source === sourceFilter);
    }

    if (sortBy === "fit") {
      data.sort(
        (a, b) => normalizeScore(b.fit_score) - normalizeScore(a.fit_score)
      );
    } else {
      data.sort((a, b) => a.name.localeCompare(b.name));
    }

    return data;
  }, [normalized, sourceFilter, sortBy]);

  // Derive which source filters actually have data
  const availableSources = useMemo(() => {
    const present = new Set(normalized.map((c) => c.source));
    return ["All", "onet", "indian", "hybrid"].filter(
      (s) => s === "All" || present.has(s)
    );
  }, [normalized]);

  return (
    <div style={{ minHeight: "100vh", paddingBottom: 80 }}>
      {/* ── Sticky header ──────────────────────────────────── */}
      <div
        style={{
          position: "sticky",
          top: 0,
          zIndex: 20,
          backdropFilter: "blur(12px)",
          background: "rgba(13,27,42,0.94)",
          borderBottom: "1px solid rgba(201,168,76,0.08)",
          padding: "18px 36px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <button className="btn-ghost" onClick={onBack}>
            ← Back
          </button>
          <div>
            <div
              style={{
                fontFamily: "'DM Serif Display', serif",
                fontSize: 22,
                color: "var(--cream, #e8dcc8)",
              }}
            >
              Career Matches
            </div>
            <div style={{ fontSize: 12, color: "var(--muted, #8899aa)" }}>
              {filtered.length} aligned path{filtered.length !== 1 ? "s" : ""}
            </div>
          </div>
        </div>

        <div style={{ display: "flex", gap: 8 }}>
          <button
            className={sortBy === "fit" ? "btn-primary" : "btn-ghost"}
            onClick={() => setSortBy("fit")}
          >
            Best fit
          </button>
          <button
            className={sortBy === "az" ? "btn-primary" : "btn-ghost"}
            onClick={() => setSortBy("az")}
          >
            A–Z
          </button>
        </div>
      </div>

      {/* ── Body ───────────────────────────────────────────── */}
      <div
        style={{
          maxWidth: 920,
          margin: "0 auto",
          padding: "34px 32px 0",
        }}
      >
        {/* Source filters — only render tabs that have data */}
        {availableSources.length > 1 && (
          <div
            style={{
              display: "flex",
              gap: 10,
              flexWrap: "wrap",
              marginBottom: 26,
            }}
          >
            {availableSources.map((src) => (
              <button
                key={src}
                className={sourceFilter === src ? "btn-primary" : "btn-ghost"}
                onClick={() => setSourceFilter(src)}
              >
                {src === "All" ? "All" : SOURCE_LABELS[src] || src}
              </button>
            ))}
          </div>
        )}

        {/* Empty state */}
        {normalized.length === 0 ? (
          <div
            style={{
              textAlign: "center",
              padding: "80px 0",
              color: "var(--muted, #8899aa)",
            }}
          >
            <div style={{ fontSize: 32, marginBottom: 16 }}>🔭</div>
            <div style={{ fontSize: 16, marginBottom: 8 }}>
              No career matches available
            </div>
            <p style={{ fontSize: 13, maxWidth: 340, margin: "0 auto" }}>
              Go back and make sure the personality assessment completed
              successfully, then try again.
            </p>
            <button
              className="btn-ghost"
              onClick={onBack}
              style={{ marginTop: 24 }}
            >
              ← Back to Results
            </button>
          </div>
        ) : filtered.length === 0 ? (
          <div
            style={{
              textAlign: "center",
              padding: "60px 0",
              color: "var(--muted, #8899aa)",
            }}
          >
            No matches for the selected filter.{" "}
            <button
              style={{
                background: "none",
                border: "none",
                color: "var(--gold, #c9a84c)",
                cursor: "pointer",
                fontSize: 13,
                padding: 0,
              }}
              onClick={() => setSourceFilter("All")}
            >
              Clear filter
            </button>
          </div>
        ) : (
          filtered.map((career) => (
            <CareerCard key={career.id || career.name} career={career} />
          ))
        )}
      </div>
    </div>
  );
}