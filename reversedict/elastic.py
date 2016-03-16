import elasticsearch
import elasticsearch.helpers as helpers

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
                self._client = elasticsearch.Elasticsearch([HOST], port=80, timeout=10)
            else:
                self._client = elasticsearch.Elasticsearch(['localhost:9200'])
        return getattr(self._client, name)
    
client = LazyClient()

def _delete(index=None):
    return client.indices.delete(index=index or SEARCH_INDEX)