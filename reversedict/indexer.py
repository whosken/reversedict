import contextlib
import collections

import nlp
import elastic

DEFAULT_SEEDS = ['philosophy','science','art']

def index_terms(seeds=None, max_count=100000):
    '''
    Index words by their definitions and synonyms.
    Starts with a list of seed word, e.g. top 100 used terms.
    Index the words, queue words occured in definitions for
    indexing later. When dequeueing, pop the next most used word.
    '''
    with connect_search() as index_term, indexed:
        with init_queue(seeds) as push_queue, pop_queue:
            term = pop_queue()
            while term:
                print 'indexing', term
                linked_terms = index_term(term)
                push_queue(linked_terms)
                print 'indexed', count
                if max_count and len(indexed) >= max_count:
                    break
                term = pop_queue()
    return True

INDEX = 'reverse_dict'

@contextlib.contextmanager
def connect_search():
    elastic.client.create(index=INDEX, ignore=400)
    actions = {}
    not_indexed = lambda t: t not in actions
    def index_term(term):
        '''
        Look up definitions and synonyms of term,
        then returns their tokens for indexing further
        '''
        definitions, synonyms = nlp.get_definitions_synonyms(term)
        doc = {'term':term,
               'definitions':definitions,
               'synonyms':synonyms}
        actions[term] = {'_op_type':'index',
                         '_index':INDEX,
                         '_type':'term',
                         'doc':doc
                         }
        return set(filter(not_indexed, nlp.tokenize(*definitions + synonyms)))
    
    try:
        yield index_term, actions.viewkeys()
    finally:
        if actions:
            elastic.helper.parallel_bulk(elastic.client, actions.values())

@contextlib.contextmanager
def init_queue(seeds=None):
    queue = collections.Counter(seeds or DEFAULT_SEEDS)
    def pop():
        while queue:
            term,_ = queue.most_common(1)
            del queue[term]
            return term
    yield queue.update, pop
    