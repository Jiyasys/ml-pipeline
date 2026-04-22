# ============================================================
# EDWISERR — OCEAN Scorer + Confidence Engine
# Pillar 1 : Internal Consistency  (Cronbach's Alpha)
# Pillar 2 : Behavioral Quality    (RT + Straight-lining + IRV)
# Pillar 3 : Statistical Stability (stubbed — needs calibration data)
#
# Master formula:
#   Confidence(trait) = 0.40 × C1  +  0.35 × C2  +  0.25 × C3
#   Confidence(overall) = mean across all 5 traits
# ============================================================

import math
from statistics import mean, stdev
from personality.questions import QUESTIONS, INVERTED_TRAITS

Q_LOOKUP    = {q['id']: q for q in QUESTIONS}
OPTION_KEYS = ['A', 'B', 'C', 'D']

W1, W2, W3 = 0.40, 0.35, 0.25   # pillar weights

TRAITS = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']

# ── Helpers ──────────────────────────────────────────────────

def _clamp(val, lo=0.0, hi=1.0):
    return max(lo, min(hi, val))

def _get_weight(qid: str, option: str) -> float:
    return float(Q_LOOKUP[qid][f'weight_{option}'])

def _longest_run(seq) -> int:
    if not seq:
        return 0
    max_run = cur = 1
    for i in range(1, len(seq)):
        cur = cur + 1 if seq[i] == seq[i - 1] else 1
        max_run = max(max_run, cur)
    return max_run

def _trait_weights(answers: dict) -> dict:
    """Returns {trait: [weight, ...]} for all answered questions."""
    tw = {t: [] for t in TRAITS}
    for qid, opt in answers.items():
        q = Q_LOOKUP.get(qid)
        if q and opt in OPTION_KEYS:
            tw[q['trait']].append(_get_weight(qid, opt))
    return tw

# ── OCEAN Scoring ────────────────────────────────────────────

def compute_ocean_scores(answers: dict) -> dict:
    """
    answers: {question_id: 'A'|'B'|'C'|'D'}
    Returns OCEAN scores 0–100.
    Neuroticism inverted: 100 = emotionally stable.
    """
    tw = _trait_weights(answers)
    ocean = {}
    for trait, weights in tw.items():
        if not weights:
            ocean[trait] = 50.0
            continue
        score = (sum(weights) / len(weights)) * 100
        if trait in INVERTED_TRAITS:
            score = 100 - score
        ocean[trait] = round(score, 1)
    return ocean

def ocean_to_mbti(ocean: dict) -> str:
    return (
        ('E' if ocean['Extraversion']      >= 50 else 'I') +
        ('N' if ocean['Openness']          >= 50 else 'S') +
        ('F' if ocean['Agreeableness']     >= 50 else 'T') +
        ('J' if ocean['Conscientiousness'] >= 50 else 'P')
    )

# ── Pillar 1: Internal Consistency (Cronbach's Alpha) ────────

def _cronbach_alpha(weights: list) -> float:
    """
    Estimates Cronbach's alpha using the inter-item correlation proxy:
        α ≈ (k × r̄) / (1 + (k-1) × r̄)
    where r̄ is estimated from within-trait weight spread.
    Low spread = high internal consistency.
    """
    k = len(weights)
    if k < 2:
        return 0.65   # neutral — not enough items to measure

    if len(set(weights)) == 1:
        return 1.0   # all identical → perfect consistency

    weight_std = stdev(weights)
    # Max meaningful std on 0.1–0.9 weight scale ≈ 0.4
    r_bar = _clamp(1.0 - (weight_std / 0.4))
    alpha = (k * r_bar) / (1 + (k - 1) * r_bar) if (1 + (k - 1) * r_bar) > 0 else 0.0
    return _clamp(float(alpha))

def compute_c1_consistency(answers: dict) -> dict:
    """
    Per-trait alpha → mapped to 0–1:
        C1 = clamp((α - 0.50) / 0.40, 0, 1)
    α=0.50 → C1=0.0 | α=0.70 → C1=0.5 | α=0.90 → C1=1.0
    """
    tw = _trait_weights(answers)
    c1_scores, alphas = {}, {}
    for trait, weights in tw.items():
        alpha           = _cronbach_alpha(weights)
        alphas[trait]   = round(alpha, 3)
        c1_scores[trait] = round(_clamp((alpha - 0.50) / 0.40), 3)
    return {'scores': c1_scores, 'alphas': alphas}

# ── Pillar 2: Behavioral Quality ─────────────────────────────

