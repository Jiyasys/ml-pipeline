const TRAIT_LABELS = {
  O: "Openness",
  C: "Conscientiousness",
  E: "Extraversion",
  A: "Agreeableness",
  N: "Neuroticism",
};

export default function Results({ data, onRetake }) {
  const { ocean_scores, mbti_display, confidence, needs_clarification } = data;

  return (
    <div style={styles.wrap}>
      <h2>Your Personality Profile</h2>

      <div style={styles.mbti}>{mbti_display}</div>
      <p style={styles.sub}>MBTI-style label (display only)</p>

      {needs_clarification && (
        <div style={styles.warning}>
          ⚠ Low confidence — follow-up questions recommended
        </div>
      )}

      <h3 style={{ marginTop: 32 }}>OCEAN Scores</h3>
      {Object.entries(ocean_scores).map(([trait, score]) => (
        <div key={trait} style={styles.traitRow}>
          <div style={styles.traitLabel}>
            <span>{TRAIT_LABELS[trait]}</span>
            <span>{score}%</span>
          </div>
          <div style={styles.barBg}>
            <div style={{ ...styles.barFill, width: `${score}%` }} />
          </div>
          <span style={styles.conf}>
            confidence: {confidence[trait]}
          </span>
        </div>
      ))}

      <p style={styles.overall}>Overall confidence: {confidence.overall}</p>

      <button onClick={onRetake} style={styles.btn}>Retake Quiz</button>
    </div>
  );
}

const styles = {
  wrap: { maxWidth: 520, margin: "60px auto", fontFamily: "sans-serif", padding: "0 16px" },
  mbti: { fontSize: 48, fontWeight: 700, color: "#4f46e5", textAlign: "center", marginTop: 16 },
  sub: { textAlign: "center", color: "#888", fontSize: 13, marginTop: 4 },
  warning: { background: "#fef3c7", border: "1px solid #f59e0b", borderRadius: 8, padding: "10px 16px", marginTop: 16 },
  traitRow: { marginBottom: 16 },
  traitLabel: { display: "flex", justifyContent: "space-between", fontSize: 14, marginBottom: 4 },
  barBg: { height: 10, background: "#e5e7eb", borderRadius: 4 },
  barFill: { height: "100%", background: "#4f46e5", borderRadius: 4 },
  conf: { fontSize: 11, color: "#aaa" },
  overall: { marginTop: 24, textAlign: "center", fontWeight: 600 },
  btn: { display: "block", margin: "24px auto 0", padding: "12px 32px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: 8, fontSize: 16, cursor: "pointer" },
};