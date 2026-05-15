# personality/selector.py
# ============================================================
# Big Five (OCEAN) Question Selector
#
# Fix: seed is now random per session (not hardcoded to 42).
# Each session gets 1 random question per sub-dimension = 25 total.
# No student ever sees the same set twice.
# ============================================================

import random
from personality.questions import QUESTIONS, SUB_DIMENSIONS, TRAITS

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

QUESTIONS_PER_SUBDIM = {
    "full":     5,   # all 5 questions per sub-dimension
    "standard": 2,   # 2 per sub-dimension = 50 total
    "fast":     1,   # 1 per sub-dimension = 25 total  ← your quiz mode
}

SHORT_TO_FULL = {
    "O": "Openness",
    "C": "Conscientiousness",
    "E": "Extraversion",
    "A": "Agreeableness",
    "N": "Neuroticism",
}

_FULL_NAMES = set(SHORT_TO_FULL.values())


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _normalize_trait(name: str) -> str:
    if name in _FULL_NAMES:
        return name
    return SHORT_TO_FULL.get(name, name)


def build_lookup() -> tuple[dict, dict]:
    q_by_id: dict = {q["id"]: q for q in QUESTIONS}

    trait_subdim_pools: dict = {}
    for key, qids in SUB_DIMENSIONS.items():
        if not isinstance(key, str) or "/" not in key:
            continue
        trait_raw, subdim = key.split("/", 1)
        trait = _normalize_trait(trait_raw)
        canonical_key = (trait, subdim)
        valid_ids = sorted(qid for qid in qids if qid in q_by_id)
        trait_subdim_pools[canonical_key] = valid_ids

    return q_by_id, trait_subdim_pools


_Q_BY_ID, _TRAIT_SUBDIM_POOLS = build_lookup()

_TRAIT_SUBDIMS_SORTED: dict = {}
for (_trait, _subdim) in _TRAIT_SUBDIM_POOLS:
    _TRAIT_SUBDIMS_SORTED.setdefault(_trait, []).append(_subdim)
for _trait in _TRAIT_SUBDIMS_SORTED:
    _TRAIT_SUBDIMS_SORTED[_trait].sort()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def select_questions(
    user_type: str,
    mode: str = "fast",
    seed: int | None = None,          # None = truly random per session
) -> list:
    """
    Select a balanced set of questions for one quiz session.

    mode="fast"  → 1 question per sub-dimension = 25 questions total
    mode="standard" → 2 per sub-dimension = 50 total
    mode="full"  → 5 per sub-dimension = 125 total

    seed=None (default) → different questions every session  ✅
    seed=int            → reproducible set (for testing only)
    """
    # ── Resolve mode ─────────────────────────────────────────
    if mode not in QUESTIONS_PER_SUBDIM:
        import warnings
        warnings.warn(
            f"select_questions(): unknown mode {mode!r} — falling back to 'fast'.",
            stacklevel=2,
        )
    n_per_subdim = QUESTIONS_PER_SUBDIM.get(mode, QUESTIONS_PER_SUBDIM["fast"])

    # ── Resolve seed ──────────────────────────────────────────
    # None → random; a provided int is used as-is (testing / replay)
    effective_seed = seed  # random.Random(None) uses OS entropy

    # ── Selection ─────────────────────────────────────────────
    seen_ids: set = set()
    selected: list = []

    for trait in TRAITS:
        full_trait = _normalize_trait(trait)
        subdims = _TRAIT_SUBDIMS_SORTED.get(full_trait, [])

        for subdim in subdims:
            pool_ids = _TRAIT_SUBDIM_POOLS.get((full_trait, subdim), [])
            if not pool_ids:
                continue

            # Each (trait, subdim) gets its own RNG instance.
            # seed=None → random.Random() uses OS entropy → unique every call
            rng = random.Random(
                f"{effective_seed}:{full_trait}:{subdim}"
                if effective_seed is not None
                else None          # truly random
            )

            shuffled = pool_ids[:]
            rng.shuffle(shuffled)

            count = 0
            for qid in shuffled:
                if count >= n_per_subdim:
                    break
                if qid in seen_ids:
                    continue
                selected.append(_Q_BY_ID[qid])
                seen_ids.add(qid)
                count += 1

    return selected


def select_clarification_questions(
    confidence: dict,
    existing_answers: dict,
    n: int = 2,
) -> list:
    """
    Return up to n clarification questions for the traits with lowest confidence.
    Excludes questions already answered in the session.
    """
    if not isinstance(confidence, dict):
        confidence = {}
    if not isinstance(existing_answers, dict):
        existing_answers = {}

    per_trait: dict = confidence.get("per_trait", {})
    if not isinstance(per_trait, dict):
        per_trait = {}

    normalised_confidence: dict = {
        _normalize_trait(t): v for t, v in per_trait.items()
    }

    ranked_traits = [
        trait for trait, _ in sorted(
            normalised_confidence.items(), key=lambda kv: kv[1]
        )
        if trait in _FULL_NAMES
    ]

    excluded_ids: set = set(existing_answers.keys())
    selected: list = []
    seen_ids: set = set()

    for full_trait in ranked_traits:
        if len(selected) >= n:
            break

        subdims = _TRAIT_SUBDIMS_SORTED.get(full_trait, [])

        subdim_pools: dict = {}
        for subdim in subdims:
            pool = [
                qid for qid in sorted(_TRAIT_SUBDIM_POOLS.get((full_trait, subdim), []))
                if qid not in excluded_ids and qid not in seen_ids
            ]
            if pool:
                subdim_pools[subdim] = pool

        while subdim_pools and len(selected) < n:
            for subdim in sorted(subdim_pools.keys()):
                if len(selected) >= n:
                    break
                pool = subdim_pools[subdim]
                if not pool:
                    del subdim_pools[subdim]
                    continue
                qid = pool.pop(0)
                if not pool:
                    del subdim_pools[subdim]
                selected.append(_Q_BY_ID[qid])
                seen_ids.add(qid)
            else:
                break

    return selected