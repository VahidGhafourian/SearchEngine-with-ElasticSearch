import CreateSpellCorrectionIndex.lib.bigram_index as bi
import CreateSpellCorrectionIndex.lib.NnT as n
import pickle



def initiation():
    with open("./CreateSpellCorrectionIndex/sources/Wordfrec-wiki.pkl", "rb") as table:
        freq = pickle.load(table)
    freq = dict(freq)
    # inp = open('../sources/input.txt', 'r')
    # words = inp.read()


    words = list(freq.keys())
    words = n.letter_filter(words)
    words = n.word_separator(words)
    bi.subfolder_creation()
    words = bi.token_set(words)

    for word in words:
        bigrams = bi.bigram_separation(word)
        for bigram in bigrams:
            bi.bigram_add(bigram, word + ' ')


initiation()
