import CreateSpellCorrectionIndex.lib.SpellCorrection as sc
import re


def get(string):
    tokens = str(string).split(' ')
    return spell_check(tokens)


def make_it_ok(string):
    res = ""
    words = re.split("\s+", string)
    for word in words:
        res = res + word + " "
    return str.strip(res)  # space is last character


def empty_filter(li):
    result = []
    for it in li:
        if len(it) > 1:
            result.append(it)
    return result


def Farsi_test(string):
    whitelist = ['ی', 'ه', 'و', 'ن', 'م', 'ل', 'گ', 'ک', 'ق', 'ف', 'غ', 'ع', 'ظ', 'ط', 'ض', 'ص', 'ش',
                 'س', 'ژ', 'ز', 'ر', 'ذ', 'د', 'خ', 'ح', 'چ', 'ج', 'ث', 'ت', 'پ', 'ب', 'ا', 'آ', '‌', ' ']
    for ch in string:
        if ch not in whitelist:
            return False
    return True


def spell_check(tokens):
    result = list()
    for token in tokens:
        words = sc.word_counter(token)
        top10 = sc.find_top10(words, token)
        if top10[0] == token:
            result.append([token])
        elif correction_check(top10, token):
            result.append(top10)
        else:
            result.append(sc.find_similar(token, words)[:10])
    return combine(result)


def combine(listOfLists):
    result = list()
    for i in range(10):
        result.append('')

    for ls in listOfLists:
        for i in range(len(ls)):
            if len(ls) == 1:
                result[i] = result[i] + ' ' + ls[0]
            elif len(ls) < 10:
                result[i] = result[i] + ' ' + ls[0]
            else:
                result[i] = result[i] + ' ' + ls[i]

    return result


def correction_check(top10, word):
    for c in top10:
        if sc.distance_measure(c, word) < 3:
            return True
    return False
