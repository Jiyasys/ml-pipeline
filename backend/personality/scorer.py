"""
scorer.py — OCEAN Score Computation for Big Five Psychometric Assessment

Responsibility: answers → OCEAN scores (0–100) + confidence
Nothing else.  No interpretation, no classification.

Pipeline:
  raw answers (A/B/C/D)
    → encode_answers()       : map each answer to its question weight [0–1]
    → group_by_trait()       : bucket encoded values by OCEAN trait
    → compute_trait_scores() : mean per trait → scale to [0–100]
    → compute_confidence()   : imported from personality.confidence
    → build_profile()        : assemble final output dict
"""

from personality.questions import QUESTIONS
from personality.confidence import compute_confidence

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SHORT_TO_FULL: dict[str, str] = {
    "O": "Openness",
    "C": "Conscientiousness",
    "E": "Extraversion",
    "A": "Agreeableness",
    "N": "Neuroticism",
}

TRAITS: list[str] = list(SHORT_TO_FULL.values())

VALID_OPTIONS: frozenset[str] = frozenset({"A", "B", "C", "D"})

# Build a lookup from question id → question dict once at import time.
_Q_LOOKUP: dict[str, dict] = {q["id"]: q for q in QUESTIONS}


# ---------------------------------------------------------------------------
# Step 1 — Encode raw answers to float weights
# ---------------------------------------------------------------------------

def encode_answers(answers: dict) -> tuple[dict, list]:
    """
    Convert raw letter answers to per-question float weights.

    Parameters
    ----------
    answers : dict
        {question_id: 'A'|'B'|'C'|'D'}

    Returns
    -------
    encoded : dict
        {question_id: float (0–1)} — only for valid question/option pairs.
    questions_used : list
        Question dicts corresponding to every key in `encoded`.

    Invalid question IDs and invalid option letters are silently ignored.
    """
    encoded: dict[str, float] = {}
    questions_used: list[dict] = []

    for qid, option in answers.items():
        if option not in VALID_OPTIONS:
            continue
        question = _Q_LOOKUP.get(qid)
        if question is None:
            continue
        weight_key = f"weight_{option}"
        raw_weight = question.get(weight_key)
        if raw_weight is None:
            continue
        try:
            weight = float(raw_weight)
        except (TypeError, ValueError):
            continue

        if question.get("reverse", False):
         weight = 1.25 - weight

        encoded[qid] = weight
        questions_used.append(question)

    return encoded, questions_used


# ---------------------------------------------------------------------------
# Step 2 — Group encoded weights by OCEAN trait
# ---------------------------------------------------------------------------

def group_by_trait(encoded: dict, questions_used: list) -> dict[str, list[float]]:
    """
    Bucket encoded answer weights by their OCEAN trait.

    Parameters
    ----------
    encoded : dict
        {question_id: float} as returned by encode_answers().
    questions_used : list
        Parallel list of question dicts (same order is not required).

    Returns
    -------
    dict mapping each full trait name → list of float weights.
    Traits with no answers map to an empty list.

    Short trait codes ("O", "C", …) and full names ("Openness", …) are
    both accepted in the question's "trait" field.
    """
    groups: dict[str, list[float]] = {t: [] for t in TRAITS}

    for question in questions_used:
        qid = question.get("id")
        if qid not in encoded:
            continue
        raw_trait = question.get("trait", "")
        full_trait = SHORT_TO_FULL.get(raw_trait, raw_trait)
        if full_trait not in groups:
            continue
        groups[full_trait].append(encoded[qid])

    return groups


# ---------------------------------------------------------------------------
# Step 3 — Compute per-trait scores (0–100) and breakdown
# ---------------------------------------------------------------------------

def compute_trait_scores(groups: dict[str, list[float]]) -> tuple[dict, dict]:
    """
    Convert per-trait weight lists into OCEAN scores (0–100).

    Scoring:
      mean  = sum(weights) / count      [0–1]
      score = mean × 100                [0–100]
      score is clamped to [0, 100].

    Traits with zero answers receive a neutral score of 50.0.

    Parameters
    ----------
    groups : dict
        {full_trait_name: [float, ...]} as returned by group_by_trait().

    Returns
    -------
    ocean_scores : dict
        {trait: float (0–100)}
    trait_breakdown : dict
        {trait: {"mean": float (0–1), "count": int}}
    """
    ocean_scores: dict[str, float] = {}
    trait_breakdown: dict[str, dict] = {}

    for trait in TRAITS:
        values = groups.get(trait, [])
        count = len(values)

        if count == 0:
            mean_weight = 0.5   # neutral
            score = 50.0
        else:
            mean_weight = sum(values) / count
            score = max(0.0, min(100.0, mean_weight * 100.0))

        ocean_scores[trait] = round(score, 1)
        trait_breakdown[trait] = {
            "mean": round(mean_weight, 4),
            "count": count,
        }

    return ocean_scores, trait_breakdown


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_profile(
    user_type: str,
    inst_id: str,
    answers: dict,
    response_times_ms: dict,
) -> dict:
    """
    Convert raw assessment answers into a complete OCEAN profile.

    Parameters
    ----------
    user_type : str
        Caller-supplied user classification (stored verbatim in meta).
    inst_id : str
        Institution identifier (stored verbatim in meta).
    answers : dict
        {question_id: 'A'|'B'|'C'|'D'} — raw letter answers.
    response_times_ms : dict
        {question_id: int (ms)} — time taken per question.

    Returns
    -------
    {
      "ocean_scores": {
          "Openness":          float (0–100),
          "Conscientiousness": float (0–100),
          "Extraversion":      float (0–100),
          "Agreeableness":     float (0–100),
          "Neuroticism":       float (0–100),
      },
      "trait_breakdown": {
          <trait>: {"mean": float (0–1), "count": int},
          ...
      },
      "confidence": <output of compute_confidence()>,
      "meta": {
          "institution_id": str,
          "user_type":      str,
          "total_answered": int,
      },
    }

    Never raises.  Invalid answers and unknown question IDs are silently
    dropped; the function always returns a complete, valid structure.
    """
    # Guard: ensure inputs are the expected types
    if not isinstance(answers, dict):
        answers = {}
    if not isinstance(response_times_ms, dict):
        response_times_ms = {}

    # ── 1. Encode ────────────────────────────────────────────────────────
    encoded, questions_used = encode_answers(answers)

    # ── 2. Group ─────────────────────────────────────────────────────────
    groups = group_by_trait(encoded, questions_used)

    # ── 3. Score ─────────────────────────────────────────────────────────
    ocean_scores, trait_breakdown = compute_trait_scores(groups)

    # ── 4. Confidence ────────────────────────────────────────────────────
    confidence = compute_confidence(encoded, questions_used, response_times_ms)

    # ── 5. Assemble ──────────────────────────────────────────────────────
    return {
        "ocean_scores":    ocean_scores,
        "trait_breakdown": trait_breakdown,
        "confidence":      confidence,
        "meta": {
            "institution_id": inst_id,
            "user_type":      user_type,
            "total_answered": len(encoded),
        },
    }