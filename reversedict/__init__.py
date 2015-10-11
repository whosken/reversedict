import collections
import math

import nlp

def lookup(description, pos=None, verbose=False):
    '''
    Parses the description into part-of-speech and removes stop words
    Select a set of primary (i.e. the entity to which the description defines) from part-of-speech
    Looks up WordNet for hyponyms (i.e. more specific forms) of the primaries
    Score each hyponym by how similar its definition is to the rest of the description
    '''
    
    words,poss,synsets = zip(*nlp.get_pos_synsets(description))
    synset_dict = dict(zip(words, synsets))
    primaries = set(select_primaries(zip(words, poss), pos) or words)
    adjustments = select_adjustments(synset_dict, primaries)

    candidates = collections.Counter()
    for primary in primaries:
        if verbose: 
            print '=====>', primary
        for synset in synset_dict[primary]:
            if verbose:
                print '===>', synset, synset.definition()
            for candidate in synset.hyponyms():
                word = candidate.lemma_names()[0].replace('_',' ')
                if word not in primaries:
                    if verbose: 
                        print '=>', candidate
                    candidates[word] += score_candidate(candidate, adjustments)
    candidates += collections.Counter() # remove 0 items
    if verbose:
        print 'selecting top candidates from', len(candidates), 'found'
    return [r for r,_ in candidates.most_common(20)]

def select_primaries(poss_pairs, primary_pos=None):
    primary_pos = (primary_pos or '').upper()
    poss_rev = collections.defaultdict(list)
    for word,pos in poss_pairs:
        poss_rev[pos].append(word)
    return poss_rev.get(primary_pos) or poss_rev.get('NN') or poss_rev.get('VB') or poss_rev.get('VBG') or poss_rev.get('JJ') or poss_rev.get('RB')

def select_adjustments(synset_dict, primaries):
    return [(w,s) for w,s in synset_dict.items() if w not in primaries] or synset_dict.items()
        
def score_candidate(candidate, adjustments): # improve this
    definition = candidate.definition()
    similarity_score = 0
    for word,_,word_synsets in nlp.get_pos_synsets(definition):
        for word_synset in word_synsets:
            for adj_word, adj_synsets in adjustments:
                for adj_synset in adj_synsets:
                    similarity_score += nlp.wordnet.wup_similarity(word_synset, adj_synset, simulate_root=False) or 0
    return math.log1p(similarity_score)