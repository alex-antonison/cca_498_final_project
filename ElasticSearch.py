# 1. Which libraries do I need ?
import csv
from elasticsearch import Elasticsearch

data_path = 'Questions_New.csv'
request_body = {
    'settings': {
      'number_of_shards': 5,
      'number_of_relicas': 0
    },
    'mappings': {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_custom_analyzer": {
              "tokenizer": "standard",
              "char_filter": [
                "html_strip"
              ]
            }
          }
        }
      },
      "mappings": {
        "tag": {
          "properties": {
            "Body": {
              "type": "string",
              "analyzer": "my_custom_analyzer"
            },
            "CreationDate": {
              "type": "date"
            },
            "Id": {
              "type": "long"
            },
            "OwnerUserId": {
              "type": "long"
            },
            "ParentId": {
              "type": "long"
            },
            "Score": {
              "type": "long"
            }
          }
        }
      }
    }
}

#CHUNKSIZE = 10

def index_data(data_path, chunksize, index_name, doc_type):
    es = Elasticsearch()
    try :
        es.indices.delete(index_name)
    except :
        pass
    es.indices.create(index=index_name, body=request_body, ignore=400)
    with open(data_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                es.index(index = index_name,  doc_type = doc_type, body = row, ignore = 400)
                        # es.index(, , list_records,con)
            except Exception as ex :
                print("error!, skiping chunk! {}".format(ex))
                pass


index_data(data_path, CHUNKSIZE, 'my_data', 'tag') # Indexing train data