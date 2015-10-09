import textblob
from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic

import collections
import math

def reverse_lookup(description):
    '''
    Parses the description into part-of-speech and removes stop words
    Select a set of primary (i.e. the entity to which the description defines) from part-of-speech
    Looks up WordNet for hyponyms (i.e. more specific forms) of the primaries
    Score each hyponym by how similar its definition is to the rest of the description
    '''
    
    words,poss,synsets = zip(*get_pos_synsets(description))
    poss_dict = dict(zip(words, poss))
    synset_dict = dict(zip(words, synsets))
    primaries = set(select_primaries(poss_dict))
    adjustments = select_adjustments(synset_dict, primaries)

    candidates = collections.Counter()
    for primary in primaries:
        print '=====>', primary
        for synset in synset_dict[primary]:
            print '===>', synset, synset.definition()
            for candidate in synset.hyponyms():
                word = candidate.lemma_names()[0].replace('_',' ')
                if word not in primaries:
                    candidates[word] += score_candidate(candidate, adjustments)
    candidates += collections.Counter()
    print 'selecting top candidates from', len(candidates), 'found'
    return candidates.most_common(20).keys()

POS_MAP = {'N':wordnet.NOUN,
           'V':wordnet.VERB,
           'J':wordnet.ADJ,
           'R':wordnet.ADV}
def wordnet_pos(pos):
    return POS_MAP.get(pos[0])

def select_primaries(poss_dict):
    poss_rev = collections.defaultdict(list)
    for word,pos in poss_dict.items():
        poss_rev[pos].append(word)
    return poss_rev.get('NN') or poss_rev.get('VB') or poss_rev.get('VBG') or poss_rev.get('JJ') or poss_rev.get('RB') or poss_dict.keys()

def select_adjustments(synset_dict, primaries):
    return [(w,s) for w,s in synset_dict.items() if w not in primaries] or synset_dict.items()

def get_pos_synsets(text):
    blob = textblob.TextBlob(text)
    poss = dict((w,t) for w,t in blob.tags)
    for word in blob.words:
        if stopwords and word in stopwords:
            continue
        if word not in poss:
            continue
        yield word, poss[word], word.get_synsets(wordnet_pos(poss[word]))
        
def score_candidate(candidate, adjustments): # improve this
    definition = candidate.definition()
    print '=>', candidate, definition
    similarity_score = 0
    for word,_,word_synsets in get_pos_synsets(definition):
        for word_synset in word_synsets:
            for adj_word, adj_synsets in adjustments:
                for adj_synset in adj_synsets:
                    similarity_score += wordnet.wup_similarity(word_synset, adj_synset, simulate_root=False) or 0
    return math.log1p(similarity_score)

def load_stopwords():
    stop_words = textblob.blob.WordList([])
    for line in open('./stopwords.txt'):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    return stop_words

stopwords = load_stopwords()