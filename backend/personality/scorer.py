# ============================================================
# EDWISERR — OCEAN Scorer + Confidence Engine
# Pillar 1 : Internal Consistency  (Cronbach's Alpha)
# Pillar 2 : Behavioral Quality    (RT + Straight-lining + IRV)
# Pillar 3 : Statistical Stability (stubbed at 0.75 — needs calibration)
#
# Master formula:
#   Confidence(trait) = 0.40×C1 + 0.35×C2 + 0.25×C3
#   Confidence(overall) = mean across all 5 traits
# ============================================================

import math
from statistics import mean, stdev
from personality.questions import QUESTIONS, INVERTED_TRAITS

Q_LOOKUP    = {q['id']: q for q in QUESTIONS}
OPTION_KEYS = ['A', 'B', 'C', 'D']
TRAITS      = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']

W1, W2, W3 = 0.40, 0.35, 0.25

# ── Helpers ──────────────────────────────────────────────────

def _clamp(val, lo=0.0, hi=1.0):
    return max(lo, min(hi, val))

def _get_weight(qid: str, option: str) -> float:
    return float(Q_LOOKUP[qid][f'weight_{option}'])

def _longest_run(seq) -> int:
    if not seq:
        return 0
    mx = cur = 1
    for i in range(1, len(seq)):
        cur = cur + 1 if seq[i] == seq[i - 1] else 1
        mx  = max(mx, cur)
    return mx

