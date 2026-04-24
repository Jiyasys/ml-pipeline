# ============================================================
# EDWISERR — Career Recommendation Engine (Phase 2)
#
# Pipeline:
#   OCEAN scores → cosine similarity → filter by user_type
#   → rank → explain → return top N
#
# Explainability: every recommendation includes a reason string
# built from which traits drove the match (not a black box).
# ============================================================

import math
from careers.profiles import CAREERS, CAREER_LOOKUP, CATEGORIES

TRAITS = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']

TRAIT_DESCRIPTIONS = {
    'Openness':          ('curiosity and creative thinking',   'preference for structure'),
    'Conscientiousness': ('discipline and goal-orientation',   'flexibility and spontaneity'),
    'Extraversion':      ('social energy and assertiveness',   'independent focused work'),
    'Agreeableness':     ('empathy and people-focus',          'analytical directness'),
    'Neuroticism':       ('emotional sensitivity',              'stability under pressure'),
}

# ── Core maths ───────────────────────────────────────────────

def _cosine_similarity(v1: list, v2: list) -> float:
    dot  = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a ** 2 for a in v1))
    mag2 = math.sqrt(sum(b ** 2 for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)

def _ocean_to_vector(ocean: dict) -> list:
    return [ocean.get(t, 50.0) for t in TRAITS]

def _fit_score(user_ocean: dict, career_ocean: dict) -> float:
    u   = _ocean_to_vector(user_ocean)
    c   = _ocean_to_vector(career_ocean)
    sim = _cosine_similarity(u, c)
    return round(sim * 100, 1)

# ── Trait gap analysis ────────────────────────────────────────

def _trait_gaps(user_ocean: dict, career_ocean: dict) -> list:
    """
    Returns list of (trait, user_score, career_score, gap, direction)
    sorted by absolute gap descending.
    direction: 'above' = user above career, 'below' = user below career
    """
    gaps = []
    for trait in TRAITS:
        u = user_ocean.get(trait, 50.0)
        c = career_ocean.get(trait, 50.0)
        gap = u - c
        gaps.append((trait, u, c, abs(gap), 'above' if gap > 0 else 'below'))
    return sorted(gaps, key=lambda x: x[3], reverse=True)

# ── Explanation builder ───────────────────────────────────────

def _build_explanation(user_ocean: dict, career: dict, fit: float) -> str:
    """
    Generates a natural language explanation for why this career fits.
    Focuses on the 2 strongest matching traits and 1 development area.
    """
    career_ocean = career['ocean_profile']
    gaps         = _trait_gaps(user_ocean, career_ocean)

    # Strong matches: traits where user and career both score high (>60)
    # or both score low (<40), and gap is small (<15)
    strong_matches = []
    for trait, u, c, gap, direction in gaps:
        if gap < 15 and u > 60 and c > 60:
            high_desc = TRAIT_DESCRIPTIONS[trait][0]
            strong_matches.append(f"{trait.lower()} ({high_desc})")
        elif gap < 15 and u < 40 and c < 40:
            low_desc = TRAIT_DESCRIPTIONS[trait][1]
            strong_matches.append(f"{trait.lower()} ({low_desc})")

    # Development area: largest gap where user is below career requirement
    development = None
    for trait, u, c, gap, direction in gaps:
        if direction == 'below' and gap > 15 and c > 65:
            development = f"{trait} (career needs ~{int(c)}, you score {int(u)})"
            break

    # Build sentence
    parts = []
    if strong_matches:
        match_str = ' and '.join(strong_matches[:2])
        parts.append(f"Strong alignment on {match_str}.")
    if development:
        parts.append(f"Growth area: {development}.")
    if fit >= 90:
        parts.append("Excellent overall trait fit.")
    elif fit >= 80:
        parts.append("Good overall fit.")
    elif fit >= 70:
        parts.append("Moderate fit — some trait gaps exist.")

    return ' '.join(parts) if parts else f"Fit score: {fit}."

# ── Academic filter ───────────────────────────────────────────

def _passes_academic_filter(career: dict, user_type: str) -> bool:
    """Returns True if this career is appropriate for this user_type."""
    return user_type in career.get('user_types', [])

# ── Main recommender ──────────────────────────────────────────

def recommend_careers(
    ocean_scores: dict,
    user_type: str,
    top_n: int = 10,
    category_filter: str = None,
    source_filter: str = None,
    min_fit_score: float = 60.0,
) -> dict:
    """
    Core recommendation function.

    Args:
        ocean_scores    : {trait: score 0-100}
        user_type       : 'class_10' | 'class_12' | 'undergraduate' | 'professional'
        top_n           : number of careers to return
        category_filter : optional — filter to one category
        source_filter   : optional — 'onet' | 'indian' | 'hybrid'
        min_fit_score   : minimum fit score to include (0-100)

    Returns:
        dict with ranked recommendations + metadata
    """
    results = []

    for career in CAREERS:
        # Academic filter
        if not _passes_academic_filter(career, user_type):
            continue

        # Optional filters
        if category_filter and career['category'] != category_filter:
            continue
        if source_filter and career['source'] != source_filter:
            continue

        fit = _fit_score(ocean_scores, career['ocean_profile'])

        if fit < min_fit_score:
            continue

        explanation = _build_explanation(ocean_scores, career, fit)

        results.append({
            'id':            career['id'],
            'name':          career['name'],
            'category':      career['category'],
            'source':        career['source'],
            'description':   career['description'],
            'fit_score':     fit,
            'explanation':   explanation,
            'entrance_exam': career.get('entrance_exam'),
            'work_style':    career.get('work_style', []),
        })

    # Sort by fit score descending
    results.sort(key=lambda x: x['fit_score'], reverse=True)

    top = results[:top_n]

    # Dominant traits — what's driving this user's recommendations
    sorted_traits = sorted(ocean_scores.items(), key=lambda x: x[1], reverse=True)
    dominant      = [t for t, s in sorted_traits[:2] if s >= 60]
    low_traits    = [t for t, s in sorted_traits if s <= 40]

    return {
        'user_type':          user_type,
        'total_matched':      len(results),
        'top_n':              len(top),
        'dominant_traits':    dominant,
        'low_traits':         low_traits,
        'recommendations':    top,
        'categories_matched': sorted(set(r['category'] for r in top)),
    }


def get_career_detail(career_id: str, ocean_scores: dict) -> dict:
    """Returns full detail for a single career with fit analysis."""
    career = CAREER_LOOKUP.get(career_id)
    if not career:
        return {'error': f'Career {career_id} not found'}

    fit         = _fit_score(ocean_scores, career['ocean_profile'])
    explanation = _build_explanation(ocean_scores, career, fit)
    gaps        = _trait_gaps(ocean_scores, career['ocean_profile'])

    trait_breakdown = [
        {
            'trait':        t,
            'user_score':   round(u, 1),
            'career_ideal': round(c, 1),
            'gap':          round(gap, 1),
            'direction':    direction,
        }
        for t, u, c, gap, direction in gaps
    ]

    return {
        **career,
        'fit_score':       fit,
        'explanation':     explanation,
        'trait_breakdown': trait_breakdown,
    }