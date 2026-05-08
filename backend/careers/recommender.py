# ============================================================
# EDWISERR — Career Recommendation Engine
#
# Pipeline:
#   OCEAN scores → validate → nonlinear weighted distance fit
#   → Neuroticism asymmetry → filter → true diversity interleave
#   → tie-break by alignment variance → explain → return top N
#
# Scoring model:
#   Nonlinear penalty: 1 - (distance/100)^0.7
#   Exponent < 1 is stricter at mid-range than the linear model.
#   distance=40 → 0.47 (vs 0.60 linear). A 40-point gap is now
#   genuinely costly, not a gentle nudge.
#
#   Neuroticism is scored asymmetrically: high user N matched
#   to a low-N career is capped, because high emotional
#   reactivity is rarely an asset in calm, low-pressure roles.
#
# Diversity:
#   Full two-pass soft-penalty selection. All ranked careers are
#   seen before any category adjustment is applied.
#
# Explainability:
#   Explanation uses work_style, confidence hedging, and
#   weighted-gap-sorted trait analysis.
#   Rationale metadata (matched_traits, mismatch_traits,
#   weighted_fit_breakdown) exposed per recommendation.
# ============================================================

from careers.profiles import CAREERS, CAREER_LOOKUP, REQUIRED_TRAITS

# ── Constants ─────────────────────────────────────────────────

DOMINANT_TRAIT_THRESHOLD = 65
LOW_TRAIT_THRESHOLD      = 35

# Diversity soft penalty
CATEGORY_PENALTY_START   = 3    # no penalty for first N entries from a category
CATEGORY_PENALTY_PER     = 4.0  # score points deducted for each entry beyond cap


# Score interpretation bands (tuned for nonlinear model)
_SCORE_BANDS: list[tuple[float, str]] = [
    (82, "This path appears to suit your profile quite well."),
    (68, "This path may especially suit the way you tend to think and work."),
    (55, "There is reasonable compatibility here, with some areas worth considering."),
    (0,  "This career involves meaningful trait differences from your current profile."),
]

TRAIT_DESCRIPTIONS: dict[str, tuple[str, str]] = {
    "Openness":          ("curiosity and creative thinking",  "preference for structure"),
    "Conscientiousness": ("discipline and goal-orientation",  "flexibility and adaptability"),
    "Extraversion":      ("social energy and assertiveness",  "independent, focused work"),
    "Agreeableness":     ("empathy and people-focus",         "analytical directness"),
    "Neuroticism":       ("emotional sensitivity",             "stability under pressure"),
}

_WORK_STYLE_PHRASES: dict[str, str] = {
    "analytical":     "analytical problem-solving",
    "creative":       "creative exploration",
    "leadership":     "leading and directing others",
    "collaborative":  "working closely with teams",
    "independent":    "autonomous, self-directed work",
    "technical":      "technical depth and precision",
    "research":       "inquiry-driven research",
    "social":         "frequent social interaction",
    "structured":     "structured, process-oriented environments",
    "hands_on":       "hands-on, applied work",
    "communication":  "communication and persuasion",
    "problem_solving":"tackling complex problems",
    "strategic":      "strategic thinking and planning",
    "artistic":       "artistic and aesthetic expression",
    "caregiving":     "supporting and caring for others",
    "entrepreneurial":"entrepreneurial initiative",
}


# ── Validation ────────────────────────────────────────────────

def _validate_ocean_scores(ocean_scores: dict) -> None:
    """
    Validate ocean_scores: all five traits present, numeric, in [0, 100].
    Raises ValueError with a clear message on any failure.
    No silent defaults — invalid input must never reach the scorer.
    """
    missing = set(REQUIRED_TRAITS) - ocean_scores.keys()
    if missing:
        raise ValueError(
            f"ocean_scores is missing required traits: {missing}. "
            f"All five traits must be provided: {REQUIRED_TRAITS}"
        )
    for trait in REQUIRED_TRAITS:
        val = ocean_scores[trait]
        if not isinstance(val, (int, float)):
            raise ValueError(
                f"ocean_scores['{trait}'] must be numeric, got {type(val).__name__}"
            )
        if not (0.0 <= val <= 100.0):
            raise ValueError(
                f"ocean_scores['{trait}'] = {val} is out of range [0, 100]"
            )


