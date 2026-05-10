import { useEffect, useState } from "react";
import axios from "axios";
import { ArchetypeSummaryWithFeedback } from "./ArchetypeSummaryWithFeedback";

const BASE = import.meta.env.VITE_API_URL;
const LOW_CONFIDENCE_THRESHOLD = 0.55;


// ── Response normalisation ────────────────────────────────────────────────────

function extractRecommendations(data) {
  if (!data) return [];
  console.log("[Results] raw /careers/recommend response:", JSON.stringify(data).slice(0, 300));
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.careers)) return data.careers;
  if (Array.isArray(data.recommendations)) return data.recommendations;
  if (Array.isArray(data.matches)) return data.matches;
  if (Array.isArray(data.results)) return data.results;
  console.warn("[Results] unrecognised response shape. Keys:", Object.keys(data));
  return [];
}

function normalizeCareer(c) {
  if (!c || typeof c !== "object") return null;
  return {
    id: c.id || c.career_id || "",
    name: c.name || c.title || "Unknown",
    category: c.category || "",
    source: c.source || "onet",
    fit_score: c.fit_score != null ? c.fit_score : 0,
    description: c.description || c.explanation || "",
    explanation: c.explanation || c.description || "",
    entrance_exam: c.entrance_exam || null,
    work_style: Array.isArray(c.work_style) ? c.work_style : [],
    tags: Array.isArray(c.tags) ? c.tags : [],
    traits: c.traits || null,
    matched_traits: Array.isArray(c.matched_traits) ? c.matched_traits : [],
    mismatch_traits: Array.isArray(c.mismatch_traits) ? c.mismatch_traits : [],
  };
}

function normalizeScore(v) {
  if (v == null || Number.isNaN(v)) return 0;
  const n = Number(v);
  return Math.max(0, Math.min(100, n <= 1 ? Math.round(n * 100) : Math.round(n)));
}

function confidenceLabel(score) {
  if (score >= 0.8) return "High";
  if (score >= 0.6) return "Moderate";
  return "Low";
}

function clearAssessmentSession() {
  try { localStorage.removeItem("edwiserr_quiz_session"); } catch { }
}

// ── Archetype map (16 types) ──────────────────────────────────────────────────

