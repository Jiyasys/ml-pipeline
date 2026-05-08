export default function Landing({ onBegin }) {
  return (
    <div className="landing">
      <div className="landing-bg" />
      <div className="landing-grid" />

      <nav className="landing-nav">
        <div className="logo">
          EDWIS<span>err</span>
        </div>
        <div className="nav-tag">Trait-Based Career Navigation</div>
      </nav>

      <section className="landing-hero">
        <div className="landing-eyebrow">
          Adaptive Personality Assessment
        </div>

        <h1 className="landing-title">
          Discover<br />
          <em>your strongest patterns.</em>
        </h1>

        <p className="landing-subtitle">
          A data-driven personality assessment that maps your behavioral traits,
          working style, and natural tendencies to career paths that may align
          well with you — helping you explore possibilities with greater clarity.
        </p>

        <div
          style={{
            marginTop: 18,
            fontSize: 13,
            lineHeight: 1.7,
            color: "var(--muted)",
            maxWidth: 620,
          }}
        >
          Adaptive questioning helps improve reliability as you answer, and
          recommendations are intended as exploratory guidance — not fixed or
          definitive labels.
        </div>

        <div className="landing-cta">
          <button className="btn-primary" onClick={onBegin}>
            Begin Assessment
            <svg
              width="16"
              height="16"
              viewBox="0 0 16 16"
              fill="none"
            >
              <path
                d="M3 8h10M9 4l4 4-4 4"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>

          <span className="landing-cta-note">
            25 adaptive questions · ~8 minutes · No login required
          </span>
        </div>
      </section>

      <div className="landing-stats">
        <div className="stat">
          <div className="stat-number">5</div>
          <div className="stat-label">Core Personality Dimensions</div>
        </div>

        <div className="stat">
          <div className="stat-number">375</div>
          <div className="stat-label">Question Assessment Bank</div>
        </div>

        <div className="stat">
          <div className="stat-number">25</div>
          <div className="stat-label">Adaptive Questions Per Session</div>
        </div>

        <div className="stat">
          <div className="stat-number">900+</div>
          <div className="stat-label">Career Path Matches</div>
        </div>
      </div>
    </div>
  );
}