# ── Scoring ───────────────────────────────────────────────────
def _trait_similarity(user_score: float, career_score: float, trait: str) -> float:
    """
    Nonlinear per-trait similarity in [0.0, 1.0].

    Formula:
        similarity = 1 - (distance/100)^1.5

    Why exponent > 1:
    -------------------
    Using an exponent greater than 1 produces psychologically more
    realistic scoring behavior:

    - Small differences are tolerated
    - Medium differences become meaningfully costly
    - Large mismatches are heavily penalized

    Neuroticism asymmetry:
    ----------------------
    High emotional reactivity is often harder to compensate for in
    careers that strongly reward calmness and pressure stability.

    Instead of a hard threshold cap, we apply a gradual penalty when:
        user Neuroticism > career Neuroticism
    """

    distance = abs(user_score - career_score)

    similarity = max(
        0.0,
        1.0 - (distance / 100.0) ** 1.5
    )

    # Smooth Neuroticism asymmetry penalty
    if trait == "Neuroticism" and user_score > career_score:

        penalty_strength = (user_score - career_score) / 100.0

        similarity *= (1.0 - penalty_strength * 0.4)

    return similarity

# ── Trait gap analysis ────────────────────────────────────────

def _trait_gaps(user_ocean: dict, career: dict) -> list[dict]:
    """
    Per-trait gap dicts sorted by (weight * gap) descending.

    Sorting by weight*gap surfaces mismatches that are both large
    AND on high-importance traits — a medium-weight trait with a 50-point
    gap outranks a low-weight trait with a 30-point gap.

    Each dict:
        trait, user_score, career_ideal, gap, direction,
        weight, weighted_gap, similarity
    """
    weights = career["weights"]
    gaps = []

    for trait in REQUIRED_TRAITS:
        u = user_ocean[trait]
        c = career["ocean_profile"][trait]
        diff = u - c
        abs_gap = abs(diff)
        direction = "above" if diff > 0 else ("below" if diff < 0 else "match")

        gaps.append({
            "trait":        trait,
            "user_score":   round(u, 1),
            "career_ideal": round(c, 1),
            "gap":          round(abs_gap, 1),
            "direction":    direction,
            "weight":       weights[trait],
            "weighted_gap": round(weights[trait] * abs_gap, 2),
            "similarity":   round(_trait_similarity(u, c, trait), 3),
        })

    return sorted(gaps, key=lambda x: x["weighted_gap"], reverse=True)


# ── Explanation engine ────────────────────────────────────────

def _score_band_text(fit: float) -> str:
    for threshold, text in _SCORE_BANDS:
        if fit >= threshold:
            return text
    return _SCORE_BANDS[-1][1]


def _confidence_qualifier(
    confidence_scores: dict | None, traits: list[str]
) -> str:
    """
    Return a hedging phrase based on average confidence of the given traits.
    Lower confidence → more cautious language in the explanation.
    """
    if not confidence_scores:
        return ""
    values = [confidence_scores[t] for t in traits if t in confidence_scores]
    if not values:
        return ""
    avg = sum(values) / len(values)
    if avg < 0.5:
        return " (based on limited data — treat this as indicative)"
    if avg < 0.75:
        return " (confidence is moderate — worth exploring further)"
    return ""


def _build_explanation(
    user_ocean: dict,
    career: dict,
    fit: float,
    confidence_scores: dict | None = None,
) -> str:
    """
    Natural-language explanation for a career recommendation.

    Incorporates:
    - Strongest trait alignments (weighted_gap-sorted, so important traits first)
    - Work-style fit note (uses career's actual work_style tags)
    - Most significant mismatch (with direction context)
    - Confidence-adjusted hedging
    - Calibrated fit qualifier (band text tuned for nonlinear model)
    """
    gaps = _trait_gaps(user_ocean, career)
    work_styles = career.get("work_style", [])

    # Find up to 2 strong alignments on the highest-impact traits
    alignment_parts: list[str] = []
    aligned_traits: list[str] = []

    # Re-sort gaps by weight desc to prioritise important trait alignments
    gaps_by_weight = sorted(gaps, key=lambda g: g["weight"], reverse=True)

    for g in gaps_by_weight:
        trait = g["trait"]
        u, c, gap = g["user_score"], g["career_ideal"], g["gap"]

        both_high = gap <= 14 and u >= 58 and c >= 58
        both_low  = gap <= 14 and u <= 42 and c <= 42

        if both_high:
            aligned_traits.append(trait)
            alignment_parts.append(
                f"{trait.lower()} ({TRAIT_DESCRIPTIONS[trait][0]})"
            )
        elif both_low:
            aligned_traits.append(trait)
            alignment_parts.append(
                f"{trait.lower()} ({TRAIT_DESCRIPTIONS[trait][1]})"
            )

        if len(alignment_parts) >= 2:
            break

    # Work-style note: first style that has a human phrase
    style_note: str = ""
    for style in work_styles[:3]:
        phrase = _WORK_STYLE_PHRASES.get(style)
        if phrase:
            style_note = f"The role tends to reward {phrase}."
            break

    # Most impactful mismatch: largest weighted_gap where user is below career need
    mismatch: str = ""
    for g in gaps:    # already sorted by weighted_gap desc
        if g["direction"] == "below" and g["gap"] > 12 and g["career_ideal"] >= 62:
            mismatch = (
                f"One area to be aware of: {g['trait'].lower()} — "
                f"this path typically involves higher levels "
                f"(career profile ~{int(g['career_ideal'])}, "
                f"your score {int(g['user_score'])})."
            )
            break

    hedge = _confidence_qualifier(confidence_scores, aligned_traits or REQUIRED_TRAITS)

    parts: list[str] = []
    if alignment_parts:
        parts.append(f"Your profile aligns with {' and '.join(alignment_parts)}{hedge}.")
    if style_note:
        parts.append(style_note)
    if mismatch:
        parts.append(mismatch)
    parts.append(_score_band_text(fit))

    return " ".join(parts)


