export function getArchetype(scores) {
  const O = scores.Openness || 0;
  const C = scores.Conscientiousness || 0;
  const E = scores.Extraversion || 0;
  const A = scores.Agreeableness || 0;
  const N = scores.Neuroticism || 0;

  // 1
  if (O >= 75 && C >= 75 && E <= 45) {
    return {
      name: "The Investigator",
      description:
        "Analytical, research-oriented and deeply curious.",
    };
  }

  // 2
  if (O >= 75 && E >= 65 && C <= 55) {
    return {
      name: "The Creator",
      description:
        "Imaginative, expressive and driven by ideas.",
    };
  }

  // 3
  if (O >= 70 && C >= 70 && E >= 65) {
    return {
      name: "The Strategist",
      description:
        "Vision-driven, ambitious and highly organized.",
    };
  }

  // 4
  if (E >= 75 && A >= 70) {
    return {
      name: "The Connector",
      description:
        "Socially intuitive, empathetic and collaborative.",
    };
  }

  // 5
  if (E >= 75 && C >= 75 && A <= 55) {
    return {
      name: "The Leader",
      description:
        "Decisive, commanding and action-oriented.",
    };
  }

  // 6
  if (A >= 80 && C >= 70 && O <= 55) {
    return {
      name: "The Caregiver",
      description:
        "Supportive, dependable and people-focused.",
    };
  }

  // 7
  if (C >= 85 && E <= 45 && O <= 65) {
    return {
      name: "The Analyst",
      description:
        "Precise, disciplined and detail-oriented.",
    };
  }

  // 8
  if (O >= 70 && A >= 70 && E >= 55) {
    return {
      name: "The Advocate",
      description:
        "Values-driven, diplomatic and thoughtful.",
    };
  }

  // 9
  if (E >= 80 && O >= 70 && C <= 50) {
    return {
      name: "The Performer",
      description:
        "Energetic, expressive and attention-driven.",
    };
  }

  // 10
  if (C >= 80 && O >= 55 && E <= 50) {
    return {
      name: "The Builder",
      description:
        "Practical, structured and execution-focused.",
    };
  }

  // 11
  if (C >= 75 && A >= 75 && O <= 50) {
    return {
      name: "The Stabiliser",
      description:
        "Reliable, grounded and consistency-oriented.",
    };
  }

  // 12
  if (O >= 80 && E >= 70 && C <= 45) {
    return {
      name: "The Explorer",
      description:
        "Novelty-seeking, adventurous and adaptive.",
    };
  }

  // 13
  if (N >= 75 && O >= 70) {
    return {
      name: "The Reflector",
      description:
        "Emotionally deep, introspective and sensitive.",
    };
  }

  // 14
  if (C >= 70 && N >= 70) {
    return {
      name: "The Guardian",
      description:
        "Prepared, cautious and responsibility-driven.",
    };
  }

  // 15
  if (E >= 70 && O >= 65 && A >= 65) {
    return {
      name: "The Inspirer",
      description:
        "Motivational, optimistic and idea-sharing.",
    };
  }

  // 16
  return {
    name: "The Adaptive Generalist",
    description:
      "Flexible across environments with balanced tendencies.",
  };
}