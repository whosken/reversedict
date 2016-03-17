import elastic

def lookup(description, synonyms=None):
    '''
    Look up words by their definitions
    using the indexed terms and their synonyms.
    '''
    return (search(get_definition_query(description, synonyms))
            or search(get_synonym_query(description, synonyms))
            )

def search(query):
    print 'searching', query
    try:
        results = elastic.client.search(index=elastic.SEARCH_INDEX, 
                                        body={'query':query})
    except Exception as error:
        print error.info
        raise
    return list(parse_results(results))

def get_definition_query(description, synonyms=None):
    query = {'match':{'definitions':{'query':description,
                                     'cutoff_frequency':0.001}}}
    if not synonyms:
        return query
    filters = {'terms':{'synonyms':synonyms}}
    return {'filtered':{'filter':filters, 'query':query}}

def get_synonym_query(description, synonyms=None):
    import nlp
    tokens = nlp.tokenize(description) + (synonyms or [])
    return {'match':{'synonyms':{'query':tokens, 'operator':'or'}}}

def parse_results(results):
    print 'found', results['hits'].get('total')
    return (h['_source']['doc'] for h in results['hits'].get('hits',[]))
