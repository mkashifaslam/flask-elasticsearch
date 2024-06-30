import json
from pprint import pprint
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_SEARCH_USER = os.getenv('ELASTIC_SEARCH_USER')
ELASTIC_SEARCH_PASS = os.getenv('ELASTIC_SEARCH_PASS')


class Search:
    def __init__(self):
        self.es = Elasticsearch('http://localhost:9200', http_auth=(ELASTIC_SEARCH_USER, ELASTIC_SEARCH_PASS))
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)

    def create_index(self):
        self.es.indices.delete(index='my_documents', ignore_unavailable=True)
        self.es.indices.create(index='my_documents')

    def reindex(self):
        self.create_index()
        with open('data.json', 'rt') as f:
            documents = json.loads(f.read())
        return self.insert_documents(documents)

    def insert_document(self, document):
        return self.es.index(index='my_documents', body=document)

    def insert_documents(self, documents):
        operations = []
        for document in documents:
            operations.append({'index': {'_index': 'my_documents'}})
            operations.append(document)
        return self.es.bulk(operations=operations)

    def search(self, **query_args):
        return self.es.search(index='my_documents', **query_args)

    def retrieve_document(self, id):
        return self.es.get(index='my_documents', id=id)
