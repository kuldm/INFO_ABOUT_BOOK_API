from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from config import settings

es_client = Elasticsearch([settings.ELASTICSEARCH_HOST])


def index_document(index, doc_type, doc_id, body):
    return es_client.index(index=index, doc_type=doc_type, id=doc_id, body=body)


def search(index, query):
    s = Search(using=es_client, index=index).query("multi_match", query=query, fields=['*'])
    response = s.execute()
    return response


def delete_document(index, doc_type, doc_id):
    return es_client.delete(index=index, doc_type=doc_type, id=doc_id)
