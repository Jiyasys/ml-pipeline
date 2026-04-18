# ============================================================
# EDWISERR — OCEAN Scorer
# New scoring model: weight-based (not 1-5 Likert)
# User picks one option (A/B/C/D) per question
# Each option has a pre-assigned weight (0.0–1.0)
# Neuroticism is inverted — high weight = high distress
# ============================================================

from personality.questions import QUESTIONS, INVERTED_TRAITS
from statistics import stdev

Q_LOOKUP = {q['id']: q for q in QUESTIONS}

OPTION_KEYS = ['A', 'B', 'C', 'D']


def get_weight(question_id: str, chosen_option: str) -> float:
    """
    Returns the weight for the chosen option on a given question.
    chosen_option: 'A', 'B', 'C', or 'D'
    """
    q = Q_LOOKUP.get(question_id)
    if not q:
        raise ValueError(f"Question {question_id} not found")
    if chosen_option not in OPTION_KEYS:
        raise ValueError(f"Option must be A/B/C/D, got: {chosen_option}")
    return q[f'weight_{chosen_option}']


def compute_ocean_scores(answers: dict) -> dict:
    """
    answers: {question_id: chosen_option}  e.g. {"O1": "C", "ST1": "A"}
    Returns OCEAN scores normalised to 0–100.

    For Neuroticism: weight is inverted — high weight = high neurotic distress.
    We convert to a 0–100 score where 100 = emotionally stable (low Neuroticism).
    This makes all 5 traits directionally consistent:
      100 = high trait expression (Open, Conscientious, Extraverted, Agreeable, Stable)
    """
    trait_weights = {
        'Openness': [], 'Conscientiousness': [], 'Extraversion': [],
        'Agreeableness': [], 'Neuroticism': []
    }

    for qid, option in answers.items():
        q = Q_LOOKUP.get(qid)
        if not q:
            continue
        weight = q[f'weight_{option}']
        trait_weights[q['trait']].append(weight)

    ocean = {}
    for trait, weights in trait_weights.items():
        if not weights:
            ocean[trait] = 50.0
            continue
        avg = sum(weights) / len(weights)   # avg weight: 0.0–1.0
        score = avg * 100                   # normalise to 0–100

        # Neuroticism: invert so that 100 = emotionally stable
        if trait in INVERTED_TRAITS:
            score = 100 - score

        ocean[trait] = round(score, 1)

    return ocean


def ocean_to_mbti(ocean: dict) -> str:
    """Maps OCEAN scores to MBTI-style 4-letter label for display only."""
    return (
        ('E' if ocean['Extraversion']     >= 50 else 'I') +
        ('N' if ocean['Openness']         >= 50 else 'S') +
        ('F' if ocean['Agreeableness']    >= 50 else 'T') +
        ('J' if ocean['Conscientiousness']>= 50 else 'P')
    )


def compute_confidence(answers: dict) -> dict:
    """
    Measures response consistency within each trait.
    Low variance in chosen weights = consistent answers = high confidence.
    Returns per-trait confidence (0–1) and overall.
    """
    trait_weights = {
        'Openness': [], 'Conscientiousness': [], 'Extraversion': [],
        'Agreeableness': [], 'Neuroticism': []
    }

    for qid, option in answers.items():
        q = Q_LOOKUP.get(qid)
        if not q:
            continue
        trait_weights[q['trait']].append(q[f'weight_{option}'])

    confidence = {}
    for trait, weights in trait_weights.items():
        if len(weights) < 2:
            confidence[trait] = 0.5
            continue
        sd = stdev(weights)
        # Max possible std on 0.1–0.9 range ≈ 0.4
        confidence[trait] = round(max(0.0, 1.0 - (sd / 0.4)), 3)

    confidence['overall'] = round(
        sum(v for k, v in confidence.items() if k != 'overall') / 5, 3
    )
    return confidence


def build_profile(user_type: str, inst_id: str, answers: dict) -> dict:
    """
    Full pipeline: answers → OCEAN → MBTI label → confidence → profile object.
    answers: {question_id: chosen_option ('A'/'B'/'C'/'D')}
    """
    ocean      = compute_ocean_scores(answers)
    confidence = compute_confidence(answers)
    mbti       = ocean_to_mbti(ocean)

    return {
        'institution_id':      inst_id,
        'user_type':           user_type,
        'ocean_scores':        ocean,
        'mbti_display':        mbti,
        'confidence':          confidence,
        'needs_clarification': confidence['overall'] < 0.75,
        'questions_answered':  len(answers),
        'profile_complete':    True,
    }