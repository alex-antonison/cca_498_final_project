# 1. Which libraries do I need ?
import csv
import string
import re
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup

def remove_html_tags(text):
    try:
        soup = BeautifulSoup(text, 'html5lib')
        text = re.sub(r'[^\x00-\x7F]+',' ', soup.getText())
        return text
    except:
        print("bs4 issue")
        print(text)

data_path = '../Questions_New.csv'

request_body = {
    "settings": {
      "index": {
         "analysis": {
            "char_filter": {
               "my_html": {
                  "type": "html_strip"
               }
            },
            "analyzer": {
               "my_html": {
                  "tokenizer": "standard",
                  "char_filter": [
                     "my_html"
                  ],
                  "type": "custom"
               }
            }
         }
      }
   },
    "mappings": {
        "tag": {
          "properties": {
            "Id": {
              "type": "long"
            },
            "Title": {
              "type": "string",
              "analyzer": "my_html",
              "search_analyzer": "standard"
            },
            "Body": {
              "type": "string",
              "analyzer": "my_html",
              "search_analyzer": "standard"
            }
          }
        }
      }
    }

CHUNKSIZE = 10


def index_data(data_path, index_name, doc_type):
    es = Elasticsearch()
    try:
        es.indices.delete(index_name)
    except:
        pass
    es.indices.create(index=index_name, body=request_body, ignore=400)
    with open(data_path, encoding="ISO-8859-1") as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            try:
                row['Body'] = remove_html_tags(row['Body'])
                black_list = {"OwnerUserId", "CreationDate", "Score"}
                rename = {}
                new_dict = {rename.get(key, key): val for key, val in row.items() if key not in black_list}
                es.index(index=index_name,  doc_type=doc_type, body=new_dict, ignore=400)
                count = count + 1
                if count % 10000 == 0:
                    print("Success: ", count)
            except Exception as ex :
                print("error!, skiping chunk! {}".format(ex))
                pass


index_data(data_path, 'my_data', 'tag')