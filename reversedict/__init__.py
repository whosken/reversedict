import elastic

def lookup(description, synonyms=None):
    '''
    Look up words by their definitions
    using the indexed terms and their synonyms.
    '''
    return (search(get_description_query(description, synonyms))
            or search(get_synonym_query(description, synonyms))
            )

def search(query):
    print 'searching', query
    try:
        results = elastic.client.search(index=elastic.SEARCH_INDEX, body=query)
    except Exception as error:
        print error.info
        raise
    return list(parse_results(results))

def get_description_query(description, synonyms=None):
    return {'match':{'descriptions':{'query':description,
                                     'cutoff_frequency':0.001},
                     'synonyms':{'query':synonyms,
                                 'operator':'or'}}}

def get_synonym_query(description, synonyms=None):
    import nlp
    tokens = nlp.tokenize(description) + (synonyms or [])
    return {'match':{'synonyms':{'query':tokens, 'operator':'or'}}}

def parse_results(results):
    return (h['_source'] for h in results['hits'].get('hits',[]))
