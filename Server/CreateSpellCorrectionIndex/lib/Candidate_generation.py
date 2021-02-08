import CreateSpellCorrectionIndex.lib.NnT

alpha = CreateSpellCorrectionIndex.lib.NnT.white_list


def _extra_letter(word):
    word = str(word)
    candidates = list()
    for i in range(len(word) - 1):
        candidates.append(word[:i] + word[i + 1:])
    candidates.append(word[0:len(word) - 1])
    return candidates


def _swapped_letter(word):
    word = str(word)
    candidates = set()
    for i in range(len(word) - 1):
        candidates.add(word[:i] + word[i + 1] + word[i] + word[i + 2:])
    return candidates


def _missed_letter(word):
    word = str(word)
    candidates = list()
    for i in range(len(word)):
        for letter in alpha:
            candidates.append(word[:i] + letter + word[i:])
    return candidates


def _changed_letter(word):
    word = str(word)
    candidates = list()
    for i in range(len(word)):
        for letter in alpha:
            candidates.append(word[:i] + letter + word[i + 1:])
    return candidates


def candidate_generation(word):
    result = list()
    result.extend(_extra_letter(word))
    result.extend(_swapped_letter(word))
    result.extend(_missed_letter(word))
    result.extend(_changed_letter(word))
    return result
