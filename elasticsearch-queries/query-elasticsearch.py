from elasticsearch import Elasticsearch


#

def search(es, term):
    res = es.search(
        index="my_data",
        doc_type="tag",
        body={
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "Title": {
                                    "query": term,
                                    "boost": 2
                                }
                            }
                        },
                        {
                            "match": {
                                "Body": {
                                    "query": term,
                                    "boost": 1
                                }
                            }
                        }
                    ]
                }
            },
            "_source": [
                "Id"
            ],
            "highlight": {
                "fields": {
                    "content": {}
                }
            }
        })

    return res


es = Elasticsearch()
res = search(es, "importing csv into dict")
print(res)

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(Id)s" % hit["_source"])
