# ============================================================
# EDWISERR — Adaptive Question Selector
# Selects a balanced subset of questions per session.
# Default: 3 questions per sub-dimension = 15 per trait = 75 total
# Fast mode: 1 per sub-dimension = 5 per trait = 25 total
# ============================================================

import random
from personality.questions import QUESTIONS, SUB_DIMENSIONS, TRAITS

Q_LOOKUP = {q['id']: q for q in QUESTIONS}

# Sub-dimensions per trait
TRAIT_SUBDIMS = {}
for key in SUB_DIMENSIONS:
    trait, subdim = key.split('/', 1)
    TRAIT_SUBDIMS.setdefault(trait, []).append(subdim)

# User-type boosts: prioritise certain sub-dimensions
USER_TYPE_SUBDIM_BOOST = {
    'class_10': {
        'Openness':          ['Curiosity', 'Imagination'],
        'Conscientiousness': ['Planning', 'Discipline'],
        'Extraversion':      ['Social_Energy', 'Expressiveness'],
        'Agreeableness':     ['Empathy', 'Cooperation'],
        'Neuroticism':       ['Anxiety_Worry', 'Stress_Response'],
    },
    'class_12': {
        'Openness':          ['Intellectual_Exploration', 'Curiosity'],
        'Conscientiousness': ['Goal_Orientation', 'Planning'],
        'Extraversion':      ['Assertiveness', 'Leadership_Initiative'],
        'Agreeableness':     ['Cooperation', 'Trust'],
        'Neuroticism':       ['Stress_Response', 'Self_Doubt'],
    },
    'undergraduate': {
        'Openness':          ['Intellectual_Exploration', 'Preference_for_Novelty'],
        'Conscientiousness': ['Goal_Orientation', 'Responsibility'],
        'Extraversion':      ['Leadership_Initiative', 'Assertiveness'],
        'Agreeableness':     ['Conflict_Handling', 'Cooperation'],
        'Neuroticism':       ['Self_Doubt', 'Reaction_to_Failure'],
    },
    'professional': {
        'Openness':          ['Intellectual_Exploration', 'Creativity'],
        'Conscientiousness': ['Responsibility', 'Time_Management'],
        'Extraversion':      ['Leadership_Initiative', 'Assertiveness'],
        'Agreeableness':     ['Conflict_Handling', 'Helping_Behavior'],
        'Neuroticism':       ['Stress_Response', 'Emotional_Stability'],
    },
}


def select_questions(
    user_type: str = 'undergraduate',
    mode: str = 'standard',   # 'standard' (75Q) | 'fast' (25Q) | 'full' (375Q)
    seed: int = None
) -> list:
    """
    Returns a list of question dicts for the assessment session.

    Modes:
      full     → all 375 questions (15 per sub-dimension)
      standard → 75 questions (3 per sub-dimension)
      fast     → 25 questions (1 per sub-dimension)
    """
    if seed is not None:
        random.seed(seed)

    n_per_subdim = {'full': 15, 'standard': 3, 'fast': 1}.get(mode, 3)
    boosts = USER_TYPE_SUBDIM_BOOST.get(user_type, {})

    selected = []

    for trait in TRAITS:
        subdims = TRAIT_SUBDIMS.get(trait, [])

        # Sort subdims: boosted ones first
        boosted = boosts.get(trait, [])
        ordered_subdims = (
            [s for s in boosted if s in subdims] +
            [s for s in subdims if s not in boosted]
        )

        for subdim in ordered_subdims:
            key = f'{trait}/{subdim}'
            pool_ids = SUB_DIMENSIONS.get(key, [])
            pool = [Q_LOOKUP[qid] for qid in pool_ids if qid in Q_LOOKUP]

            # Shuffle for variety across sessions
            random.shuffle(pool)
            selected.extend(pool[:n_per_subdim])

    return selected


def select_clarification_questions(
    ocean_scores: dict,
    existing_answers: dict,
    n: int = 2
) -> list:
    """
    Returns n clarification questions for traits with lowest confidence.
    Picks questions not already answered.
    """
    answered_ids = set(existing_answers.keys())

    # Find 2 lowest-scoring traits (most uncertain)
    sorted_traits = sorted(ocean_scores.items(), key=lambda x: abs(x[1] - 50))
    target_traits = [t for t, _ in sorted_traits[:2]]

    clarification = []
    for trait in target_traits:
        # Pick 1 unanswered question from this trait
        pool = [q for q in QUESTIONS
                if q['trait'] == trait and q['id'] not in answered_ids]
        if pool:
            clarification.append(random.choice(pool))

    return clarification[:n]