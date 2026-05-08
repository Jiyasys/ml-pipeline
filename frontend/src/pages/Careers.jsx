import { useState, useEffect, useCallback, useRef } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL;

const SOURCE_LABELS = { onet: "Global", indian: "India", hybrid: "Hybrid" };
const SOURCE_COLORS = { onet: "#4c9ac9", indian: "#c9a84c", hybrid: "#4cc97a" };
const TRAIT_COLORS  = {
  Openness: "#c9a84c", Conscientiousness: "#4c9ac9",
  Extraversion: "#c94c7a", Agreeableness: "#4cc97a", Neuroticism: "#9a4cc9",
};

const LOW_CONFIDENCE_THRESHOLD = 0.65;

// ── Helpers ───────────────────────────────────────────────────

function cloneSort(arr, compareFn) {
  return [...arr].sort(compareFn);
}

function isValidProfile(profile) {
  return (
    profile &&
    profile.ocean_scores &&
    typeof profile.ocean_scores === "object" &&
    profile.user_type
  );
}

// ── Sub-components ────────────────────────────────────────────

function FitBadge({ score }) {
  const color = score >= 90 ? "#4cc97a" : score >= 80 ? "#c9a84c" : "#4c9ac9";
  return (
    <div style={{ minWidth: 52, textAlign: "right" }}>
      <div style={{ fontFamily: "'DM Serif Display',serif", fontSize: 26, color, lineHeight: 1 }}>
        {score}
      </div>
      <div style={{ fontSize: 10, color: "var(--muted)", textAlign: "center" }}>fit</div>
    </div>
  );
}

function SourceTag({ source }) {
  const color = SOURCE_COLORS[source] || "var(--gold)";
  return (
    <span style={{
      fontSize: 10, letterSpacing: "0.1em", textTransform: "uppercase",
      color, border: `1px solid ${color}44`, borderRadius: 4, padding: "2px 7px",
    }}>
      {SOURCE_LABELS[source] || source}
    </span>
  );
}

function FilterBtn({ active, color = "var(--gold)", onClick, children }) {
  return (
    <button onClick={onClick} style={{
      fontSize: 12, padding: "6px 14px", borderRadius: 20, cursor: "pointer",
      background: active ? `${color}22` : "transparent",
      border: `1px solid ${active ? color : "rgba(201,168,76,0.2)"}`,
      color: active ? color : "var(--muted)",
      transition: "all 0.2s",
    }}>
      {children}
    </button>
  );
}

function TraitRow({ trait, userScore, idealScore }) {
  const color = TRAIT_COLORS[trait] || "var(--gold)";
  const gap   = Math.abs(userScore - idealScore);
  return (
    <div style={{ marginBottom: 10 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, marginBottom: 4 }}>
        <span style={{ color: "var(--cream2)" }}>{trait}</span>
        <span style={{ color: "var(--muted)" }}>
          you <span style={{ color }}>{Math.round(userScore)}</span>
          {" · "}ideal{" "}
          <span style={{ color: "var(--cream2)" }}>{Math.round(idealScore)}</span>
          {gap > 15 && (
            <span style={{ color: gap > 25 ? "#c94c4c" : "#c9a84c", marginLeft: 6 }}>
              Δ{Math.round(gap)}
            </span>
          )}
        </span>
      </div>
      <div style={{ position: "relative", height: 4, background: "rgba(255,255,255,0.05)", borderRadius: 2 }}>
        <div style={{ position: "absolute", top: 0, left: 0, height: "100%", width: `${idealScore}%`, background: "rgba(255,255,255,0.08)", borderRadius: 2 }} />
        <div style={{ position: "absolute", top: 0, left: 0, height: "100%", width: `${userScore}%`, background: color, borderRadius: 2, transition: "width 0.8s ease" }} />
      </div>
    </div>
  );
}

