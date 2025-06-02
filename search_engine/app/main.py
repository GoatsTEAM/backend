from elasticsearch import Elasticsearch
import json
# TODO: change Host
ES_HOST = "http://localhost:9200"  
INDEX_NAME = "products_index"

def create_index():
    es = Elasticsearch(ES_HOST)

    if es.indices.exists(index=INDEX_NAME):
        print(f"Index {INDEX_NAME} exists. Deleting it...")
        es.indices.delete(index=INDEX_NAME)

    with open("es_mapping.json", "r", encoding="utf-8") as f:
        mapping = json.load(f)

    es.indices.create(index=INDEX_NAME, body=mapping)
    print(f"Index {INDEX_NAME} created with mapping.")

if __name__ == "__main__":
    create_index()