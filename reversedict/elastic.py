import elasticsearch
import elasticsearch.helpers as helpers
import elasticsearch.exceptions as exceptions

import os

HOST = os.environ.get('SEARCHBOX_URL')
SEARCH_INDEX = 'reverse_dict'

class LazyClient(object):
    def __init__(self):
        self._client = False
        
    def __getattr__(self,name):
        if name == '_client':
            return self._client
        if not self._client:
            print 'connecting to', HOST
            if HOST:
                self._client = elasticsearch.Elasticsearch([HOST], port=80, timeout=30)
            else:
                self._client = elasticsearch.Elasticsearch(['localhost:9200'])
        return getattr(self._client, name)
    
client = LazyClient()

def delete_index(index=None):
    return client.indices.delete(index=index or SEARCH_INDEX)

def create_index(index=None):
    return client.indices.create(index=index or SEARCH_INDEX, ignore=400)

def refresh_index(index=None):
    return client.indices.refresh(index=index or SEARCH_INDEX)