const ARCHETYPES = [
  {
    key: "investigator",
    name: "The Investigator",
    description: "Analytical, research-oriented and deeply curious.",
    match: (s) => s.Openness >= 60 && s.Conscientiousness >= 60 && s.Extraversion <= 50,
    insights: [
      { title: "The Signal Hunter", body: "Where others see noise, you see structure. You don't just consume information — you interrogate it, cross-reference it, and won't rest until the pattern beneath reveals itself." },
      { title: "Depth Over Breadth", body: "You'd rather know one thing completely than a hundred things superficially. Mastery isn't a goal for you — it's a minimum standard." },
      { title: "Solitude as Fuel", body: "Your best thinking doesn't happen in meetings. It happens in the quiet hours when you can follow a thread without interruption. You protect that space fiercely." },
      { title: "Sceptical by Default", body: "You don't take claims at face value. Every assumption is a hypothesis waiting to be tested. This makes you an exceptionally rigorous thinker — and occasionally a difficult dinner guest." },
      { title: "Systems Before Action", body: "You're rarely the first to move — but when you do, it's because you've already mapped the terrain. Your decisions look slow from the outside and inevitable in hindsight." },
    ],
  },
  {
    key: "creator",
    name: "The Creator",
    description: "Imaginative, expressive and driven by ideas.",
    match: (s) => s.Openness >= 65 && s.Extraversion >= 60 && s.Conscientiousness <= 60,
    insights: [
      { title: "The Idea Factory", body: "Your brain doesn't idle. It generates, connects and reimagines constantly. The challenge was never having ideas — it's choosing which ones deserve your energy." },
      { title: "Expression as Necessity", body: "You don't create because it's productive. You create because not creating feels like holding your breath. Output is how you process the world." },
      { title: "Boredom as a Warning Signal", body: "The moment routine sets in, your attention starts searching for an exit. You need novelty the way others need stability — it's not a preference, it's a requirement." },
      { title: "Intuition-Led", body: "Your best work rarely starts with a plan. It starts with a feeling — an image, a phrase, an aesthetic pull — and the structure follows once the energy is alive." },
      { title: "Collaboration on Your Terms", body: "You work brilliantly with others when the creative latitude is real. The moment you feel constrained by someone else's vision, the quality of your contribution quietly drops." },
    ],
  },
  {
    key: "strategist",
    name: "The Strategist",
    description: "Vision-driven, ambitious and highly organized.",
    match: (s) => s.Openness >= 60 && s.Conscientiousness >= 60 && s.Extraversion >= 60,
    insights: [
      { title: "The Optimization Engine", body: "You don't just do tasks — you re-engineer them. Whether it's a workflow or a conversation, your default setting is to find the most efficient path from where you are to where you want to be." },
      { title: "Predictive Mapping", body: "Your brain runs simulations. Before a meeting, a negotiation or a project kick-off, you've already played out the five most likely scenarios. You rarely get surprised — only confirmed or recalibrated." },
      { title: "Long Game Thinking", body: "Short-term wins interest you only if they compound. You're always asking what this decision looks like in three years, not three weeks. This makes you invaluable in complex, slow-moving situations." },
      { title: "High Standards, High Friction", body: "You hold yourself and your environment to a demanding standard. This drives results — and occasionally drives people away. The gap between your vision and others' execution is a permanent source of tension." },
      { title: "Competence-Based Respect", body: "Titles don't impress you. Execution does. You'll follow someone with less seniority if they can actually deliver — and you'll quietly disengage from anyone who can't." },
    ],
  },
  {
    key: "connector",
    name: "The Connector",
    description: "Socially intuitive, empathetic and collaborative.",
    match: (s) => s.Extraversion >= 60 && s.Agreeableness >= 65,
    insights: [
      { title: "The Room Reader", body: "You pick up on social dynamics faster than most people notice them. Who's uncomfortable, who's performing, who's actually in charge — you clock it within minutes of entering a space." },
      { title: "Relationships as Infrastructure", body: "Your network isn't a list of contacts — it's a living system you actively maintain. You remember details, follow up without prompting and make people feel genuinely seen." },
      { title: "Trust as Currency", body: "You understand intuitively that trust takes longer to build than to break. You invest in it consistently — and you notice immediately when someone isn't doing the same." },
      { title: "Conflict Aversion Has a Cost", body: "Your instinct to preserve harmony sometimes delays necessary confrontations. The conversations you avoid tend to resurface — louder and harder — later." },
      { title: "Energy Through Others", body: "You don't just tolerate social interaction — you genuinely recharge through it. Isolation doesn't feel peaceful to you. It feels like something is missing." },
    ],
  },
  {
    key: "leader",
    name: "The Leader",
    description: "Decisive, commanding and action-oriented.",
    match: (s) => s.Extraversion >= 65 && s.Conscientiousness >= 60 && s.Agreeableness <= 60,
    insights: [
      { title: "Bias Toward Action", body: "Waiting for perfect information isn't your style. You make the best call available with what you have, move fast and correct course. Paralysis costs more than imperfect action." },
      { title: "Command Without Permission", body: "You don't need a title to lead. When a situation lacks direction, you naturally fill the vacuum. People follow because you project certainty — even when you're figuring it out." },
      { title: "High Decoupling", body: "You can dislike a person and still execute a project with them cleanly. Emotion and function occupy different compartments. This makes you effective — and occasionally seem cold." },
      { title: "Accountability as Identity", body: "You hold yourself to results, not effort. Excuses — even legitimate ones — feel like weakness to you. You expect the same standard from the people around you." },
      { title: "Loneliness at the Top", body: "The decisiveness that makes you effective also creates distance. People respect you more than they confide in you. That's a trade-off you've made — consciously or not." },
    ],
  },
  {
    key: "caregiver",
    name: "The Caregiver",
    description: "Supportive, dependable and people-focused.",
    match: (s) => s.Agreeableness >= 65 && s.Conscientiousness >= 60 && s.Openness <= 60,
    insights: [
      { title: "Stability as Service", body: "You don't just show up — you show up consistently, predictably and without drama. In a world that prizes novelty, your reliability is a rare and underrated superpower." },
      { title: "The Hidden Load", body: "You carry more than people realise — emotional labour, logistical coordination, the quiet acts of holding things together. Most of it goes unacknowledged. You do it anyway." },
      { title: "Difficulty Receiving", body: "You're far more comfortable giving support than asking for it. When someone offers help, your first instinct is to say you're fine. That instinct isn't always honest." },
      { title: "Loyalty With Limits", body: "Your commitment runs deep — but it isn't unconditional. When someone repeatedly takes without reciprocating, you don't announce your exit. You just quietly stop." },
      { title: "Systems of Care", body: "You think in routines, traditions and consistent practices. Not because you're uncreative — but because you understand that reliable structures are how people feel safe." },
    ],
  },
  {
    key: "analyst_type",
    name: "The Analyst",
    description: "Precise, disciplined and detail-oriented.",
    match: (s) => s.Conscientiousness >= 65 && s.Extraversion <= 50 && s.Openness <= 60,
    insights: [
      { title: "Zero Tolerance for Ambiguity", body: "Vague instructions aren't a minor inconvenience — they're a genuine obstacle. You need to understand the criteria before you can produce work you're proud of." },
      { title: "The Internal Auditor", body: "Before you submit anything, you've already reviewed it as your harshest critic. Your error rate is low not because you're lucky — because you've built a rigorous internal review process." },
      { title: "Slow Trust, Strong Trust", body: "You don't warm to people quickly. But once someone has earned your trust, you're one of the most reliable presences in their life. Your loyalty is hard-won and near-unbreakable." },
      { title: "Underpromise, Overdeliver", body: "You'd rather promise less and exceed expectations than overpromise and feel the pressure of an inflated commitment. Your credibility is too important to risk." },
      { title: "Invisibility of Excellence", body: "Your best work often goes unnoticed precisely because it's seamless. Problems you prevented, errors you caught, risks you mitigated — they don't make it into the meeting summary." },
    ],
  },
  {
    key: "advocate",
    name: "The Advocate",
    description: "Values-driven, diplomatic and thoughtful.",
    match: (s) => s.Openness >= 60 && s.Agreeableness >= 65 && s.Extraversion >= 55,
    insights: [
      { title: "The Principles Engine", body: "Your decisions aren't made from convenience — they're filtered through a values system that runs deeper than most people realise. You'll absorb significant cost rather than compromise something you believe in." },
      { title: "The Bridge Builder", body: "You have a rare ability to hold two opposing perspectives simultaneously without needing to immediately resolve them. This makes you an exceptional mediator — and sometimes an indecisive one." },
      { title: "Language as a Tool", body: "You choose words carefully. You know that how something is said shapes what it means, and you use that understanding to navigate difficult conversations with unusual precision." },
      { title: "Idealism Under Pressure", body: "You believe things can and should be better. This conviction is your engine — and your vulnerability. When systems repeatedly fail your ideals, the disillusionment hits hard." },
      { title: "Quiet Influence", body: "You rarely force your views. You plant them. You ask the right question, share the relevant story, create the space for someone to arrive at the insight themselves. It takes longer — and sticks more." },
    ],
  },
  {
    key: "performer",
    name: "The Performer",
    description: "Energetic, expressive and attention-driven.",
    match: (s) => s.Extraversion >= 65 && s.Openness >= 60 && s.Conscientiousness <= 55,
    insights: [
      { title: "The Presence Effect", body: "When you enter a room, the energy changes. You're not trying to dominate — it happens naturally. People orient toward you before you've said anything." },
      { title: "Live in the Moment", body: "Long-term planning competes with the intensity of what's happening right now. Your relationship with the future is optimistic but abstract. The present is where you actually live." },
      { title: "Audience as Amplifier", body: "You perform better when people are watching. Attention isn't just gratifying — it sharpens your output. An empty room brings out your average. A full one brings out your best." },
      { title: "Boredom Intolerance", body: "Repetitive tasks, slow processes and administrative detail drain you faster than almost anything. You're not lazy — you're misallocated. Put you in the right arena and the output is extraordinary." },
      { title: "The Reinvention Cycle", body: "You don't stay the same version of yourself for long. Interests shift, aesthetics evolve, identities update. What looks like inconsistency from the outside is actually an active process of becoming." },
    ],
  },
  {
    key: "builder",
    name: "The Builder",
    description: "Practical, structured and execution-focused.",
    match: (s) => s.Conscientiousness >= 65 && s.Openness >= 50 && s.Extraversion <= 55,
    insights: [
      { title: "The Completion Drive", body: "Starting things doesn't satisfy you — finishing them does. Half-built projects create a low-grade cognitive pressure that doesn't lift until the work is done and the standard is met." },
      { title: "Tangible Over Abstract", body: "You trust what you can measure, test and see. Grand theories that don't connect to practical outcomes feel like intellectual performance to you. Show you the mechanism." },
      { title: "Process as Protection", body: "Your systems and workflows aren't bureaucracy — they're accumulated wisdom. You've learned that reliable processes prevent the errors that cost you time, credibility and energy." },
      { title: "Quiet Confidence", body: "You don't announce your competence. You demonstrate it. The track record speaks — and you let it, rather than lobbying for recognition that should be self-evident." },
      { title: "Autonomy Non-Negotiable", body: "You work best when given a clear outcome and the freedom to determine how to reach it. Micromanagement doesn't just frustrate you — it actively degrades your output." },
    ],
  },
  {
    key: "stabiliser",
    name: "The Stabiliser",
    description: "Reliable, grounded and consistency-oriented.",
    match: (s) => s.Conscientiousness >= 60 && s.Agreeableness >= 65 && s.Openness <= 55,
    insights: [
      { title: "The Load-Bearing Wall", body: "You're often not the most visible person in a system — but you're the one everything else leans on. Remove you, and the structure becomes visible in the gaps." },
      { title: "Change as Disruption", body: "You're not opposed to improvement — you're opposed to change for its own sake. When something is working, the burden of proof is on the person who wants to upend it." },
      { title: "Depth of Commitment", body: "You don't commit lightly. But when you do, the follow-through is total. People who have your word have something worth more than a contract." },
      { title: "The Comfort You Provide", body: "People don't always articulate it, but they feel safer around you. Your steadiness regulates the anxiety of others — a function that's easy to take for granted and impossible to replace." },
      { title: "Slow Burn Resentment", body: "You absorb a lot without complaint. But pressure accumulates. When you finally reach your limit, the reaction surprises people who didn't notice the slow build. They should have been paying attention." },
    ],
  },
  {
    key: "explorer",
    name: "The Explorer",
    description: "Novelty-seeking, adventurous and adaptive.",
    match: (s) => s.Openness >= 65 && s.Extraversion >= 60 && s.Conscientiousness <= 50,
    insights: [
      { title: "The Horizon Problem", body: "The next thing always looks more interesting than the current thing. This isn't distraction — it's a genuine orientation toward possibility. The challenge is knowing when to stay." },
      { title: "Learning by Immersion", body: "You don't learn well from textbooks alone. You need to be in it — making mistakes, adjusting in real time, absorbing through experience rather than instruction." },
      { title: "Adaptability as Strength", body: "Environments that destabilise others energise you. Uncertainty isn't threatening — it's the condition in which you're most alive. Stability, paradoxically, makes you restless." },
      { title: "Commitment Ambivalence", body: "Long-term obligations feel heavier to you than they do to most. Not because you don't care — but because they constrain the optionality that feels essential to your wellbeing." },
      { title: "The Pattern Connector", body: "You synthesise across domains effortlessly. You've read widely, lived variously and thought about things that don't obviously connect — until, suddenly, they do. Your ideas have unusual range." },
    ],
  },
  {
    key: "reflector",
    name: "The Reflector",
    description: "Emotionally deep, introspective and sensitive.",
    match: (s) => s.Neuroticism >= 60 && s.Openness >= 55,
    insights: [
      { title: "The Inner Landscape", body: "Your emotional life is more textured than most people's. You experience things with an intensity that others find hard to access — which makes you more perceptive, and more vulnerable." },
      { title: "The Meaning Imperative", body: "Surface-level engagement isn't enough. You need to understand why things matter, what they connect to, what they say about the deeper structure beneath. Small talk feels like a missed opportunity." },
      { title: "Hypersensitivity to Tone", body: "You pick up on subtext, shifts in energy, things left unsaid. This gives you rare interpersonal insight — and an exhausting tendency to read situations that weren't meant to be read." },
      { title: "Creative Depth", body: "Your emotional range is a creative resource. The work you produce when you're able to channel what you feel — rather than suppress it — tends to resonate at a level most people can't manufacture." },
      { title: "Recovery Takes Time", body: "You don't bounce back quickly from difficult experiences. You process slowly and thoroughly. Forcing yourself to move on before you've finished processing doesn't work — it just delays the reckoning." },
    ],
  },
  {
    key: "guardian",
    name: "The Guardian",
    description: "Prepared, cautious and responsibility-driven.",
    match: (s) => s.Conscientiousness >= 55 && s.Neuroticism >= 60,
    insights: [
      { title: "Contingency as Comfort", body: "You feel safer when you've thought through what could go wrong. Having a backup plan isn't pessimism — it's the condition under which you can actually relax." },
      { title: "Responsibility as Identity", body: "When something is in your care, it stays in your care. You don't hand off and forget. You check, follow up and carry the outcome as yours until it's actually resolved." },
      { title: "Hypervigilance Has a Cost", body: "Your nervous system runs hot. You're constantly scanning for risk, managing for downside, preparing for disruption. The threat detection system that protects you also exhausts you." },
      { title: "Trust Through Track Record", body: "You don't extend trust based on warmth or impression. You extend it based on evidence. People who want your confidence need to demonstrate it through consistent, reliable behaviour over time." },
      { title: "The Anxiety-Competence Trade-Off", body: "Much of your anxiety is channelled into preparation and prevention. The worrying, paradoxically, produces the very competence that reassures others. The cost is yours alone to carry." },
    ],
  },
  {
    key: "inspirer",
    name: "The Inspirer",
    description: "Motivational, optimistic and idea-sharing.",
    match: (s) => s.Extraversion >= 60 && s.Openness >= 55 && s.Agreeableness >= 60,
    insights: [
      { title: "The Belief Transmitter", body: "You have an unusual ability to make people believe in something — including themselves. You don't just share ideas; you transfer the energy behind them." },
      { title: "Optimism as Operating System", body: "You default to possibility. This isn't naivety — it's a deliberate orientation that keeps you moving when more cautious people have already stopped. Problems are temporary. Potential is permanent." },
      { title: "The Enthusiasm Gap", body: "Your energy for an idea peaks at inception. Execution — the long, unglamorous middle — is where you need the most external support. Without it, great starts stay unfinished." },
      { title: "You Amplify Others", body: "People come away from conversations with you feeling more capable than before they arrived. You reflect their potential back at them in a way they struggle to see alone." },
      { title: "Overpromising Risk", body: "Your genuine enthusiasm sometimes writes cheques your follow-through can't cash. The gap between what you intend and what you deliver — even narrowly — erodes the trust you've worked hard to build." },
    ],
  },
  {
    key: "adaptive_generalist",
    name: "The Adaptive Generalist",
    description: "Flexible across environments with balanced tendencies.",
    match: () => true,
    insights: [
      { title: "Context Fluency", body: "You don't have a fixed operating mode. You read the room, adjust your approach and show up differently in different environments — not because you're inconsistent, but because you're genuinely adaptive." },
      { title: "The Generalist Advantage", body: "In a world of specialists, you're the person who can hold multiple perspectives simultaneously, translate between domains and see connections that narrow expertise misses." },
      { title: "Identity Under Pressure", body: "Because you adapt so readily, you sometimes wonder which version of you is the real one. The answer: all of them. Versatility isn't a lack of identity — it's a more complex form of it." },
      { title: "The Range Problem", body: "Your balanced profile means you don't have obvious outlier strengths — but you also have fewer obvious blind spots. You can function across more contexts than most, which is underrated until a situation demands it." },
      { title: "Finding Your Anchor", body: "Without a dominant drive, the question of what you're optimising for can feel unresolved. The work isn't finding your one thing — it's choosing which of your many genuine interests deserves the next chapter." },
    ],
  },
];
function getArchetype(scores) {
  const s = {
    Openness: scores.Openness || 0,
    Conscientiousness: scores.Conscientiousness || 0,
    Extraversion: scores.Extraversion || 0,
    Agreeableness: scores.Agreeableness || 0,
    Neuroticism: scores.Neuroticism || 0,
  };
  for (const arch of ARCHETYPES) {
    if (arch.match(s)) return arch;
  }
  return ARCHETYPES[ARCHETYPES.length - 1];
}

