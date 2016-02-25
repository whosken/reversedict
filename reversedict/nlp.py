import nltk
try:
    for package in ['brown','conll2000','punkt','wordnet']:
        nltk.download(package)
except:
    pass

import textblob
import textblob.wordnet as wordnet

import stopwords

stopword_list = stopwords.load()
        
def is_stopword(term):
    return stopword_list and word in stopword_list

def lookup_word(term):
    return term if isinstance(term, textblob.Word) else textblob.Word(term)

def get_definitions_synonyms(term):
    word = nlp.lookup_word(term)
    definitions = word.define()
    synonyms = [l for s in word.get_synsets() for l in s.lemma_names()]
    return definitions, synonyms

def tokenize(*texts):
    blob = textblob.TextBlob(' '.join(texts))
    return (w for w in blob.words if not nlp.is_stopword(t))
