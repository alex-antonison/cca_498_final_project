from flask import Flask, request, jsonify, send_from_directory
import happybase
import textwrap
from neo4j.v1 import GraphDatabase
from elasticsearch import Elasticsearch
import time
app = Flask(__name__)


class GetAnswerCount(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def get_answers_count(self, id):
        with self._driver.session() as session:
            return session.write_transaction(self._get_answers_count, id)

    @staticmethod
    def _get_answers_count(tx, id):
        result = tx.run("MATCH (q:Question {id: $id}) MATCH (a)-[:ANS_OF]->(q) RETURN count(a)", id=int(id))
        count = 0
        for record in result:
            count = record["count(a)"]
        return count


def batch_insert_graph(id):
    adapator = GetAnswerCount('bolt://localhost:7687', 'neo4j', 'neo4j')
    count = adapator.get_answers_count(id)

    adapator.close()
    return count


@app.route('/get_questions/<question>', methods=['GET'])
def get_random_questions_from_hbase(question):
    start_time = time.time()
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    response = search_es(es, question)

    hits = response['hits']['total']

    row_data = {}

    for hit in response['hits']['hits']:
        if 'Body' in hit["highlight"]:
            row_data[hit["_source"]["Id"]] = ({'body': " ... ".join(hit["highlight"]["Body"]).replace("\"", ""),
                                               'title': " ... ".join(hit["highlight"]["Title"]),
                                               # 'date': data[b'raw:CreationDate'].decode("utf-8"),
                                               # 'ownerid': data[b'raw:OwnerUserId'].decode("utf-8"),
                                               # 'score': data[b'raw:Score'].decode("utf-8"),
                                               # 'tags': str(data[b'mod:Tags'].decode("utf-8")).split(','),
                                               'count': batch_insert_graph(hit["_source"]["Id"])
                                               })

    time_taken=(time.time() - start_time)

    '''
    connnection = happybase.Connection("localhost")
    table = connnection.table("questions")
    rows = table.rows([b'23721800', b'14853757', b'19170111', b'23059398', b'26580944', b'29748897', b'32765572', b'38056227', b'4590516', b'9998815'])

    connnection.close()

    row_data = {}

    for key, data in rows:
        try:
            if b'mod:Tags' in data:
                row_data[key.decode("utf-8")] = ({'body': data[b'raw:Body'].decode("utf-8").replace("\"", ""),
                                                  'title': data[b'mod:Title'].decode("utf-8"),
                                                  'date': data[b'raw:CreationDate'].decode("utf-8"),
                                                  'ownerid': data[b'raw:OwnerUserId'].decode("utf-8"),
                                                  'score': data[b'raw:Score'].decode("utf-8"),
                                                  'tags': str(data[b'mod:Tags'].decode("utf-8")).split(','),
                                                  'count': batch_insert_graph(key.decode("utf-8"))
                                                  })
            else:
                row_data[key.decode("utf-8")] = ({'body': textwrap.shorten(data[b'raw:Body'].decode("utf-8").replace("\"", ""), width=500, placeholder="..."),
                                                  'title': data[b'mod:Title'].decode("utf-8"),
                                                  'date': data[b'raw:CreationDate'].decode("utf-8"),
                                                  'ownerid': data[b'raw:OwnerUserId'].decode("utf-8"),
                                                  'score': data[b'raw:Score'].decode("utf-8"),
                                                  'tags': [],
                                                  'count': batch_insert_graph(key.decode("utf-8"))
                                                  })

        except:
            print("Error")

    return jsonify(row_data)
    '''

    return jsonify({'data':row_data,'total':hits,'time':time_taken})


class GetAnswersIDs(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def get_answers_id(self, id):
        with self._driver.session() as session:
            return session.write_transaction(self._get_answers_count, id)

    @staticmethod
    def _get_answers_count(tx, id):
        result = tx.run("MATCH (q:Question {id: $id}) MATCH (a)-[:ANS_OF]->(q) RETURN a.id", id=int(id))
        answer_ids = []
        for record in result:
            answer_ids.append(record["a.id"])
        return answer_ids


def graph_get_answers_id(id):
    adapator = GetAnswersIDs('bolt://localhost:7687', 'neo4j', 'neo4j')
    answer_ids = adapator.get_answers_id(id)

    adapator.close()
    return answer_ids


def hbase_get_answers(answer_ids):
    encoded_ids = []

    for id in answer_ids:
        encoded_ids.append(bytes((str)(id), encoding='utf-8'))

    #print(encoded_ids)

    connnection = happybase.Connection("localhost")
    table = connnection.table("answers")
    rows = table.rows(encoded_ids)

    connnection.close()

    row_data = {}

    for key, data in rows:
        try:
            row_data[key.decode("utf-8")] = ({'body': data[b'raw:Body'].decode("utf-8").replace("\"", ""),
                                              'date': data[b'raw:CreationDate'].decode("utf-8"),
                                              'user_id': data[b'raw:OwnerUserId'].decode("utf-8"),
                                              'score': data[b'raw:Score'].decode("utf-8")
                                              })
        except:
            print("Error")

    return row_data


def get_question_from_hbase(id):
    connnection = happybase.Connection("localhost")
    table = connnection.table("questions")
    row = table.row(bytes((str)(id), encoding='utf-8'))

    connnection.close()

    row_data = {'body': row[b'raw:Body'].decode("utf-8").replace("\"", ""),
                'title': row[b'mod:Title'].decode("utf-8"),
                'date': row[b'raw:CreationDate'].decode("utf-8"),
                'ownerid': row[b'raw:OwnerUserId'].decode("utf-8"),
                'score': row[b'raw:Score'].decode("utf-8")
                }

    return row_data


@app.route('/get_answers_for_question/<qid>', methods=['GET'])
def get_answers_for_question(qid):
    answer_ids = graph_get_answers_id(qid)
    data = {'q': get_question_from_hbase(qid), 'a': hbase_get_answers(answer_ids)}

    return jsonify(data)


def search_es(es, term):
    res = es.search(
        index="my_data",
        doc_type="tag",
        body={
            "from": 0, "size": 10,
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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
