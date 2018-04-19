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
                                    "boost": 10
                                }
                            }
                        },
                        {
                            "match": {
                                "BodyClean": {
                                    "query": term,
                                    "boost": 1
                                }
                            }
                        }
                    ]
                }
            },
            "_source": [
                "Id",
                "Title",
                "Body"
            ],
            "highlight": {
                "fields": {
                    "*": {}
                }
            }
        })

    return res


es = Elasticsearch()
res = search(es, "Mixing Matplotlib")
print(res)

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    # print("%(Id)s | %(Title)s | %(Body)s" % hit["_source"])
    print("%(Id)s" % hit["_source"], "%(Title)s | %(BodyClean)s" % hit["highlight"])
