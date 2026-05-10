"""
confidence.py — Psychometric Confidence Scoring for Big Five (OCEAN) Assessment
================================================================================

WHY CRONBACH'S ALPHA IS NOT USED
---------------------------------
Cronbach's alpha requires a *sample of respondents* (rows = people, cols = items).
In a single-session assessment there is exactly one respondent, so:

  - Each item has exactly one observation  →  item variance = 0
  - α = (k/k−1) × (1 − 0/σ²_total) = k/(k−1)  →  always > 1  →  clamped to 1

This makes internal_consistency ≈ 1.0 regardless of response pattern, rendering
the entire confidence model meaningless.

WHAT IS USED INSTEAD: Single-Session Internal Consistency (SSIC)
-----------------------------------------------------------------
SSIC is composed of two statistically valid within-session signals:

  A) Intra-trait agreement (ITA) — per trait
     Measures how tightly a respondent's own answers cluster within a single trait.
     A genuinely high-scoring trait should produce answers that are close to each
     other; wide scatter within one trait signals ambivalence or careless responding.

     Formula:
       mean_i  = mean of item scores for trait t
       MAD_t   = mean(|x_j − mean_t|) for all items j in trait t
       ITA_t   = 1 − (MAD_t / MAX_MAD)
       MAX_MAD = 0.5  (maximum possible MAD on [0,1])

     Boundary cases:
       k < 2  →  ITA_t = 0.5  (insufficient data, neutral)
       All items equal  →  MAD = 0  →  ITA = 1.0

  B) Inter-trait discrimination (ITD) — global
     A respondent who answers identically across all traits provides no
     discriminant information.  High between-trait variance indicates genuine
     differentiation across personality dimensions.

     Formula:
       trait_means = [mean of answers] for each trait with ≥ 1 answer
       ITD = min(1.0, pop_std(trait_means) / ITD_TARGET_STD)
       ITD_TARGET_STD = 0.20  (std expected from a differentiating respondent)

     Boundary cases:
       < 2 traits answered        →  ITD = 0.5  (neutral)
       All trait means identical  →  std = 0  →  ITD = 0.0

  Final:
    internal_consistency = 0.6 × mean(ITA_t) + 0.4 × ITD
    consistency_t        = 0.7 × ITA_t + 0.3 × ITD

RESPONSE QUALITY — three equal-weight signals
  A) Response-time score  — per-question, ideal window 800–30 000 ms
  B) Straight-lining score — penalises longest run of identical answers
  C) IRV score             — penalises extreme low/high answer std deviation

SAMPLE SIZE CONFIDENCE
  sample_size_score = min(1.0, n_answered / 40)

FINAL WEIGHTING
  overall = 0.5 × internal_consistency + 0.3 × response_quality + 0.2 × sample_size
  per_trait_t = 0.7 × consistency_t + 0.3 × sample_size_score
"""

import math
import statistics

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TRAITS = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]

SHORT_TO_FULL: dict = {
    "O": "Openness",
    "C": "Conscientiousness",
    "E": "Extraversion",
    "A": "Agreeableness",
    "N": "Neuroticism",
}

# ITA: maximum possible mean-absolute-deviation for responses in [0, 1].
# Achieved when half of answers are 0 and half are 1.
ITA_MAX_MAD: float = 0.5

# ITD: std of trait means expected from a respondent who genuinely differentiates
# across OCEAN dimensions.  A realistic profile (e.g. O=0.7, C=0.6, E=0.4,
# A=0.8, N=0.3) has trait-mean std ≈ 0.18–0.22.  0.20 is the saturation point.
ITD_TARGET_STD: float = 0.20

# SSIC composition weights (must sum to 1)
W_ITA_GLOBAL: float = 0.6
W_ITD_GLOBAL: float = 0.4

# Per-trait consistency weights (must sum to 1)
W_ITA_TRAIT: float = 0.7
W_ITD_TRAIT: float = 0.3

# Response time bounds (milliseconds)
RT_IDEAL_MIN: int = 800
RT_IDEAL_MAX: int = 30_000
RT_IGNORE_ABOVE: int = 60_000

# Straight-lining
STRAIGHTLINE_SAFE_RUN: int = 4
STRAIGHTLINE_DECAY_SPAN: int = 6  # run=4 → score=1.0, run=10 → score=0.0

# IRV std range
IRV_IDEAL_MIN: float = 0.15
IRV_IDEAL_MAX: float = 0.35
# Theoretical max std for a [0,1]-bounded variable (50/50 split of 0 and 1)
IRV_MAX_STD: float = 0.5

# Overall confidence weights (must sum to 1)
W_CONSISTENCY: float = 0.5
W_QUALITY: float = 0.3
W_SAMPLE: float = 0.2

# Per-trait confidence weights (must sum to 1)
W_CONSISTENCY_TRAIT: float = 0.7
W_SAMPLE_TRAIT: float = 0.3

# Full-coverage question count
IDEAL_N_QUESTIONS: int = 40


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _mean(values: list) -> float:
    """Arithmetic mean; 0.0 for empty list."""
    return sum(values) / len(values) if values else 0.0