def _trait_weights(answers: dict) -> dict:
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
    Estimates alpha via inter-item correlation proxy:
        r̄ estimated from within-trait weight spread
        α = (k × r̄) / (1 + (k-1) × r̄)
    Low spread = high consistency = high alpha.
    """
    k = len(weights)
    if k < 2:
        return 0.65
    if len(set(weights)) == 1:
        return 1.0

    sd    = stdev(weights)
    # Max meaningful std on 0.1–0.9 weight scale ≈ 0.4
    r_bar = _clamp(1.0 - (sd / 0.4))
    denom = 1 + (k - 1) * r_bar
    alpha = (k * r_bar) / denom if denom > 0 else 0.0
    return _clamp(float(alpha))

def compute_c1_consistency(answers: dict) -> dict:
    """
    Per-trait alpha → C1 score (0–1):
        C1 = clamp((α − 0.50) / 0.40)
    α=0.50 → C1=0.0 | α=0.70 → C1=0.5 | α=0.90 → C1=1.0
    """
    tw = _trait_weights(answers)
    c1_scores, alphas = {}, {}
    for trait, weights in tw.items():
        alpha            = _cronbach_alpha(weights)
        alphas[trait]    = round(alpha, 3)
        c1_scores[trait] = round(_clamp((alpha - 0.50) / 0.40), 3)
    return {'scores': c1_scores, 'alphas': alphas}

# ── Pillar 2: Behavioral Quality ─────────────────────────────

def compute_c2_behavior(answers: dict, response_times_ms: dict) -> dict:
    """
    Three indicators:

    RT score (0.40)
        Flags responses that are too fast (<1.5s) or distracted (>90s).
        Normal range 3–30s gets no penalty.

    Straight-lining score (0.35)
        Detects long runs of the same option.
        Threshold scales with n_questions:
            suspicious  ≥ max(4, n×0.30)
            strong IER  ≥ max(7, n×0.50)
        FIX: Raised thresholds vs original — 25Q format needs higher tolerance.

    IRV score (0.25)
        FIX: IRV now rewards moderate variance, not high variance.
        A consistent responder (clear personality) has low-moderate IRV — good.
        Near-zero IRV is only penalised when straight-lining is also detected.
        Very high IRV (purely random) is also penalised.
        Optimal range: 0.8–1.3 stdev on the 4-option scale.
    """
    ordered_ids  = list(answers.keys())
    ordered_opts = [answers[qid] for qid in ordered_ids]
    n            = len(ordered_ids)

    # ── RT Score ────────────────────────────────────────────
    flags = 0.0
    rt_detail = {}
    for qid in ordered_ids:
        t_ms = response_times_ms.get(qid)
        if t_ms is None or t_ms <= 0:
            rt_detail[qid] = 'no_data'
            continue
        t = t_ms / 1000.0
        if t < 1.5:
            flags += 1.0
            rt_detail[qid] = 'too_fast'
        elif t < 3.0:
            flags += 0.3
            rt_detail[qid] = 'fast'
        elif t > 90.0:
            flags += 0.5
            rt_detail[qid] = 'distracted'
        else:
            rt_detail[qid] = 'normal'

    rt_score = _clamp(1.0 - (flags / n)) if n > 0 else 0.75

    # ── Straight-lining Score ────────────────────────────────
    # Scale thresholds with question count to avoid over-penalising
    # short consistent assessments
    max_run           = _longest_run(ordered_opts)
    suspicious_thresh = max(4, int(n * 0.30))   # e.g. 25Q → 7
    strong_ier_thresh = max(7, int(n * 0.50))   # e.g. 25Q → 12

    if max_run >= strong_ier_thresh:
        str_score = _clamp(1.0 - (max_run / strong_ier_thresh))
    elif max_run >= suspicious_thresh:
        # Partial penalty between thresholds
        ratio     = (max_run - suspicious_thresh) / (strong_ier_thresh - suspicious_thresh)
        str_score = _clamp(1.0 - 0.5 * ratio)
    else:
        str_score = 1.0   # no straight-lining detected

    # ── IRV Score ────────────────────────────────────────────
    # Map A=1 B=2 C=3 D=4 and compute stdev across all responses
    option_nums = [OPTION_KEYS.index(o) + 1 for o in ordered_opts if o in OPTION_KEYS]

    if len(option_nums) < 2:
        irv       = 0.0
        irv_score = 0.75
    else:
        irv = stdev(option_nums)

        # FIX: Reward moderate variability. Penalise extremes.
        # Optimal stdev ≈ 0.8–1.3 (using 2 or 3 of the 4 options consistently)
        # Near-zero: suspicious only if combined with straight-lining
        # Very high (>1.5): may indicate random clicking

        if irv < 0.3:
            # Near-zero variance — straight-lining caught above; give small penalty
            # but only if straight-lining is also suspicious
            irv_score = 0.6 if max_run >= suspicious_thresh else 0.8
        elif irv <= 1.4:
            # Healthy moderate range → full score
            irv_score = 1.0
        else:
            # High variance — possible random clicking
            irv_score = _clamp(1.0 - (irv - 1.4) / 0.8)

    # ── Composite C2 ────────────────────────────────────────
    c2 = 0.40 * rt_score + 0.35 * str_score + 0.25 * irv_score

    return {
        'score':     round(_clamp(c2), 3),
        'rt_score':  round(rt_score, 3),
        'str_score': round(str_score, 3),
        'irv_score': round(irv_score, 3),
        'max_run':   max_run,
        'irv':       round(irv, 3),
        'rt_flags':  round(flags, 2),
        'rt_detail': rt_detail,
    }

# ── Pillar 3: Statistical Stability (Stubbed) ────────────────

def compute_c3_stability(_answers: dict) -> dict:
    """
    Stubbed at 0.75 (neutral-good) until calibration sample is available.
    FIX: Changed from 0.65 → 0.75 to avoid artificially depressing
    overall confidence while P3 is not yet implemented.
    Phase 3 will implement z-score extremity penalty and variance analysis.
    """
    return {
        'score': 0.75,
        'note':  'Pending calibration sample (Phase 3) — currently neutral',
    }

# ── Master Confidence Builder ────────────────────────────────

def compute_confidence(answers: dict, response_times_ms: dict = None) -> dict:
    rts = response_times_ms or {}

    c1 = compute_c1_consistency(answers)
    c2 = compute_c2_behavior(answers, rts)
    c3 = compute_c3_stability(answers)

    c1_scores = c1['scores']
    c2_global = c2['score']
    c3_global = c3['score']

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