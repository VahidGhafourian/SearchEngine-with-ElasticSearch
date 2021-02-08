import CreateSpellCorrectionIndex.lib.SpellCorrection as sc
import CreateSpellCorrectionIndex.lib.evaluate
from difflib import SequenceMatcher
import pickle
import re

with open("./CreateSpellCorrectionIndex/sources/Wordfrec-wiki.pkl", "rb") as table:
    freq = pickle.load(table)


def get(string):
    tokens = string.split(" ")
    suggestions = list()

    for token in tokens:
        if freq.get(token):
            suggestions.append(token)
        else:
            if len(token) > 5:
                tmp = list(spell_check(token))
                for i in tmp:
                    str.strip(i)
                try:
                    tmp.sort(key=freq.get,reverse=True)
                except:
                    pass
                suggestions.append(tmp)
            else:
                suggestions.append(CreateSpellCorrectionIndex.lib.evaluate.evaluate(token))
    return combine(suggestions)


def spell_check(token):
    result = list()
    token = str(token)
    words = sc.word_counter(token)
    top10 = sc.find_top10(words, token)
    words = sc.find_similar(token, words)
    result.append(correction_check(words, top10, token))

    return combine(result)


def matrix(suggestions):
    result = list()
    for i in range(len(suggestions)):
        result.append([])
    j = 0
    for s in suggestions:
        if isinstance(s, str):
            for i in range(10):
                result[j].append(s)
        else:
            if len(s) > 10:
                for i in range(10):
                    result[j].append(s[i])
            else:
                for i in range(10):
                    try:
                        result[j].append(s[i])
                    except:
                        result[j].append(s[0])
        j += 1
    return result


def combine(suggestions):
    result = list()
    for i in range(10):
        result.append("")
    suggestions = matrix(suggestions)
    j = 0
    for f in range(10):
        for suggestion in suggestions:
            result[j] += suggestion[j] + " "
        j += 1
    return result


def rate(base_word, comparing_word):
    return int(SequenceMatcher(None, base_word, comparing_word).ratio() * 100)


def correction_check(words, top10, word):
    for i in  range(2):
        if sc.distance_measure(top10[i], word) > 2:
            return sc.find_similar(word, words)
    return top10

def make_it_ok(string):
    res = ""
    words = re.split("\s+", string)
    for word in words:
        res = res + word + " "
    return str.strip(res)  # space is last character

def Farsi_test(string):
    whitelist = ['ی', 'ه', 'و', 'ن', 'م', 'ل', 'گ', 'ک', 'ق', 'ف', 'غ', 'ع', 'ظ', 'ط', 'ض', 'ص', 'ش',
                 'س', 'ژ', 'ز', 'ر', 'ذ', 'د', 'خ', 'ح', 'چ', 'ج', 'ث', 'ت', 'پ', 'ب', 'ا', 'آ', '‌', ' ']
    for ch in string:
        if ch not in whitelist:
            return False
    return True