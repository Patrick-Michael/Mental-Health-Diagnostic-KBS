from rapidfuzz import process, fuzz
from symptom_map import symptom_map

# Reverse index
variant_lookup = {}
for item in symptom_map:
    for variant in item["variants"]:
        variant_lookup[variant.lower()] = item

def match_symptom(user_input, threshold=80):
    best_match = process.extractOne(user_input.lower(), variant_lookup.keys(), scorer=fuzz.ratio)
    if best_match and best_match[1] >= threshold:
        return variant_lookup[best_match[0]]
    return None
