# 1. Which libraries do I need ?
import csv
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup

def remove_html_tags(text):
    try:
        soup = BeautifulSoup(text, 'html5lib')
        return soup.getText()
    except:
        print("bs4 issue")
        print(text)

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
            "TitleBody": {
              "type": "string",
              "analyzer": "my_custom_analyzer"
            },
            "Id": {
              "type": "long"
            }
          }
        }
      }
    }
}

CHUNKSIZE = 10

def index_data(data_path, chunksize, index_name, doc_type):
    es = Elasticsearch()
    try :
        es.indices.delete(index_name)
    except :
        pass
    es.indices.create(index=index_name, body=request_body, ignore=400)
    with open(data_path) as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            try:
                row['TitleBody'] = row['Title'] + remove_html_tags(row['Body'])
                black_list = {"OwnerUserId", "CreationDate", "Score", "Title", "Body"}
                rename = {}
                new_dict = {rename.get(key, key): val for key, val in row.items() if key not in black_list}
                # print(new_dict)
                es.index(index = index_name,  doc_type = doc_type, body = row, ignore = 400)
                    # es.index(, , list_records,con)
                count = count + 1
                print("Success: ", count)
            except Exception as ex :
                print("error!, skiping chunk! {}".format(ex))
                pass


index_data(data_path, CHUNKSIZE, 'my_data', 'tag') # Indexing train data