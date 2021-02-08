import pickle

import CreateSpellCorrectionIndex.lib.Candidate_generation as cnd

with open("./CreateSpellCorrectionIndex/sources/Wordfrec-wiki.pkl", "rb") as table:
    freq = pickle.load(table)

def evaluate(query):
    suggestions = list()
    query = str(query)
    candidates = cnd.candidate_generation(query)

    for candidate in candidates:

        if freq.get(candidate):
            suggestions.append(candidate)
    suggestions.sort(key=freq.get, reverse=True)
    return suggestions
