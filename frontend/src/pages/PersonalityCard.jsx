// ============================================================
// EDWISERR — MBTI Personality Profiles
// 16 types with title, summary, and trait breakdowns
// Used in Results page PersonalityCard component
// ============================================================

export const MBTI_PROFILES = {

  INTJ: {
    title: "The Architect",
    tagline: "Visionary strategist. Independent. Razor-sharp.",
    summary: "An INTJ is a visionary strategist who values logic, efficiency, and independence above all else. Natural problem-solvers, they prefer working alone or in small, competent groups to turn complex ideas into reality. They don't just accept how things are done — they want to know why, and then find a better way.",
    traits: {
      Mindset:  "Driven by a constant desire to improve everything around them. They question systems, find inefficiencies, and build better ones.",
      Behavior: "Private and reserved, often appearing serious or aloof. Future-focused, spending most of their time analysing patterns in their own head.",
      Values:   "Prize competence, intelligence, and rationality. Little patience for social drama, inefficiency, or rules that exist for no reason.",
      "Inner World": "While they seem cold on the outside, they have a strong internal moral compass and deep loyalty to the people and projects they truly care about.",
    },
    closing: "A mastermind who looks at the world like a system to be optimised — using sharp intellect to build long-term plans and solve puzzles others find overwhelming.",
  },

  INTP: {
    title: "The Logician",
    tagline: "Precise thinker. Analytical. Endlessly curious.",
    summary: "An INTP is a relentless intellectual explorer who lives in the world of ideas, theories, and systems. They are driven by the need to understand how everything works at a fundamental level — not just the surface but the underlying logic.",
    traits: {
      Mindset:  "Everything is a puzzle to be solved. They love abstract ideas and theoretical frameworks, often thinking several layers deeper than most.",
      Behavior: "Quiet and introspective. They can appear distracted or detached, but internally they are in constant analytical motion.",
      Values:   "Intellectual honesty and accuracy above all. They will correct a wrong idea even if it makes the conversation uncomfortable.",
      "Inner World": "They feel emotions more than they show. Deep down they care about truth, fairness, and the people close to them — they just express it differently.",
    },
    closing: "An INTP is an ideas machine — most comfortable in the world of theory, most alive when cracking a problem no one else could untangle.",
  },

  ENTJ: {
    title: "The Commander",
    tagline: "Born leader. Decisive. Unstoppable drive.",
    summary: "An ENTJ is a natural born leader who sees the world as full of problems to fix and opportunities to capture. They move fast, think strategically, and expect others to keep up. They are built for ambition.",
    traits: {
      Mindset:  "Everything is a step in a larger plan. They think long-term, set ambitious goals, and drive hard toward them without losing sight of the bigger picture.",
      Behavior: "Assertive and direct. They take charge in any room they enter and are comfortable making tough calls under pressure.",
      Values:   "Efficiency, competence, and results. They respect people who deliver and have little patience for excuses or mediocrity.",
      "Inner World": "Behind the commanding exterior is a deep desire to build something meaningful and lasting — they lead not just to win, but to create.",
    },
    closing: "An ENTJ is a force of nature — combining strategic vision with relentless execution to turn ambitious ideas into real outcomes.",
  },

  ENTP: {
    title: "The Debater",
    tagline: "Idea generator. Challenger. Quick-minded.",
    summary: "An ENTP is a rapid-fire thinker who loves nothing more than a good intellectual challenge. They question everything, poke holes in arguments, and generate ideas faster than most people can process them.",
    traits: {
      Mindset:  "The world is full of interesting problems and untested ideas. They love exploring possibilities and are energised by debate and mental sparring.",
      Behavior: "Outgoing and quick-witted. They can argue any side of an issue convincingly — not to be right, but because the argument itself is fun.",
      Values:   "Innovation, originality, and intellectual freedom. They resist being boxed in by rules, routine, or conventional thinking.",
      "Inner World": "Beneath the bravado is someone who genuinely wants to make a difference — they just need the right problem big enough to hold their attention.",
    },
    closing: "An ENTP thrives at the intersection of ideas and action — most powerful when given a hard problem, a whiteboard, and the freedom to think without limits.",
  },

  INFJ: {
    title: "The Advocate",
    tagline: "Principled idealist. Empathetic. Quietly powerful.",
    summary: "An INFJ is a rare combination of deep empathy and iron conviction. They understand people at an intuitive level and are driven by a strong sense of purpose — they don't just want a good life, they want to make things better for others.",
    traits: {
      Mindset:  "See the world in terms of what it could be, not just what it is. They are idealistic but strategic, always thinking about the long-term human impact of decisions.",
      Behavior: "Quiet and reserved but intensely perceptive. They read people and situations with unusual accuracy.",
      Values:   "Authenticity, meaning, and doing what's right — even when it's hard. They cannot stand hypocrisy or cruelty.",
      "Inner World": "They feel everything deeply. Their empathy is a superpower but can also be exhausting — they absorb the emotions of people around them.",
    },
    closing: "An INFJ is a rare quiet force — driven by a vision of a better world and the empathy to actually make it happen.",
  },

  INFP: {
    title: "The Mediator",
    tagline: "Deeply feeling. Creative. Values-driven.",
    summary: "An INFP is a gentle idealist with a rich inner world and a deep commitment to their values. They are creative, empathetic, and quietly passionate — they care about authenticity above almost everything else.",
    traits: {
      Mindset:  "Everything connects to meaning. They ask not just 'what' but 'why' — and they need their life and work to feel genuinely purposeful.",
      Behavior: "Reflective and introspective. They often appear calm on the outside while processing a great deal internally.",
      Values:   "Authenticity, creativity, and compassion. They cannot tolerate being asked to act against their values — it feels physically wrong to them.",
      "Inner World": "Enormously rich and complex. They live in a world of ideas, feelings, and imagination that few people get to fully see.",
    },
    closing: "An INFP is a quiet creative force — most powerful when given the space to work on something that truly matters to them.",
  },

  ENFJ: {
    title: "The Protagonist",
    tagline: "Natural mentor. Inspiring. People-first.",
    summary: "An ENFJ is a charismatic leader who is genuinely energised by helping others grow. They see potential in people before those people see it in themselves — and they work tirelessly to help them reach it.",
    traits: {
      Mindset:  "The world gets better when people reach their full potential. They are always thinking about how to develop, inspire, and lift those around them.",
      Behavior: "Warm, expressive, and socially intuitive. They are natural communicators who connect deeply with almost everyone they meet.",
      Values:   "Harmony, growth, and genuine human connection. They feel personally responsible for the wellbeing of those they care about.",
      "Inner World": "They give so much of themselves to others that they sometimes neglect their own needs — their greatest challenge is allowing themselves to receive support too.",
    },
    closing: "An ENFJ is a catalyst for human growth — most fulfilled when the people around them are flourishing.",
  },

  ENFP: {
    title: "The Campaigner",
    tagline: "Boundlessly creative. Enthusiastic. People-energised.",
    summary: "An ENFP is a free spirit with a contagious enthusiasm for life. They are imaginative, deeply empathetic, and restless — always looking for the next big idea, connection, or adventure.",
    traits: {
      Mindset:  "Possibility is everywhere. They see connections others miss and get genuinely excited by ideas, people, and experiences that are new or unconventional.",
      Behavior: "Energetic, expressive, and spontaneous. They are the person who lights up a room — and then wonders what's happening in the next room.",
      Values:   "Creativity, authenticity, and deep human connection. They need their work and relationships to feel meaningful, not just transactional.",
      "Inner World": "Beneath the enthusiasm is a sensitive soul who feels things deeply and cares enormously about being understood and accepted.",
    },
    closing: "An ENFP is a creative engine with a human heart — most powerful when their imagination is pointed at something that genuinely matters.",
  },

  ISTJ: {
    title: "The Logistician",
    tagline: "Reliable. Detail-oriented. Built to deliver.",
    summary: "An ISTJ is the backbone of any organisation — dependable, thorough, and deeply committed to doing things properly. They take their responsibilities seriously and follow through on every commitment they make.",
    traits: {
      Mindset:  "If something is worth doing, it's worth doing right. They value accuracy, structure, and proven methods over novelty.",
      Behavior: "Reserved and methodical. They observe before acting, plan before executing, and prefer consistency over spontaneity.",
      Values:   "Duty, integrity, and reliability. They keep their word and expect the same from others — broken commitments feel like a personal affront.",
      "Inner World": "They show care through action, not words. Their loyalty and dedication run extremely deep even when they don't express it openly.",
    },
    closing: "An ISTJ is a pillar of dependability — the person you call when you need something done right, on time, without drama.",
  },

  ISFJ: {
    title: "The Defender",
    tagline: "Caring. Loyal. Quietly dedicated.",
    summary: "An ISFJ is a warm, devoted protector who finds deep fulfilment in caring for others. They are attentive to the needs of the people around them and work tirelessly behind the scenes to keep things running smoothly.",
    traits: {
      Mindset:  "People matter most. They are attuned to emotions, remember small details about the people they care about, and act on what they notice.",
      Behavior: "Quiet, consistent, and deeply reliable. They prefer familiar environments and build strong, lasting bonds over time.",
      Values:   "Loyalty, stability, and genuine care. They give generously without expecting recognition in return.",
      "Inner World": "They absorb stress quietly and rarely ask for help. Learning to set boundaries is often their most important personal growth challenge.",
    },
    closing: "An ISFJ is a quiet guardian — most at home when the people they love are safe, comfortable, and cared for.",
  },

  ESTJ: {
    title: "The Executive",
    tagline: "Organised. Direct. Gets things done.",
    summary: "An ESTJ is a natural administrator who brings order, structure, and momentum to everything they touch. They are decisive, practical, and willing to make tough calls to keep things moving forward.",
    traits: {
      Mindset:  "Systems work when everyone plays their role and pulls their weight. They set clear expectations and hold themselves and others to them.",
      Behavior: "Direct, confident, and action-oriented. They move quickly from decision to execution and prefer concrete results over abstract discussion.",
      Values:   "Tradition, responsibility, and order. They respect institutions, clear rules, and people who demonstrate reliability over time.",
      "Inner World": "They care deeply about the people in their lives but express it through acts of service and providing stability rather than emotional words.",
    },
    closing: "An ESTJ is a natural executor — most effective when they have a clear goal, a team they trust, and the authority to get things done.",
  },

  ESFJ: {
    title: "The Consul",
    tagline: "Warm. Socially intelligent. Community-builder.",
    summary: "An ESFJ is a people-person who finds genuine joy in bringing others together and making sure everyone feels included and valued. They are socially skilled, attuned to group dynamics, and deeply invested in harmony.",
    traits: {
      Mindset:  "Relationships are everything. They think constantly about how to support the people around them and make environments feel welcoming and positive.",
      Behavior: "Outgoing, attentive, and warm. They notice when someone is struggling and respond instinctively with support.",
      Values:   "Harmony, loyalty, and community. They work hard to maintain positive relationships and can feel genuinely distressed by conflict.",
      "Inner World": "Their deep need for approval can sometimes make it hard to hear criticism — their greatest growth comes from separating their self-worth from others' validation.",
    },
    closing: "An ESFJ is a social anchor — the person who remembers everyone's birthday, makes sure nobody feels left out, and holds groups together.",
  },

  ISTP: {
    title: "The Virtuoso",
    tagline: "Hands-on problem solver. Calm under pressure.",
    summary: "An ISTP is a practical, independent thinker who learns best by doing. They are fascinated by how things work and are at their best when they can get their hands on a problem and figure it out from first principles.",
    traits: {
      Mindset:  "Theory only matters if it works in practice. They are pragmatic, resourceful, and highly adaptable when things go wrong.",
      Behavior: "Quiet and self-contained. They observe carefully, act decisively, and rarely waste words.",
      Values:   "Efficiency, independence, and practical skill. They respect people who can actually do things, not just talk about them.",
      "Inner World": "They process emotions privately and can seem detached. But they are deeply loyal to people they trust and will show up reliably when it matters.",
    },
    closing: "An ISTP is a quiet expert — most alive when they are building, fixing, or cracking something the hard way.",
  },

  ISFP: {
    title: "The Adventurer",
    tagline: "Gentle. Artistic. Present-moment focused.",
    summary: "An ISFP is a gentle, creative soul who experiences the world through their senses and their feelings. They are spontaneous, open-minded, and deeply authentic — they live for experiences that feel real and meaningful.",
    traits: {
      Mindset:  "Life is meant to be experienced, not just planned. They focus on the present moment and find beauty and meaning in everyday things.",
      Behavior: "Quiet and reserved but warm with people they trust. They are non-judgmental and create safe spaces for others to be themselves.",
      Values:   "Authenticity, freedom, and beauty. They cannot tolerate feeling constrained or forced to act against who they genuinely are.",
      "Inner World": "They feel things deeply but keep much of it private. Their sensitivity is both their greatest strength and the thing they protect most carefully.",
    },
    closing: "An ISFP is a quiet creative — most alive when they are free to experience the world on their own terms and make something beautiful from it.",
  },

  ESTP: {
    title: "The Entrepreneur",
    tagline: "Action-first. Charismatic. Thrives under pressure.",
    summary: "An ESTP is a bold, energetic doer who lives in the moment and thrives on action. They are natural risk-takers who learn by jumping in and are at their best in fast-moving, high-stakes environments.",
    traits: {
      Mindset:  "Thinking without doing is pointless. They process the world through action and direct experience, not reflection.",
      Behavior: "Charismatic, confident, and persuasive. They are natural at reading people and situations in real time.",
      Values:   "Freedom, excitement, and results. They resist routine and conventional paths — they need to be where the action is.",
      "Inner World": "Beneath the bold exterior is someone who cares deeply about impact and being respected by the people they admire — even if they rarely show vulnerability.",
    },
    closing: "An ESTP is a live wire — most powerful in high-pressure moments where fast thinking, bold moves, and charm can turn the tide.",
  },

  ESFP: {
    title: "The Entertainer",
    tagline: "Energetic. Spontaneous. Genuinely people-loving.",
    summary: "An ESFP is a vibrant, spontaneous soul who brings energy, warmth, and fun to everything they do. They are natural performers who love people, live fully in the present, and make every experience more colourful.",
    traits: {
      Mindset:  "Life is meant to be enjoyed. They focus on the present and find genuine delight in connecting with people and experiencing new things.",
      Behavior: "Expressive, enthusiastic, and socially magnetic. They are the energy in the room and rarely meet a stranger.",
      Values:   "Joy, connection, and authentic experience. They have no interest in pretence — what you see is what you get.",
      "Inner World": "They are more emotionally sensitive than they appear. When they care about someone, they care deeply — and criticism from people they love cuts hard.",
    },
    closing: "An ESFP is pure human warmth — most alive when surrounded by people, possibility, and a good story to tell.",
  },
};

