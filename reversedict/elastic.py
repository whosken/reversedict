import elasticsearch
import elasticsearch.helpers as helpers
import os

HOST = os.environ.get('SEARCHBOX_URL') or 'localhost:9200'
SEARCH_INDEX = 'reverse_dict'

class LazyClient(object):
    def __init__(self):
        self._client = False
        
    def __getattr__(self,name):
        if name == '_client':
            return self._client
        if not self._client:
            print 'connecting to', HOST
            self._client = elasticsearch.Elasticsearch([HOST])
        return getattr(self._client, name)
    
client = LazyClient()
