import elastic
import nlp

def lookup(description, synonyms=None):
    '''
    Look up words by their definitions
    using the indexed terms and their synonyms.
    '''
    description = nlp.correct(description)
    query = {'bool':{'must':get_definition_query(description),
                     'should':get_synonym_query(description, synonyms),
                     'minimum_should_match':0,
                     'boost':1.5}}
    return search(query)

def search(query):
    print 'searching', query
    results = elastic.client.search(index=elastic.SEARCH_INDEX, body={'query':query})
    return list(parse_results(results))

def get_definition_query(description, synonyms=None):
    query = {'match':{'definitions':{'query':unicode(description),
                                     'cutoff_frequency':0.001}}}
    return query

def get_synonym_query(description, synonyms=None):
    tokens = nlp.tokenize(description) + (synonyms or [])
    return {'match':{'synonyms':{'query':tokens, 'operator':'or'}}}

def parse_results(results):
    print 'found', results['hits'].get('total')
    return (h['_source']['doc'] for h in results['hits'].get('hits',[]))