// ── PersonalityCard component ────────────────────────────────

export default function PersonalityCard({ mbtiType }) {
  const profile = MBTI_PROFILES[mbtiType];

  if (!profile) return null;

  const letters = mbtiType.split('');
  const letterMeanings = {
    E: "Extraverted", I: "Introverted",
    N: "Intuitive",  S: "Sensing",
    F: "Feeling",    T: "Thinking",
    J: "Judging",    P: "Perceiving",
  };

  return (
    <div style={{
      background: "var(--navy2)",
      border: "1px solid rgba(201,168,76,0.15)",
      borderRadius: "var(--radius-lg)",
      overflow: "hidden",
      marginBottom: 16,
    }}>
      {/* Header */}
      <div style={{
        background: "linear-gradient(135deg, rgba(201,168,76,0.12) 0%, rgba(13,27,42,0) 60%)",
        borderBottom: "1px solid rgba(201,168,76,0.1)",
        padding: "28px 28px 20px",
      }}>
        <div style={{ fontSize: 11, letterSpacing: "0.2em", textTransform: "uppercase", color: "var(--gold)", marginBottom: 8 }}>
          Your Personality Type
        </div>

        <div style={{ display: "flex", alignItems: "flex-end", gap: 16, flexWrap: "wrap", marginBottom: 12 }}>
          {/* MBTI letters */}
          <div style={{ display: "flex", gap: 4 }}>
            {letters.map(l => (
              <div key={l} style={{
                fontFamily: "'DM Serif Display', serif",
                fontSize: 36, color: "var(--gold)", lineHeight: 1,
              }}>
                {l}
              </div>
            ))}
          </div>

          <div>
            <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 22, color: "var(--cream)", marginBottom: 2 }}>
              {profile.title}
            </div>
            <div style={{ fontSize: 13, color: "var(--muted)", fontStyle: "italic" }}>
              {profile.tagline}
            </div>
          </div>
        </div>

        {/* Letter meanings */}
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          {letters.map(l => (
            <span key={l} style={{
              fontSize: 11, color: "var(--gold)",
              border: "1px solid rgba(201,168,76,0.25)",
              borderRadius: 4, padding: "3px 8px",
            }}>
              {l} — {letterMeanings[l]}
            </span>
          ))}
        </div>
      </div>

      {/* Summary */}
      <div style={{ padding: "20px 28px" }}>
        <p style={{ fontSize: 14, color: "var(--cream2)", lineHeight: 1.75, marginBottom: 20 }}>
          {profile.summary}
        </p>

        {/* Trait breakdown */}
        <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 20 }}>
          {Object.entries(profile.traits).map(([key, val]) => (
            <div key={key} style={{
              background: "rgba(201,168,76,0.04)",
              border: "1px solid rgba(201,168,76,0.08)",
              borderRadius: 8,
              padding: "12px 16px",
            }}>
              <div style={{ fontSize: 11, letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--gold)", marginBottom: 6 }}>
                {key}
              </div>
              <div style={{ fontSize: 13, color: "var(--cream2)", lineHeight: 1.65 }}>
                {val}
              </div>
            </div>
          ))}
        </div>

        {/* Closing */}
        <div style={{
          borderTop: "1px solid rgba(201,168,76,0.1)",
          paddingTop: 16,
          fontSize: 13,
          color: "var(--muted)",
          fontStyle: "italic",
          lineHeight: 1.7,
        }}>
          {profile.closing}
        </div>
      </div>
    </div>
  );
}