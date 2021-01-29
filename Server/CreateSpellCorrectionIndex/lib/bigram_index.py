import os

__alpha__ = ['آ', 'ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ',
             'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س',
             'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف',
             'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی', '‌']


# find unique tokens and return them as a list
def token_set(words):
    result = set()
    for word in words:
        result.add(word)
    return list(result)


# creates index of bigrams in the index directory, wont do anything if its created already
def subfolder_creation():
    for i in __alpha__:
        cp = '../index/' + i
        if not os.path.exists(path=cp):
            os.mkdir(path=cp)
            for j in __alpha__:
                open(cp + '/' + j + '.txt', 'x', encoding='utf-8')


# gets a word and return its bigrams
def bigram_separation(token):
    bigrams = list()
    for i in range(len(token)):
        bi = token[i:i + 2]
        if len(bi) == 2:
            bigrams.append(token[i:i + 2])
    return bigrams


def bigram_add(bigram, word):
    path = '../index/' + bigram[0] + '/' + bigram[1] + '.txt'
    f = open(path, 'a', encoding='utf-8')
    f.write(word)
    f.close()