def _build_rationale(user_ocean: dict, career: dict) -> dict:
    """
    Structured rationale metadata for frontend explainability.

    Returns:
        matched_traits         — trait names with strong alignment
        mismatch_traits        — trait names with significant weighted mismatch
        weighted_fit_breakdown — list of {trait, similarity, weight, contribution}
    """
    gaps = _trait_gaps(user_ocean, career)   # sorted by weighted_gap desc
    matched: list[str] = []
    mismatched: list[str] = []
    breakdown: list[dict] = []

    for g in gaps:
        trait = g["trait"]
        u, c = g["user_score"], g["career_ideal"]
        sim, w = g["similarity"], g["weight"]

        breakdown.append({
            "trait":        trait,
            "similarity":   sim,
            "weight":       w,
            "contribution": round(w * sim * 100, 2),
        })

        both_high = g["gap"] <= 14 and u >= 58 and c >= 58
        both_low  = g["gap"] <= 14 and u <= 42 and c <= 42
        if both_high or both_low:
            matched.append(trait)
        elif g["weighted_gap"] >= 6.0 and g["gap"] >= 15:
            mismatched.append(trait)

    return {
        "matched_traits":         matched,
        "mismatch_traits":        mismatched,
        "weighted_fit_breakdown": breakdown,
    }


# ── Fit scoring ───────────────────────────────────────────────

def _fit_score(ocean_scores: dict, career: dict) -> float:
    """
    Calculate overall fit score for a career (0-100).

    Weighted sum of nonlinear per-trait similarities.
    """
    total_score = 0.0
    total_weight = 0.0

    weights = career["weights"]

    for trait in REQUIRED_TRAITS:
        user_score = ocean_scores[trait]
        career_score = career["ocean_profile"][trait]

        similarity = _trait_similarity(user_score, career_score, trait)
        weight = weights[trait]

        total_score += similarity * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return round((total_score / total_weight) * 100, 1)


def _alignment_variance(ocean_scores: dict, career: dict) -> float:
    """
    Calculate variance of per-trait similarities for tie-breaking.
    
    Lower variance indicates consistent alignment across traits.
    Higher variance indicates spiky alignment (good on some traits, poor on others).
    """
    gaps = _trait_gaps(ocean_scores, career)
    similarities = [g["similarity"] for g in gaps]
    
    if not similarities:
        return 0.0
    
    mean = sum(similarities) / len(similarities)
    variance = sum((s - mean) ** 2 for s in similarities) / len(similarities)
    
    return round(variance, 4)


# ── Filters ───────────────────────────────────────────────────

def _passes_academic_filter(career: dict, user_type: str) -> bool:
    return user_type in career.get("user_types", [])


