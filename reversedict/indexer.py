import contextlib
import collections
import time

import nlp
import elastic

DEFAULT_SEEDS = ['philosophy','science','art','health','emotion']

def index_terms(seeds=None, max_count=5000):
    '''
    Index words by their definitions and synonyms.
    Starts with a list of seed word, e.g. top 100 used terms.
    Index the words, queue words occured in definitions for
    indexing later. When dequeueing, pop the next most used word.
    '''
    with connect_search() as (index_term, indexed):
        with init_queue(indexed, seeds) as (push_queue, pop_queue):
            term = pop_queue()
            while term:
                print 'indexing', term
                linked_terms = index_term(term)
                push_queue(linked_terms)
                if max_count and max_count <= len(indexed):
                    break
                term = pop_queue()
        print 'indexed', len(indexed), 'terms'
    return True

@contextlib.contextmanager
def connect_search():
    #elastic.delete_index()
    elastic.create_index()
    actions = {}
    def index_term(term):
        '''
        Look up definitions and synonyms of term,
        then returns their tokens for indexing further
        '''
        definitions, synonyms = nlp.get_definitions_synonyms(term)
        if not definitions:
            return []
        doc = {'term':term,
               'definitions':definitions,
               'synonyms':synonyms}
        actions[term] = {'_op_type':'index',
                         '_id':hash(term),
                         '_index':elastic.SEARCH_INDEX,
                         '_type':'term',
                         'doc':doc
                         }
        actions_count = len(actions)
        if actions_count > 1000 and actions_count % 1000 == 0:
            retry_commit()
        return nlp.tokenize(*definitions + synonyms)
    
    def commit_index_actions():
        actionables = filter(None, actions.values())
        if not actionables:
            return False
        successes, errors = elastic.helpers.bulk(elastic.client, actionables)
        if errors:
            print errors
        print 'committed', successes, 'terms'; print
        for term in actions:
            actions[term] = None
        return True
    
    def retry_commit():
        for timeout in (0,10,20,30):
            try:
                return commit_index_actions()
            except elastic.exceptions.ConnectionTimeout as error:
                print 'errored', error, 'sleeping for', timeout
                time.sleep(timeout)
    
    try:
        yield index_term, actions.viewkeys()
    finally:
        if actions:
            retry_commit()
            elastic.refresh_index()

@contextlib.contextmanager
def init_queue(indexed, seeds=None):
    seeds = seeds or DEFAULT_SEEDS
    queue = collections.Counter()
    is_not_indexed = lambda t: t not in indexed
    def yield_terms():
        while seeds:
            yield seeds.pop(0)
        while queue:
            term,_ = queue.most_common(1)[0]
            del queue[term]
            yield term
    def pop():
        for term in yield_terms():
            if is_not_indexed(term):
                return term
    def push(tokens):
        queue.update(filter(is_not_indexed, tokens))
    yield push, pop
    