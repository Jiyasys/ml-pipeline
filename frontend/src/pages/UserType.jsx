const USER_TYPES = [
  {
    id: "class_10",
    icon: "📚",
    title: "Class 10 Student",
    desc: "Exploring streams and future directions. The assessment adapts examples and emphasis to your current stage.",
  },
  {
    id: "class_12",
    icon: "🎓",
    title: "Class 12 Student",
    desc: "Considering degrees, entrance paths, and broader career possibilities aligned with your tendencies and interests.",
  },
  {
    id: "undergraduate",
    icon: "🔬",
    title: "Undergraduate Student",
    desc: "Exploring work styles, strengths, and environments that may align with your evolving goals and preferences.",
  },
  {
    id: "professional",
    icon: "💼",
    title: "Working Professional",
    desc: "Reflecting on career growth, transitions, or new directions based on your current behavioral patterns and work preferences.",
  },
];

export default function UserType({ onSelect }) {
  const handleKeyDown = (e, typeId) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      onSelect(typeId);
    }
  };

  return (
    <div className="usertype">
      <div className="usertype-header">
        <div className="section-eyebrow">
          Step 1 of 2
        </div>

        <h2 className="section-title">
          What stage are you currently in?
        </h2>

        <p className="section-sub">
          Your current context helps tailor question emphasis,
          examples, and career-alignment patterns.
        </p>
      </div>

      <div
        className="usertype-grid"
        role="list"
        aria-label="Select your current stage"
      >
        {USER_TYPES.map((type) => (
          <div
            key={type.id}
            role="button"
            tabIndex={0}
            aria-label={type.title}
            className="usertype-card"
            onClick={() => onSelect(type.id)}
            onKeyDown={(e) =>
              handleKeyDown(e, type.id)
            }
          >
            <span
              className="card-icon"
              aria-hidden="true"
            >
              {type.icon}
            </span>

            <div className="card-title">
              {type.title}
            </div>

            <div className="card-desc">
              {type.desc}
            </div>

            <span
              className="card-arrow"
              aria-hidden="true"
            >
              →
            </span>
          </div>
        ))}
      </div>

      <p
        style={{
          marginTop: 20,
          fontSize: 12,
          color: "var(--muted)",
          lineHeight: 1.7,
          textAlign: "center",
          maxWidth: 720,
          marginInline: "auto",
        }}
      >
        This assessment explores broader behavioral tendencies
        and work-style preferences. Results are intended as
        guidance, not fixed labels or definitive predictions.
      </p>
    </div>
  );
}