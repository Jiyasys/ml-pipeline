from statistics import stdev

def compute_confidence(encoded_answers: dict, questions_used: list) -> dict:
    trait_responses = {"O":[],"C":[],"E":[],"A":[],"N":[]}
    for q in questions_used:
        if q["id"] in encoded_answers:
            trait_responses[q["trait"]].append(encoded_answers[q["id"]])
    confidence = {}
    for trait, responses in trait_responses.items():
        if len(responses) < 2:
            confidence[trait] = 0.5
            continue
        confidence[trait] = round(max(0.0, 1.0 - (stdev(responses) / 2.0)), 3)
    confidence["overall"] = round(sum(v for k,v in confidence.items() if k != "overall") / 5, 3)
    return confidence