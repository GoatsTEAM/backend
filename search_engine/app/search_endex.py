from elasticsearch import Elasticsearch

ES_HOST = "http://localhost:9200"
INDEX_NAME = "products_index"

class ProductSearchEngine:
    def __init__(self, es_host=ES_HOST, index=INDEX_NAME):
        self.es = Elasticsearch(es_host)
        self.index = index

    def search(
        self,
        query_text=None,
        min_price=None,
        max_price=None,
        category_id=None,
        seller_company=None,
        page=0,
        size=10
    ):
        """
        Возвращает результаты поиска в виде списка dict: [{source}, ...].
        Параметры:
          - query_text: строка, поиск по title и description
          - min_price, max_price: фильтр по цене
          - category_id: точный match по category.category_id
          - seller_company: текстовый поиск по seller.company_name
          - page: номер страницы (0-based)
          - size: количество на странице
        """
        must_clauses = []
        filter_clauses = []

        if query_text:
            must_clauses.append({
                "multi_match": {
                    "query": query_text,
                    "fields": ["title^2", "description"],  
                    "fuzziness": "AUTO"  # допустимая нестрогая коррекция
                }
            })

        if min_price is not None or max_price is not None:
            price_range = {}
            if min_price is not None:
                price_range["gte"] = min_price
            if max_price is not None:
                price_range["lte"] = max_price
            filter_clauses.append({
                "range": {
                    "price": price_range
                }
            })

        if category_id is not None:
            filter_clauses.append({
                "term": {
                    "category.category_id": category_id
                }
            })

        if seller_company:
            must_clauses.append({
                "match": {
                    "seller.company_name": {
                        "query": seller_company,
                        "operator": "and"
                    }
                }
            })

        body = {
            "query": {
                "bool": {
                    "must": must_clauses,
                    "filter": filter_clauses
                }
            },
            "from": page * size,
            "size": size,
            "sort": [
                {"seller.rating": {"order": "desc", "missing": 0}},
                {"price": {"order": "asc"}}
            ]
        }

        res = self.es.search(index=self.index, body=body)
        hits = res["hits"]["hits"]

        # Возвращаем только _source и _id
        return [
            {"_id": hit["_id"], **hit["_source"]} for hit in hits
        ]


if __name__ == "__main__":
    engine = ProductSearchEngine()

    results = engine.search(
        query_text="синяя футболка",
        min_price=10,
        max_price=100,
        category_id=5,
        seller_company="Acme Inc.",
        page=0,
        size=5
    )
    for doc in results:
        print(f"ID = {doc['product_id']}, Title = {doc['title']}, Price = {doc['price']}, Seller = {doc['seller']['company_name']}")