// ── Style helpers ─────────────────────────────────────────────────────────────

function card(extra = {}) {
  return {
    background: "var(--navy2, #0d1b2a)",
    border: "1px solid rgba(201,168,76,0.14)",
    borderRadius: "var(--radius, 14px)",
    padding: "28px",
    marginBottom: 20,
    ...extra,
  };
}

// ── Sub-components ────────────────────────────────────────────────────────────

function LowConfidenceNotice() {
  return (
    <div style={{ ...card({ padding: "16px 22px", marginBottom: 20 }), borderColor: "rgba(201,168,76,0.35)", background: "rgba(201,168,76,0.07)" }}>
      <div style={{ fontSize: 12, color: "var(--gold, #c9a84c)", marginBottom: 4 }}>⚠ Low confidence profile</div>
      <p style={{ fontSize: 13, color: "var(--muted, #8899aa)", margin: 0, lineHeight: 1.6 }}>
        Some responses were inconsistent or very quick. Results are indicative — consider retaking for a sharper picture.
      </p>
    </div>
  );
}

function OceanBar({ label, score }) {
  const pct = normalizeScore(score);
  const color = pct >= 70 ? "var(--gold, #c9a84c)" : pct >= 45 ? "var(--blue, #4c9ac9)" : "rgba(255,255,255,0.2)";
  return (
    <div style={{ marginBottom: 14 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 5, color: "var(--cream2, #c8d4e0)" }}>
        <span>{label}</span>
        <span style={{ color: "var(--muted, #8899aa)" }}>{pct}</span>
      </div>
      <div style={{ height: 5, borderRadius: 999, background: "rgba(255,255,255,0.06)", overflow: "hidden" }}>
        <div style={{ width: `${pct}%`, height: "100%", background: color, transition: "width 0.6s ease" }} />
      </div>
    </div>
  );
}

