# ============================================================
# selector.py — Big Five (OCEAN) Question Selector
#
# Responsibilities:
#   - select_questions()              : balanced, deterministic session Q selection
#   - select_clarification_questions(): lowest-confidence trait clarification Qs
#
# This module handles ONLY question selection.
# No scoring, no personality interpretation, no recommendations.
# ============================================================

import random
from personality.questions import QUESTIONS, SUB_DIMENSIONS, TRAITS

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_SEED = 42

QUESTIONS_PER_SUBDIM = {
    "full":     15,
    "standard": 3,
    "fast":     1,
}

SHORT_TO_FULL = {
    "O": "Openness",
    "C": "Conscientiousness",
    "E": "Extraversion",
    "A": "Agreeableness",
    "N": "Neuroticism",
}

# Inverse map for normalisation (full names are identity-mapped)
_FULL_NAMES = set(SHORT_TO_FULL.values())


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _normalize_trait(name: str) -> str:
    """Return the canonical full trait name, or the input unchanged if unknown."""
    if name in _FULL_NAMES:
        return name
    return SHORT_TO_FULL.get(name, name)


def build_lookup() -> tuple[dict, dict]:
    """
    Build and return two lookup structures:

    q_by_id  : { question_id -> question_dict }
                O(1) access by ID; invalid IDs are simply absent.

    trait_subdim_pools : { (full_trait, subdim) -> [question_id, ...] }
                         Derived from SUB_DIMENSIONS; keys use full trait names.
                         Sub-dimension lists are sorted for stability.
    """
    q_by_id: dict = {q["id"]: q for q in QUESTIONS}

    trait_subdim_pools: dict = {}
    for key, qids in SUB_DIMENSIONS.items():
        if not isinstance(key, str) or "/" not in key:
            continue                         # skip malformed keys silently
        trait_raw, subdim = key.split("/", 1)
        trait = _normalize_trait(trait_raw)
        canonical_key = (trait, subdim)
        # Keep only IDs that exist in q_by_id; sort for deterministic base order
        valid_ids = sorted(qid for qid in qids if qid in q_by_id)
        trait_subdim_pools[canonical_key] = valid_ids

    return q_by_id, trait_subdim_pools


# Build once at import time
_Q_BY_ID, _TRAIT_SUBDIM_POOLS = build_lookup()

# Pre-compute sorted sub-dimension lists per trait (lexicographic, stable)
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
    mode: str = "standard",
    seed: int = None,
) -> list:
    """
    Select a balanced, deterministic subset of questions for one assessment session.

    Parameters
    ----------
    user_type : str
        Caller-supplied user type.  NOT used to bias selection in any way.
    mode : str
        "fast" | "standard" | "full".  Invalid values fall back to "standard".
    seed : int | None
        RNG seed.  None → DEFAULT_SEED (42).

    Returns
    -------
    list of question dicts, ordered by:
        TRAITS order → sub-dimension (lexicographic) → question order within subdim
    """
    # ── Resolve seed ──────────────────────────────────────────────────────────
    effective_seed = seed if seed is not None else DEFAULT_SEED

    # ── Resolve mode ─────────────────────────────────────────────────────────
    if mode not in QUESTIONS_PER_SUBDIM:
        import warnings
        warnings.warn(
            f"select_questions(): unknown mode {mode!r} — falling back to 'standard'.",
            stacklevel=2,
        )
    n_per_subdim = QUESTIONS_PER_SUBDIM.get(mode, QUESTIONS_PER_SUBDIM["standard"])

    # ── Tracking structures ───────────────────────────────────────────────────
    seen_ids: set = set()
    counts: dict = {}       # (trait, subdim) -> int  — O(1) increment
    selected: list = []

    # ── Iterate in stable order ───────────────────────────────────────────────
    for trait in TRAITS:
        full_trait = _normalize_trait(trait)
        subdims = _TRAIT_SUBDIMS_SORTED.get(full_trait, [])  # already sorted

        for subdim in subdims:
            counts[(full_trait, subdim)] = 0

            pool_ids = _TRAIT_SUBDIM_POOLS.get((full_trait, subdim), [])
            if not pool_ids:
                continue

            # Per-(trait, subdim) local RNG — never touches global state
            rng = random.Random(f"{effective_seed}:{full_trait}:{subdim}")
            shuffled = pool_ids[:]          # copy; don't mutate the lookup
            rng.shuffle(shuffled)

            for qid in shuffled:
                if counts[(full_trait, subdim)] >= n_per_subdim:
                    break
                if qid in seen_ids:
                    continue
                # qid is guaranteed in _Q_BY_ID (filtered at build_lookup time)
                selected.append(_Q_BY_ID[qid])
                seen_ids.add(qid)
                counts[(full_trait, subdim)] += 1   # O(1)

    return selected


def select_clarification_questions(
    confidence: dict,
    existing_answers: dict,
    n: int = 2,
) -> list:
    """
    Return up to n clarification questions for the traits with lowest confidence.

    Parameters
    ----------
    confidence : dict
        Must contain a "per_trait" sub-dict mapping trait names → confidence scores.
        Trait names may be short ("O") or full ("Openness").
    existing_answers : dict
        Keys are question IDs already answered; those questions are excluded.
    n : int
        Maximum number of questions to return.

    Returns
    -------
    list of question dicts (deterministic, no randomness).
    """
    # ── Input guards ──────────────────────────────────────────────────────────
    if not isinstance(confidence, dict):
        confidence = {}
    if not isinstance(existing_answers, dict):
        existing_answers = {}

    per_trait: dict = confidence.get("per_trait", {})
    if not isinstance(per_trait, dict):
        per_trait = {}

    # ── Normalize trait names in confidence dict ──────────────────────────────
    normalised_confidence: dict = {
        _normalize_trait(t): v for t, v in per_trait.items()
    }

    # ── Rank traits by ascending confidence (most uncertain first) ────────────
    ranked_traits = [
        trait for trait, _ in sorted(
            normalised_confidence.items(), key=lambda kv: kv[1]
        )
        if trait in _FULL_NAMES          # only known traits
    ]

    # ── Excluded IDs ─────────────────────────────────────────────────────────
    excluded_ids: set = set(existing_answers.keys())

    # ── Select questions, rotating across sub-dimensions ─────────────────────
    selected: list = []
    seen_ids: set = set()

    for full_trait in ranked_traits:
        if len(selected) >= n:
            break

        subdims = _TRAIT_SUBDIMS_SORTED.get(full_trait, [])  # lexicographic order

        # Build per-subdim pools of unused questions (sorted IDs for stability)
        subdim_pools: dict = {}
        for subdim in subdims:
            pool = [
                qid for qid in sorted(_TRAIT_SUBDIM_POOLS.get((full_trait, subdim), []))
                if qid not in excluded_ids and qid not in seen_ids
            ]
            if pool:
                subdim_pools[subdim] = pool

        # Rotate across sub-dimensions: pick one from each in turn
        while subdim_pools and len(selected) < n:
            for subdim in sorted(subdim_pools.keys()):   # stable iteration order
                if len(selected) >= n:
                    break
                pool = subdim_pools[subdim]
                if not pool:
                    del subdim_pools[subdim]
                    continue
                qid = pool.pop(0)           # first unused (sorted → deterministic)
                if not pool:
                    del subdim_pools[subdim]
                selected.append(_Q_BY_ID[qid])
                seen_ids.add(qid)
            else:
                # All remaining pools exhausted for this trait
                break

    return selected