function CareerCard({ career, ocean_scores }) {
  const [expanded, setExpanded] = useState(false);
  const [detail,   setDetail]   = useState(null);
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState(null);
  const cancelRef = useRef(null);

  useEffect(() => {
    return () => { cancelRef.current?.abort(); };
  }, []);

  const toggle = async () => {
    if (expanded) { setExpanded(false); return; }
    if (detail)   { setExpanded(true);  return; }

    cancelRef.current?.abort();
    const controller = new AbortController();
    cancelRef.current = controller;

    setLoading(true);
    setError(null);

    try {
      const res = await axios.post(
        `${API}/careers/${career.id}`,
        { ocean_scores },
        { signal: controller.signal }
      );
      setDetail(res.data);
      setExpanded(true);
    } catch (err) {
      if (axios.isCancel(err) || err?.code === "ERR_CANCELED") return;
      setError("Could not load career details. Tap to retry.");
      // Do NOT expand on failure — card stays collapsed
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); }
  };

  return (
    <div style={{
      background: "var(--navy2)",
      border: `1px solid ${expanded ? "rgba(201,168,76,0.3)" : "rgba(201,168,76,0.1)"}`,
      borderRadius: "var(--radius)", overflow: "hidden",
      transition: "border-color 0.25s", marginBottom: 12,
    }}>
      {/* Header row — keyboard accessible */}
      <div
        role="button"
        tabIndex={0}
        onClick={toggle}
        onKeyDown={handleKeyDown}
        aria-expanded={expanded}
        style={{ display: "flex", alignItems: "flex-start", gap: 16, padding: "18px 20px", cursor: "pointer", outline: "none" }}
      >
        <FitBadge score={career.fit_score} />
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", marginBottom: 6 }}>
            <span style={{ fontFamily: "'DM Serif Display',serif", fontSize: 17, color: "var(--cream)" }}>
              {career.name}
            </span>
            <SourceTag source={career.source} />
          </div>
          <div style={{ fontSize: 13, color: "var(--muted)", lineHeight: 1.6, marginBottom: career.work_style?.length ? 8 : 0 }}>
            {career.description}
          </div>
          {career.work_style?.length > 0 && (
            <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: career.entrance_exam ? 8 : 0 }}>
              {career.work_style.map(tag => (
                <span key={tag} style={{
                  fontSize: 10, color: "var(--muted)",
                  background: "rgba(255,255,255,0.04)",
                  border: "1px solid rgba(255,255,255,0.08)",
                  borderRadius: 4, padding: "2px 8px", textTransform: "capitalize",
                }}>{tag}</span>
              ))}
            </div>
          )}
          {career.entrance_exam && (
            <div style={{ fontSize: 11, color: "var(--gold)", opacity: 0.85 }}>📋 {career.entrance_exam}</div>
          )}
          {/* Inline error shown below card summary, not in expanded panel */}
          {error && !loading && (
            <div style={{ fontSize: 12, color: "#c94c4c", marginTop: 6 }}>{error}</div>
          )}
        </div>
        <div style={{
          color: "var(--muted)", fontSize: 16, transition: "transform 0.25s",
          transform: expanded ? "rotate(180deg)" : "none", paddingTop: 2,
          display: "flex", alignItems: "center",
        }}>
          {loading ? <div className="spinner" style={{ width: 14, height: 14 }} /> : "⌄"}
        </div>
      </div>

      {/* Expanded detail — only rendered on successful fetch */}
      {expanded && detail && (
        <div style={{ borderTop: "1px solid rgba(201,168,76,0.08)", padding: "18px 20px", animation: "fadeUp 0.3s ease" }}>
          <p style={{ fontSize: 13, color: "var(--cream2)", lineHeight: 1.7, marginBottom: 16 }}>
            {detail.explanation || career.explanation}
          </p>
          {detail.trait_breakdown && (
            <div>
              <div style={{ fontSize: 11, letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 12 }}>
                Trait Alignment
              </div>
              {detail.trait_breakdown.map(t => (
                <TraitRow key={t.trait} trait={t.trait} userScore={t.user_score} idealScore={t.career_ideal} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────

export default function Careers({ profile, recommendations: propRecs, onBack, onClarify }) {
  const [careers,    setCareers]    = useState(propRecs || []);
  const [loading,    setLoading]    = useState(!propRecs);
  const [error,      setError]      = useState(null);
  const [categories, setCategories] = useState(["All"]);
  const [activeCat,  setActiveCat]  = useState("All");
  const [activeSrc,  setActiveSrc]  = useState("All");
  const [sortBy,     setSortBy]     = useState("fit");

  const ocean_scores = profile?.ocean_scores;
  const user_type    = profile?.user_type;
  const confidence   = profile?.confidence?.overall;
  const showLowConfidenceWarning = typeof confidence === "number" && confidence < LOW_CONFIDENCE_THRESHOLD;

  const buildCategories = useCallback((recs) => {
    setCategories(["All", ...new Set(recs.map(c => c.category).filter(Boolean))]);
  }, []);

  const fetchCareers = useCallback(async () => {
    if (!isValidProfile(profile)) return;
    setLoading(true);
    setError(null);
    try {
      const res = await await axios.post(`${API}/careers/recommend`, {
  ocean_scores,
  user_type,
  top_n: 50,
});
      const recs = res.data.recommendations || [];
      setCareers(recs);
      buildCategories(recs);
    } catch {
      setError("Could not load career recommendations. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [ocean_scores, user_type, profile, buildCategories]);

  useEffect(() => {
    if (propRecs) {
      buildCategories(propRecs);
      return;
    }
    fetchCareers();
  }, [propRecs, fetchCareers, buildCategories]);

  const dominant = Object.entries(ocean_scores || {})
    .sort((a, b) => b[1] - a[1]).slice(0, 2)
    .filter(([, v]) => v >= 60).map(([t]) => t);

  const filtered = cloneSort(
    careers
      .filter(c => activeCat === "All" || c.category === activeCat)
      .filter(c => activeSrc === "All" || c.source   === activeSrc),
    sortBy === "fit"
      ? (a, b) => b.fit_score - a.fit_score
      : (a, b) => a.name.localeCompare(b.name)
  );

  return (
    <div style={{ minHeight: "100vh", paddingBottom: 80 }}>

      {/* Sticky nav */}
      <div style={{
        position: "sticky", top: 0, zIndex: 10,
        background: "rgba(13,27,42,0.96)", backdropFilter: "blur(12px)",
        borderBottom: "1px solid rgba(201,168,76,0.08)",
        padding: "16px 40px",
        display: "flex", alignItems: "center", justifyContent: "space-between",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <button className="btn-ghost" onClick={onBack} style={{ padding: "8px 14px" }}>← Back</button>
          <div>
            <div style={{ fontFamily: "'DM Serif Display',serif", fontSize: 18, color: "var(--cream)" }}>Career Matches</div>
            {!loading && <div style={{ fontSize: 12, color: "var(--muted)" }}>{filtered.length} of {careers.length} shown</div>}
          </div>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          {["fit","name"].map(s => (
            <FilterBtn key={s} active={sortBy === s} onClick={() => setSortBy(s)}>
              {s === "fit" ? "Best fit" : "A–Z"}
            </FilterBtn>
          ))}
        </div>
      </div>

      <div style={{ maxWidth: 860, margin: "0 auto", padding: "32px 40px 0" }}>

        {/* Low confidence warning */}
        {showLowConfidenceWarning && (
          <div style={{
            background: "rgba(201,168,76,0.05)", border: "1px solid rgba(201,168,76,0.18)",
            borderRadius: "var(--radius)", padding: "12px 18px", marginBottom: 20,
            display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <span style={{ fontSize: 15 }}>ℹ</span>
              <span style={{ fontSize: 12, color: "var(--muted)" }}>
                Some recommendations may benefit from additional clarification questions.
              </span>
            </div>
            {onClarify && (
              <button className="btn-ghost" onClick={onClarify} style={{ fontSize: 11, padding: "5px 12px", whiteSpace: "nowrap" }}>
                Clarify answers
              </button>
            )}
          </div>
        )}

        {/* Dominant traits banner */}
        {dominant.length > 0 && (
          <div style={{
            background: "rgba(201,168,76,0.06)", border: "1px solid rgba(201,168,76,0.15)",
            borderRadius: "var(--radius)", padding: "14px 20px", marginBottom: 24,
            display: "flex", alignItems: "center", gap: 12,
          }}>
            <span style={{ fontSize: 18 }}>✦</span>
            <span style={{ fontSize: 13, color: "var(--cream2)" }}>
              Strong matches aligned with:{" "}
              {dominant.map((t, i) => (
                <span key={t}>
                  {i > 0 && <span style={{ color: "var(--muted)" }}> & </span>}
                  <span style={{ color: TRAIT_COLORS[t], fontWeight: 500 }}>{t}</span>
                </span>
              ))}
            </span>
          </div>
        )}

        {/* Category filter */}
        {categories.length > 1 && (
          <div style={{ marginBottom: 14 }}>
            <div style={{ fontSize: 11, letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 10 }}>Category</div>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              {categories.map(cat => (
                <FilterBtn key={cat} active={activeCat === cat} onClick={() => setActiveCat(cat)}>{cat}</FilterBtn>
              ))}
            </div>
          </div>
        )}

        {/* Source filter */}
        <div style={{ marginBottom: 28 }}>
          <div style={{ fontSize: 11, letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 10 }}>Source</div>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            {["All","onet","indian","hybrid"].map(src => {
              const color = src === "All" ? "var(--gold)" : SOURCE_COLORS[src];
              return (
                <FilterBtn key={src} active={activeSrc === src} color={color} onClick={() => setActiveSrc(src)}>
                  {src === "All" ? "All" : SOURCE_LABELS[src]}
                </FilterBtn>
              );
            })}
          </div>
        </div>

        {/* Cards / states */}
        {loading ? (
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 16, padding: "80px 0" }}>
            <div className="spinner" />
            <span style={{ fontSize: 14, color: "var(--muted)" }}>Finding aligned career paths…</span>
          </div>
        ) : error ? (
          <div style={{ textAlign: "center", padding: "80px 0" }}>
            <div style={{ fontSize: 32, marginBottom: 12 }}>⚠</div>
            <div style={{ fontSize: 15, color: "#c94c4c", marginBottom: 16 }}>{error}</div>
            <button className="btn-ghost" onClick={fetchCareers}>Retry</button>
          </div>
        ) : careers.length === 0 ? (
          <div style={{ textAlign: "center", padding: "80px 0" }}>
            <div style={{ fontSize: 32, marginBottom: 12 }}>🔍</div>
            <div style={{ fontSize: 15, color: "var(--muted)", marginBottom: 8 }}>
              No career matches were returned for your profile.
            </div>
            <div style={{ fontSize: 13, color: "var(--muted)", opacity: 0.7 }}>
              Try completing additional questions to sharpen your results.
            </div>
          </div>
        ) : filtered.length === 0 ? (
          <div style={{ textAlign: "center", padding: "80px 0" }}>
            <div style={{ fontSize: 32, marginBottom: 12 }}>🔍</div>
            <div style={{ fontSize: 15, color: "var(--muted)" }}>No careers match this filter.</div>
            <button className="btn-ghost" onClick={() => { setActiveCat("All"); setActiveSrc("All"); }} style={{ marginTop: 16 }}>
              Clear filters
            </button>
          </div>
        ) : filtered.map(career => (
          <CareerCard key={career.id} career={career} ocean_scores={ocean_scores} />
        ))}
      </div>
    </div>
  );
}