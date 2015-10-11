

import nltk
try:
    for package in ['brown','conll2000','punkt','wordnet']:
        nltk.download(package)
except:
    pass

from nltk.corpus import wordnet

import textblob

import stopwords

stopword_list = stopwords.load()

POS_MAP = {'N':wordnet.NOUN,
           'V':wordnet.VERB,
           'J':wordnet.ADJ,
           'R':wordnet.ADV}
def wordnet_pos(pos):
    return POS_MAP.get(pos[0])

def get_pos_synsets(text):
    blob = textblob.TextBlob(text)
    poss = dict((w,t) for w,t in blob.tags)
    for word in blob.words:
        if stopword_list and word in stopword_list:
            continue
        if word not in poss:
            continue
        yield word, poss[word], word.get_synsets(wordnet_pos(poss[word]))