def compute_c2_behavior(answers: dict, response_times_ms: dict) -> dict:
    """
    Three indicators combined:
      RT score      (0.40 weight) — response time quality
      Str score     (0.35 weight) — straight-lining / long-run detection
      IRV score     (0.25 weight) — intra-individual response variability

    C2 = 0.40×rt + 0.35×str + 0.25×irv
    """
    ordered_ids     = list(answers.keys())
    ordered_options = [answers[qid] for qid in ordered_ids]
    n               = len(ordered_ids)

    # ── RT Score ────────────────────────────────────────────
    rt_flags  = 0.0
    rt_detail = {}

    if response_times_ms:
        for qid in ordered_ids:
            t_ms = response_times_ms.get(qid)
            if t_ms is None or t_ms <= 0:
                continue
            t = t_ms / 1000.0   # convert to seconds

            if t < 1.5:
                rt_flags += 1.0
                rt_detail[qid] = 'too_fast'
            elif t < 3.0:
                rt_flags += 0.3
                rt_detail[qid] = 'fast'
            elif t > 90.0:
                rt_flags += 0.5
                rt_detail[qid] = 'distracted'
            else:
                rt_detail[qid] = 'normal'

    rt_score = _clamp(1.0 - (rt_flags / n)) if n > 0 else 0.5

    # ── Straight-lining Score ────────────────────────────────
    # ≥4 consecutive same = suspect, ≥7 = strong IER signal
    max_run   = _longest_run(ordered_options)
    str_score = _clamp(1.0 - (max_run / 7.0))

    # ── IRV Score ────────────────────────────────────────────
    # Map A=1 B=2 C=3 D=4, compute stdev
    option_nums = [OPTION_KEYS.index(o) + 1 for o in ordered_options if o in OPTION_KEYS]
    if len(option_nums) >= 2:
        irv       = stdev(option_nums)
        irv_score = _clamp(irv / 1.5)   # max meaningful stdev on 4-option scale ≈ 1.5
    else:
        irv, irv_score = 0.0, 0.5

    c2 = (0.40 * rt_score) + (0.35 * str_score) + (0.25 * irv_score)

    return {
        'score':     round(_clamp(c2), 3),
        'rt_score':  round(rt_score, 3),
        'str_score': round(str_score, 3),
        'irv_score': round(irv_score, 3),
        'max_run':   max_run,
        'irv':       round(irv, 3),
        'rt_flags':  round(rt_flags, 2),
        'rt_detail': rt_detail,
    }

# ── Pillar 3: Statistical Stability (Stubbed) ────────────────

def compute_c3_stability(_answers: dict) -> dict:
    """
    Stubbed at neutral 0.65 until calibration data is available.
    Phase 3 implementation: z-score extremity penalty + within-trait variance.
    """
    return {
        'score': 0.65,
        'note':  'Pending calibration sample (Phase 3)',
    }

# ── Master Confidence Builder ────────────────────────────────

def compute_confidence(answers: dict, response_times_ms: dict = None) -> dict:
    """
    Full 3-pillar confidence.
    Returns per-trait + overall confidence with full diagnostic breakdown.
    """
    rts = response_times_ms or {}

    c1 = compute_c1_consistency(answers)
    c2 = compute_c2_behavior(answers, rts)
    c3 = compute_c3_stability(answers)

    c1_scores  = c1['scores']
    c2_global  = c2['score']
    c3_global  = c3['score']

    per_trait = {}
    for trait in TRAITS:
        c1_t = c1_scores.get(trait, 0.5)
        per_trait[trait] = round(_clamp(W1 * c1_t + W2 * c2_global + W3 * c3_global), 3)

    overall = round(mean(per_trait.values()), 3)

    return {
        'overall':             overall,
        'per_trait':           per_trait,
        'needs_clarification': overall < 0.75,
        'pillar_1': {
            'label':  'Internal Consistency (Cronbach α)',
            'scores': c1_scores,
            'alphas': c1['alphas'],
        },
        'pillar_2': {
            'label':     'Behavioral Quality',
            'score':     c2_global,
            'rt_score':  c2['rt_score'],
            'str_score': c2['str_score'],
            'irv_score': c2['irv_score'],
            'max_run':   c2['max_run'],
            'irv':       c2['irv'],
            'rt_flags':  c2['rt_flags'],
        },
        'pillar_3': {
            'label': 'Statistical Stability',
            'score': c3_global,
            'note':  c3['note'],
        },
    }

# ── Full Profile Builder ──────────────────────────────────────

def build_profile(
    user_type: str,
    inst_id: str,
    answers: dict,
    response_times_ms: dict = None,
) -> dict:
    """
    answers:           {question_id: 'A'|'B'|'C'|'D'}
    response_times_ms: {question_id: milliseconds}
    """
    ocean      = compute_ocean_scores(answers)
    confidence = compute_confidence(answers, response_times_ms or {})
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