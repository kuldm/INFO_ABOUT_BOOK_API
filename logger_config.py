from loguru import logger
from elasticsearch import Elasticsearch
from elasticsearch.helpers import BulkIndexError
from config import settings

# Существующая конфигурация логгера

# Добавляем обработчик для Elasticsearch
es_client = Elasticsearch([settings.ELASTICSEARCH_HOST])


class ElasticsearchHandler:
    def __init__(self, es_client, index):
        self.es_client = es_client
        self.index = index

    def write(self, message):
        try:
            self.es_client.index(index=self.index, body=message)
        except BulkIndexError as e:
            print(f"Ошибка при индексации лога в Elasticsearch: {e}")


es_handler = ElasticsearchHandler(es_client, "application_logs")
logger.add(es_handler.write, format="{time} {level} {message}", level="INFO")
# http://localhost:5601 - Kibana