# ── Diversity control ─────────────────────────────────────────
def _apply_diversity(
    ranked: list[dict],
    top_n: int,
    penalty_start: int = CATEGORY_PENALTY_START,
    penalty_per: float = CATEGORY_PENALTY_PER,
) -> list[dict]:
    """
    Diversity-aware reranking.

    Categories are penalised only during final selection,
    preventing dominant categories from unfairly suppressing
    lower-ranked careers before they are even considered.
    """

    selected: list[dict] = []
    category_counts: dict[str, int] = {}

    remaining = ranked.copy()

    while remaining and len(selected) < top_n:

        rescored = []

        for career in remaining:

            cat = career["category"]
            count = category_counts.get(cat, 0)

            excess = max(0, count - (penalty_start - 1))

            adjusted_score = career["fit_score"] - (excess * penalty_per)

            rescored.append((adjusted_score, career))

        rescored.sort(
            key=lambda x: (-x[0], x[1]["name"])
        )

        best = rescored[0][1]

        selected.append(best)

        cat = best["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

        remaining = [r for r in remaining if r["id"] != best["id"]]

    return selected

# ── Dominant / low trait analysis ─────────────────────────────

def _dominant_traits(ocean_scores: dict) -> list[str]:
    return [
        t for t, s in sorted(ocean_scores.items(), key=lambda x: x[1], reverse=True)
        if s >= DOMINANT_TRAIT_THRESHOLD
    ]


def _low_traits(ocean_scores: dict) -> list[str]:
    return [
        t for t, s in sorted(ocean_scores.items(), key=lambda x: x[1])
        if s <= LOW_TRAIT_THRESHOLD
    ]


# ── Main recommender ──────────────────────────────────────────

def recommend_careers(
    ocean_scores: dict,
    user_type: str,
    top_n: int = 10,
    category_filter: str | None = None,
    source_filter: str | None = None,
    min_fit_score: float = 50.0,
    confidence_scores: dict | None = None,
) -> dict:
    """
    Core recommendation function. Backward-compatible API contract preserved.

    Args:
        ocean_scores      : {trait: score 0-100} for all five OCEAN traits
        user_type         : 'class_10' | 'class_12' | 'undergraduate' | 'professional'
        top_n             : number of careers to return
        category_filter   : optional — restrict to one category
        source_filter     : optional — 'onet' | 'indian' | 'hybrid'
        min_fit_score     : minimum fit score to include (0-100)
        confidence_scores : optional {trait: confidence 0-1};
                            affects explanation hedging and output metadata

    Returns:
        dict with user_type, total_matched, top_n, dominant_traits,
        low_traits, recommendations, categories_matched.
        Each recommendation includes matched_traits, mismatch_traits,
        and weighted_fit_breakdown for frontend explainability.
    """
    _validate_ocean_scores(ocean_scores)

    results: list[dict] = []

    for career in CAREERS:
        if not _passes_academic_filter(career, user_type):
            continue
        if category_filter and career["category"] != category_filter:
            continue
        if source_filter and career["source"] != source_filter:
            continue

        fit = _fit_score(ocean_scores, career)
        if fit < min_fit_score:
            continue

        explanation = _build_explanation(ocean_scores, career, fit, confidence_scores)
        rationale   = _build_rationale(ocean_scores, career)
        variance    = _alignment_variance(ocean_scores, career)

        results.append({
            "id":            career["id"],
            "name":          career["name"],
            "category":      career["category"],
            "source":        career["source"],
            "description":   career["description"],
            "fit_score":     fit,
            "explanation":   explanation,
            "entrance_exam": career.get("entrance_exam"),
            "work_style":    career.get("work_style", []),
            # Rationale metadata
            "matched_traits":         rationale["matched_traits"],
            "mismatch_traits":        rationale["mismatch_traits"],
            "weighted_fit_breakdown": rationale["weighted_fit_breakdown"],
            # Internal tie-break key (stripped before output)
            "_variance": variance,
        })

    # Primary: fit_score desc | Secondary: variance asc (consistent > spiky) | Tertiary: name asc
    results.sort(key=lambda x: (-x["fit_score"], x["_variance"], x["name"]))
    for r in results:
        r.pop("_variance")

    top = _apply_diversity(results, top_n)

    output: dict = {
        "user_type":          user_type,
        "total_matched":      len(results),
        "top_n":              len(top),
        "dominant_traits":    _dominant_traits(ocean_scores),
        "low_traits":         _low_traits(ocean_scores),
        "recommendations":    top,
        "categories_matched": sorted(set(r["category"] for r in top)),
    }

    if confidence_scores is not None:
        valid = {
            t: v for t, v in confidence_scores.items()
            if isinstance(v, (int, float)) and 0.0 <= v <= 1.0
        }
        if valid:
            output["recommendation_confidence"] = round(
                sum(valid.values()) / len(valid), 3
            )
            output["low_confidence_traits"] = [t for t, v in valid.items() if v < 0.6]

    return output


# ── Career detail ─────────────────────────────────────────────

def get_career_detail(career_id: str, ocean_scores: dict) -> dict:
    """
    Full detail for a single career: fit score, explanation,
    per-trait breakdown (sorted by weighted_gap), and rationale metadata.
    """
    career = CAREER_LOOKUP.get(career_id)
    if not career:
        return {"error": f"Career '{career_id}' not found"}

    _validate_ocean_scores(ocean_scores)

    fit         = _fit_score(ocean_scores, career)
    explanation = _build_explanation(ocean_scores, career, fit)
    gaps        = _trait_gaps(ocean_scores, career)
    rationale   = _build_rationale(ocean_scores, career)

    return {
        **career,
        "fit_score":    fit,
        "explanation":  explanation,
        "trait_breakdown": [
            {
                "trait":        g["trait"],
                "user_score":   g["user_score"],
                "career_ideal": g["career_ideal"],
                "gap":          g["gap"],
                "direction":    g["direction"],
                "weight":       g["weight"],
                "weighted_gap": g["weighted_gap"],
                "similarity":   g["similarity"],
            }
            for g in gaps
        ],
        "matched_traits":         rationale["matched_traits"],
        "mismatch_traits":        rationale["mismatch_traits"],
        "weighted_fit_breakdown": rationale["weighted_fit_breakdown"],
    }