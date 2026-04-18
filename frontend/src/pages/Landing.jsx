export default function Landing({ onBegin }) {
  return (
    <div className="landing">
      <div className="landing-bg" />
      <div className="landing-grid" />

      <nav className="landing-nav">
        <div className="logo">EDWIS<span>err</span></div>
        <div className="nav-tag">AI Career Navigation</div>
      </nav>

      <section className="landing-hero">
        <div className="landing-eyebrow">
          Psychometric Assessment
        </div>

        <h1 className="landing-title">
          Understand<br />
          <em>who you are.</em>
        </h1>

        <p className="landing-subtitle">
          A science-backed personality assessment that maps your traits
          to the careers and paths most aligned with who you actually are —
          not who you think you should be.
        </p>

        <div className="landing-cta">
          <button className="btn-primary" onClick={onBegin}>
            Begin Assessment
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
          <span className="landing-cta-note">25 questions · ~8 minutes · No login required</span>
        </div>
      </section>

      <div className="landing-stats">
        <div className="stat">
          <div className="stat-number">5</div>
          <div className="stat-label">Personality Dimensions</div>
        </div>
        <div className="stat">
          <div className="stat-number">375</div>
          <div className="stat-label">Scenario Questions</div>
        </div>
        <div className="stat">
          <div className="stat-number">25</div>
          <div className="stat-label">Adaptive Questions</div>
        </div>
        <div className="stat">
          <div className="stat-number">900+</div>
          <div className="stat-label">Career Matches</div>
        </div>
      </div>
    </div>
  );
}