function PersonalityCareers({ ocean_scores }) {
  const traits = [
    { key: "Openness", label: "Openness" },
    { key: "Conscientiousness", label: "Conscientiousness" },
    { key: "Extraversion", label: "Extraversion" },
    { key: "Agreeableness", label: "Agreeableness" },
    { key: "Neuroticism", label: "Neuroticism" },
  ];
  return (
    <div style={card()}>
      <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted, #8899aa)", marginBottom: 16 }}>
        Personality Dimensions
      </div>
      {traits.map((t) => (
        <OceanBar key={t.key} label={t.label} score={ocean_scores?.[t.key] ?? 0} />
      ))}
    </div>
  );
}

function ArchetypeSummary({ archetype }) {
  return (
    <div style={card()}>
      <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted, #8899aa)", marginBottom: 16 }}>
        What this means for you
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        {archetype.insights.map((insight, i) => (
          <div key={i} style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
            <div style={{
              minWidth: 24, height: 24, borderRadius: "50%",
              background: "rgba(201,168,76,0.12)",
              border: "1px solid rgba(201,168,76,0.3)",
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 11, color: "var(--gold, #c9a84c)", fontWeight: 700,
              marginTop: 1, flexShrink: 0,
            }}>
              {i + 1}
            </div>
            <div>
              <div style={{ fontSize: 14, fontWeight: 600, color: "var(--cream, #e8dcc8)", marginBottom: 5, fontFamily: "'DM Serif Display', serif" }}>
                {insight.title}
              </div>
              <p style={{ fontSize: 13, color: "var(--muted, #8899aa)", margin: 0, lineHeight: 1.75 }}>
                {insight.body}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function DerivationNote({ overall }) {
  const pct = Math.round((overall ?? 0) * 100);
  return (
    <p style={{ fontSize: 13, color: "var(--muted, #8899aa)", margin: 0, lineHeight: 1.7 }}>
      Results are derived from a weighted OCEAN model across five personality dimensions.
      Overall confidence: <strong style={{ color: "var(--gold, #c9a84c)" }}>{pct}%</strong>.
    </p>
  );
}

function CareerTeaser({ career, rank, isLowConf }) {
  const fit = normalizeScore(career.fit_score);
  const fitColor = fit >= 90 ? "#4cc97a" : fit >= 80 ? "var(--gold, #c9a84c)" : "var(--blue, #4c9ac9)";
  const blurb = career.description || career.explanation || "";
  return (
    <div style={{ display: "flex", alignItems: "flex-start", gap: 16, padding: "14px 18px", background: "rgba(255,255,255,0.03)", border: "1px solid rgba(201,168,76,0.08)", borderRadius: 10 }}>
      <div style={{ minWidth: 42, textAlign: "center", fontFamily: "'DM Serif Display', serif", fontSize: 22, color: fitColor, lineHeight: 1 }}>
        {fit}
        <div style={{ fontSize: 9, color: "var(--muted, #8899aa)", textTransform: "uppercase" }}>fit</div>
      </div>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 15, color: "var(--cream, #e8dcc8)", fontFamily: "'DM Serif Display', serif", marginBottom: 4 }}>
          {rank}. {career.name}
        </div>
        {blurb && (
          <p style={{ fontSize: 12, color: "var(--muted, #8899aa)", margin: 0, lineHeight: 1.6 }}>
            {blurb.slice(0, 120)}{blurb.length > 120 ? "…" : ""}
          </p>
        )}
        {isLowConf && (
          <div style={{ fontSize: 11, color: "rgba(201,168,76,0.55)", marginTop: 4 }}>indicative only</div>
        )}
      </div>
    </div>
  );
}

function buildExport(profile, careers) {
  return {
    exported_at: new Date().toISOString(),
    profile,
    top_careers: careers.map((c) => ({ id: c.id, name: c.name, fit_score: c.fit_score, category: c.category })),
  };
}

// ── Results ───────────────────────────────────────────────────────────────────

export default function Results({ profile, userType, onCareersReady, onRetake }) {
  const [topCareers, setTopCareers] = useState([]);
  const [careerLoad, setCareerLoad] = useState(true);
  const [careerError, setCareerError] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    if (!profile?.ocean_scores) {
      setCareerLoad(false);
      return;
    }

    let cancelled = false;
    setCareerLoad(true);
    setCareerError(null);

    const payload = {
      ocean_scores: profile.ocean_scores,
      user_type: userType,
      top_n: 100,
      category_filter: null,
      source_filter: null,
      min_fit_score: 0,
    };

    console.log("[Results] POST payload:", payload);
    console.log("[Results] URL:", `${BASE}/careers/recommend`);

    axios
      .post(`${BASE}/careers/recommend`, payload)
      .then((r) => {
        if (cancelled) return;
        const raw = extractRecommendations(r.data);
        const recs = raw.map(normalizeCareer).filter(Boolean);
        console.log(`[Results] extracted ${recs.length} careers:`, recs.slice(0, 2));
        setTopCareers(recs);
        setCareerLoad(false);
      })
      .catch((err) => {
        if (cancelled) return;
        console.error("[Results] career fetch error:", err?.response?.data || err.message);
        setCareerError("Could not load career matches. Please try again.");
        setCareerLoad(false);
      });

    return () => { cancelled = true; };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  if (!profile) return null;

  const { ocean_scores, confidence, questions_answered } = profile;
  const archetype = getArchetype(ocean_scores || {});
  const overall = confidence?.overall ?? 0;
  const isLowConf = overall < LOW_CONFIDENCE_THRESHOLD;

  const handleRetake = () => {
    clearAssessmentSession();
    onRetake?.();
  };

  const handleViewCareers = () => {
    if (careerLoad || topCareers.length === 0) return;
    onCareersReady?.(topCareers);
  };

  const handleDownload = () => {
    const blob = new Blob(
      [JSON.stringify(buildExport(profile, topCareers), null, 2)],
      { type: "application/json" }
    );
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "edwiserr_profile.json";
    a.click();
    URL.revokeObjectURL(a.href);
  };

  return (
    <div className="results">

      <div className="results-header">
        <div className="section-eyebrow">Behavioral Profile Overview</div>
        <div className="results-archetype">
          <div className="results-archetype-label">Closest Current Pattern</div>
          <h2>{archetype.name}</h2>
          <p>{archetype.description}</p>
        </div>
        <h2 className="results-title">Profile Summary</h2>
        <p className="results-sub">{questions_answered ?? "—"} questions · 5 personality dimensions</p>
      </div>

      {isLowConf && <LowConfidenceNotice />}

      <PersonalityCareers ocean_scores={ocean_scores} />

      <ArchetypeSummaryWithFeedback
        archetype={archetype}
        responseSessionId={profile?.response_session_id}
        oceanScores={ocean_scores}
        userType={userType}
      />
      {console.log("archetype passed:", archetype)}

      <div style={card({ padding: "18px 24px" })}>
        <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted, #8899aa)", marginBottom: 6 }}>
          How these results are derived
        </div>
        <DerivationNote overall={overall} />
      </div>

      <div style={card()}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
          <div>
            <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted, #8899aa)", marginBottom: 4 }}>
              Career Alignment
            </div>
            <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 20, color: "var(--cream, #e8dcc8)" }}>
              Likely Fit Areas
            </div>
          </div>
          <button
            className="btn-primary"
            onClick={handleViewCareers}
            disabled={careerLoad || topCareers.length === 0}
            style={{ fontSize: 13, padding: "10px 20px" }}
          >
            {careerLoad ? "Loading…" : `Explore All (${topCareers.length})`}
          </button>
        </div>

        <p style={{ fontSize: 12, color: "var(--muted, #8899aa)", lineHeight: 1.6, marginBottom: 16 }}>
          These directions reflect environments and roles that tend to align with your behavioral patterns — not prescriptions for a fixed path.
        </p>

        {careerLoad ? (
          <div style={{ display: "flex", alignItems: "center", gap: 12, padding: "16px 0" }}>
            <div className="spinner" style={{ width: 24, height: 24 }} />
            <span style={{ fontSize: 13, color: "var(--muted, #8899aa)" }}>Finding aligned areas…</span>
          </div>
        ) : careerError ? (
          <p style={{ fontSize: 13, color: "#c94c4c" }}>{careerError}</p>
        ) : topCareers.length === 0 ? (
          <p style={{ fontSize: 13, color: "var(--muted, #8899aa)" }}>No strong alignment patterns emerged yet.</p>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {topCareers.slice(0, 5).map((career, i) => (
              <CareerTeaser key={career.id || i} career={career} rank={i + 1} isLowConf={isLowConf} />
            ))}
          </div>
        )}
      </div>

      <div className="results-actions" style={{ marginBottom: 32 }}>
        <button className="btn-ghost" onClick={handleRetake}>← Retake</button>
        <button
          className="btn-ghost"
          onClick={handleViewCareers}
          disabled={careerLoad || topCareers.length === 0}
        >
          Explore Careers →
        </button>
        <button className="btn-primary" onClick={handleDownload}>Download</button>
      </div>

      <div style={{ borderTop: "1px solid rgba(201,168,76,0.08)", paddingTop: 20, marginBottom: showDetails ? 0 : 40 }}>
        <button
          onClick={() => setShowDetails((v) => !v)}
          style={{ background: "transparent", border: "1px solid rgba(201,168,76,0.15)", borderRadius: 8, padding: "8px 18px", cursor: "pointer", fontSize: 12, color: "var(--muted, #8899aa)", display: "flex", alignItems: "center", gap: 8 }}
        >
          <span style={{ fontSize: 14 }}>{showDetails ? "🔒" : "🔓"}</span>
          {showDetails ? "Hide advanced details" : "Advanced details"}
        </button>

        {showDetails && (
          <div style={{ marginTop: 20 }}>
            <div style={card({ padding: "18px 22px" })}>
              <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted, #8899aa)", marginBottom: 12 }}>
                Raw OCEAN Scores
              </div>
              {ocean_scores && Object.entries(ocean_scores).map(([trait, score]) => (
                <div key={trait} style={{ display: "flex", justifyContent: "space-between", fontSize: 12, color: "var(--cream2, #c8d4e0)", padding: "4px 0", borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
                  <span>{trait}</span>
                  <span style={{ color: "var(--gold, #c9a84c)" }}>{typeof score === "number" ? score.toFixed(1) : score}</span>
                </div>
              ))}
            </div>

            {confidence && (
              <div style={card({ padding: "18px 22px" })}>
                <div style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted, #8899aa)", marginBottom: 12 }}>
                  Confidence Breakdown
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, color: "var(--cream2, #c8d4e0)", padding: "4px 0" }}>
                  <span>Overall</span>
                  <span style={{ color: "var(--gold, #c9a84c)" }}>{confidenceLabel(overall)} ({Math.round(overall * 100)}%)</span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

    </div>
  );
}