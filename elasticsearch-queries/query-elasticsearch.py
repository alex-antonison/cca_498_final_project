from elasticsearch import Elasticsearch


#

def search(es, term):
    res = es.search(
        index="my_data",
        doc_type="tag",
        body={
            "from" : 0, "size" : 100,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "Title": {
                                    "query": term,
                                    "boost": 5
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
                "Id",
                "Title",
                "Body"
            ],
            "highlight": {
                "fields": {
                    "Title": {},
                    "Body": {}
                }
            }
        })

    return res


es = Elasticsearch()
res = search(es, "Matplotlib")
print(res)

counter = 1

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    try:
        print(counter, " ", "%(Id)s" % hit["_source"], "%(Title)s | %(Body)s" % hit["highlight"])
    except:
        print(counter, " ", "%(Id)s | %(Title)s | %(Body)s" % hit["_source"],)

    counter = counter + 1