def _mad(values: list) -> float:
    """
    Mean absolute deviation from the mean.
    MAD = mean(|x_i − mean(x)|)
    Returns 0.0 for fewer than 2 values (single point has no spread).
    """
    if len(values) < 2:
        return 0.0
    m = _mean(values)
    return _mean([abs(v - m) for v in values])


def _pop_std(values: list) -> float:
    """
    Population standard deviation: sqrt(Σ(x−μ)²/n).
    Returns 0.0 for fewer than 2 values.
    """
    if len(values) < 2:
        return 0.0
    m = _mean(values)
    return math.sqrt(_mean([(v - m) ** 2 for v in values]))


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def _collect_trait_items(answers: dict, questions_used: list) -> dict:
    """
    Group answered question values by their OCEAN trait.
    Accepts both short ("O") and full ("Openness") trait labels.
    """
    items: dict = {t: [] for t in TRAITS}
    for q in questions_used:
        qid = q.get("id")
        if qid is None or qid not in answers:
            continue
        raw = q.get("trait", "")
        trait = SHORT_TO_FULL.get(raw, raw)
        if trait in items:
            items[trait].append(answers[qid])
    return items


# ---------------------------------------------------------------------------
# Component 1 — Single-Session Internal Consistency (SSIC)
# ---------------------------------------------------------------------------

def _intra_trait_agreement(items: list) -> float:
    """
    Intra-Trait Agreement (ITA) for one trait.

    Uses mean absolute deviation — a robust linear measure valid for n ≥ 1.

    ITA = 1 − (MAD / ITA_MAX_MAD)

    Why MAD instead of variance?
      Variance squares deviations, amplifying outlier answers.  MAD treats all
      deviations equally and has a natural maximum of 0.5 on [0,1] data,
      making normalisation exact with no distributional assumptions.
    """
    if len(items) < 2:
        return 0.5  # neutral: insufficient data
    return _clamp(1.0 - _mad(items) / ITA_MAX_MAD)


def _inter_trait_discrimination(trait_items: dict) -> float:
    """
    Inter-Trait Discrimination (ITD) — global signal.

    ITD = min(1.0, pop_std(trait_means) / ITD_TARGET_STD)

    Rewards profiles where trait means genuinely differ from each other.
    Returns neutral 0.5 when fewer than 2 traits have answers.
    """
    trait_means = [
        _mean(vals)
        for vals in trait_items.values()
        if vals
    ]
    if len(trait_means) < 2:
        return 0.5
    return _clamp(_pop_std(trait_means) / ITD_TARGET_STD)


def compute_internal_consistency(answers: dict, questions_used: list) -> tuple:
    """
    Compute Single-Session Internal Consistency (SSIC).

    Returns
    -------
    (overall_consistency, per_trait_consistency)
      overall_consistency   : float in [0, 1]
      per_trait_consistency : dict[trait, float in [0, 1]]
    """
    trait_items = _collect_trait_items(answers, questions_used)

    ita_per_trait: dict = {
        trait: _intra_trait_agreement(items)
        for trait, items in trait_items.items()
    }
    itd = _inter_trait_discrimination(trait_items)

    mean_ita = _mean(list(ita_per_trait.values()))
    overall = _clamp(W_ITA_GLOBAL * mean_ita + W_ITD_GLOBAL * itd)

    per_trait_consistency: dict = {
        trait: _clamp(W_ITA_TRAIT * ita_per_trait[trait] + W_ITD_TRAIT * itd)
        for trait in TRAITS
    }
    return overall, per_trait_consistency


# ---------------------------------------------------------------------------
# Component 2 — Response Quality
# ---------------------------------------------------------------------------

def _rt_score(answers: dict, response_times_ms: dict) -> float:
    """
    Per-question response-time score, averaged across all answered questions.

      rt in [RT_IDEAL_MIN, RT_IDEAL_MAX]         →  1.0
      rt < RT_IDEAL_MIN                          →  linear decay: rt / RT_IDEAL_MIN
      rt in (RT_IDEAL_MAX, RT_IGNORE_ABOVE]      →  linear decay toward 0
      rt > RT_IGNORE_ABOVE                       →  excluded (treated as missing)

    Returns 0.5 (neutral) when no valid timing data is available.
    """
    scores = []
    for qid in answers:
        raw = response_times_ms.get(qid)
        if raw is None:
            continue
        try:
            rt = int(raw)
        except (TypeError, ValueError):
            continue
        if rt > RT_IGNORE_ABOVE:
            continue
        if RT_IDEAL_MIN <= rt <= RT_IDEAL_MAX:
            scores.append(1.0)
        elif rt < RT_IDEAL_MIN:
            scores.append(_clamp(rt / RT_IDEAL_MIN))
        else:
            span = RT_IGNORE_ABOVE - RT_IDEAL_MAX
            scores.append(_clamp(1.0 - (rt - RT_IDEAL_MAX) / span))
    return _mean(scores) if scores else 0.5


