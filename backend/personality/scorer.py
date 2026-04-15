def compute_ocean_scores(encoded_answers: dict, questions_used: list) -> dict:
    trait_scores = {"O":[],"C":[],"E":[],"A":[],"N":[]}
    for q in questions_used:
        if q["id"] in encoded_answers:
            trait_scores[q["trait"]].append(encoded_answers[q["id"]])
    ocean = {}
    for trait, scores in trait_scores.items():
        if not scores:
            ocean[trait] = 50.0
            continue
        n = len(scores)
        ocean[trait] = round(((sum(scores) - n) / (n * 4)) * 100, 1)
    return ocean

def ocean_to_mbti(ocean: dict) -> str:
    return (
        ("E" if ocean["E"] >= 50 else "I") +
        ("N" if ocean["O"] >= 50 else "S") +
        ("F" if ocean["A"] >= 50 else "T") +
        ("J" if ocean["C"] >= 50 else "P")
    )