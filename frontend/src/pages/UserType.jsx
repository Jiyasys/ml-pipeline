const USER_TYPES = [
  {
    id: "class_10",
    icon: "📚",
    title: "Class 10 Student",
    desc: "Choosing your stream — Science, Commerce, or Arts. Let's find what fits you best.",
  },
  {
    id: "class_12",
    icon: "🎓",
    title: "Class 12 Student",
    desc: "Selecting a college and career path. We'll map your traits to the right degree.",
  },
  {
    id: "undergraduate",
    icon: "🔬",
    title: "Undergraduate Student",
    desc: "Mid-course or planning ahead. Discover your strongest career directions.",
  },
  {
    id: "professional",
    icon: "💼",
    title: "Working Professional",
    desc: "Career switch or reskilling. Understand what paths align with who you've become.",
  },
];

export default function UserType({ onSelect }) {
  return (
    <div className="usertype">
      <div className="usertype-header">
        <div className="section-eyebrow">Step 1 of 2</div>
        <h2 className="section-title">Who are you right now?</h2>
        <p className="section-sub">
          Your stage shapes the questions and recommendations.
        </p>
      </div>

      <div className="usertype-grid">
        {USER_TYPES.map((type) => (
          <div
            key={type.id}
            className="usertype-card"
            onClick={() => onSelect(type.id)}
          >
            <span className="card-icon">{type.icon}</span>
            <div className="card-title">{type.title}</div>
            <div className="card-desc">{type.desc}</div>
            <span className="card-arrow">→</span>
          </div>
        ))}
      </div>
    </div>
  );
}