def _straightlining_score(answer_values: list) -> float:
    """
    Penalises longest consecutive run of identical answers.

    run ≤ 4  →  1.0
    run > 4  →  max(0, 1 − (run − 4) / 6)
    """
    if not answer_values:
        return 1.0
    max_run = current_run = 1
    for i in range(1, len(answer_values)):
        if math.isclose(answer_values[i], answer_values[i - 1], abs_tol=1e-9):
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1
    if max_run <= STRAIGHTLINE_SAFE_RUN:
        return 1.0
    return _clamp(1.0 - (max_run - STRAIGHTLINE_SAFE_RUN) / STRAIGHTLINE_DECAY_SPAN)


def _irv_score(answer_values: list) -> float:
    """
    Inter-Response Variability score based on sample std deviation.

    std in [0.15, 0.35]  →  1.0
    std < 0.15           →  linear decay to 0 at std=0
    std > 0.35           →  linear decay to 0 at std=0.5 (theoretical max)

    Returns 0.5 (neutral) when fewer than 2 values are available.
    """
    if len(answer_values) < 2:
        return 0.5
    std = statistics.stdev(answer_values)
    if IRV_IDEAL_MIN <= std <= IRV_IDEAL_MAX:
        return 1.0
    elif std < IRV_IDEAL_MIN:
        return _clamp(std / IRV_IDEAL_MIN)
    else:
        span = IRV_MAX_STD - IRV_IDEAL_MAX
        return _clamp(1.0 - (std - IRV_IDEAL_MAX) / span)


def compute_response_quality(answers: dict, response_times_ms: dict) -> float:
    """
    Response quality score in [0, 1].

    Equal-weight mean of three behavioural signals:
      response_quality = (rt_score + straightlining_score + irv_score) / 3

    Returns 0.5 (neutral) on empty input.
    """
    if not answers:
        return 0.5
    values = list(answers.values())
    return (_rt_score(answers, response_times_ms) +
            _straightlining_score(values) +
            _irv_score(values)) / 3.0


# ---------------------------------------------------------------------------
# Component 3 — Sample Size Confidence
# ---------------------------------------------------------------------------

def compute_sample_size_score(answers: dict) -> float:
    """
    Coverage score: min(1.0, n_answered / IDEAL_N_QUESTIONS).

    Saturates at 1.0 once 40 or more questions have been answered.
    """
    return _clamp(len(answers) / IDEAL_N_QUESTIONS)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_confidence(
    answers: dict,
    questions_used: list,
    response_times_ms: dict,
) -> dict:
    """
    Compute a psychometric confidence score for a Big Five (OCEAN) assessment.

    Parameters
    ----------
    answers : dict
        {question_id: float (0–1)} — normalised item responses.
    questions_used : list
        List of question dicts.  Each must have:
          "id"    — matches a key in `answers`
          "trait" — "O"/"C"/"E"/"A"/"N" or the full OCEAN name
    response_times_ms : dict
        {question_id: int (ms)} — time taken per question.

    Returns
    -------
    {
      "overall": float,           # [0, 1]
      "per_trait": {              # [0, 1] per dimension
          "Openness":          float,
          "Conscientiousness": float,
          "Extraversion":      float,
          "Agreeableness":     float,
          "Neuroticism":       float,
      },
      "components": {
          "internal_consistency": float,   # SSIC  [0, 1]
          "response_quality":     float,   # RQ    [0, 1]
          "sample_size":          float,   # SSS   [0, 1]
      },
    }

    Never raises.  Always returns a complete, valid structure.
    """
    _zero: dict = {
        "overall": 0.0,
        "per_trait": {t: 0.0 for t in TRAITS},
        "components": {
            "internal_consistency": 0.0,
            "response_quality": 0.0,
            "sample_size": 0.0,
        },
    }

    if not isinstance(answers, dict) or not isinstance(questions_used, list):
        return _zero
    if not isinstance(response_times_ms, dict):
        response_times_ms = {}
    if not answers:
        return _zero

    # Sanitise: keep only finite floats in [0, 1]
    clean: dict = {}
    for qid, val in answers.items():
        try:
            f = float(val)
            if math.isfinite(f) and 0.0 <= f <= 1.0:
                clean[qid] = f
        except (TypeError, ValueError):
            pass

    if not clean:
        return _zero

    # ── Component 1: SSIC ────────────────────────────────────────────────
    consistency, per_trait_consistency = compute_internal_consistency(clean, questions_used)

    # ── Component 2: Response Quality ────────────────────────────────────
    quality = compute_response_quality(clean, response_times_ms)

    # ── Component 3: Sample Size ──────────────────────────────────────────
    sample = compute_sample_size_score(clean)

    # ── Overall confidence ────────────────────────────────────────────────
    overall = _clamp(W_CONSISTENCY * consistency + W_QUALITY * quality + W_SAMPLE * sample)

    # ── Per-trait confidence ──────────────────────────────────────────────
    per_trait: dict = {
        trait: _clamp(W_CONSISTENCY_TRAIT * per_trait_consistency[trait] + W_SAMPLE_TRAIT * sample)
        for trait in TRAITS
    }

    return {
        "overall": overall,
        "per_trait": per_trait,
        "components": {
            "internal_consistency": consistency,
            "response_quality": quality,
            "sample_size": sample,
        },
    }