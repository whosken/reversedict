import elasticsearch
import elasticsearch.helper as helper
import os

HOST = os.environ.get('SEARCHBOX_URL')

class LazyClient(object):
    def __init__(self):
        self._client = False
        
    def __getattr__(self,name):
        if name == '_client':
            return self._client
        if not self._client:
            self._client = elasticsearch.Elasticsearch(HOST)
        return getattr(self._client, name)
    
client = LazyClient()
