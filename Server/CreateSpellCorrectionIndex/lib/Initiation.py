import bigram_index as bi
import NnT as n


def initiation():
    inp = open('../sources/input.txt', 'r', encoding='utf-8')
    words = inp.read()
    words = n.letter_filter(words)
    words = n.word_separator(words)
    words = bi.token_set(words)
    bi.subfolder_creation()

    for word in words:
        bigrams = bi.bigram_separation(word)
        for bigram in bigrams:
            bi.bigram_add(bigram, word + ' ')

initiation()