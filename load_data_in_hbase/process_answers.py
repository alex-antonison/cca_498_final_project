from pyspark.sql import SparkSession
from bs4 import BeautifulSoup
import happybase
from neo4j.v1 import GraphDatabase

server = "localhost"
table_name = "answers"


def remove_html_tags(text):
    # try:
    soup = BeautifulSoup(text, 'html5lib')
    return soup.getText()
    # except:
    #     print(text)


def remove_bad_record(line):
    if len(line) == 6:
        # try:
        val = int(line[0])
        return True
        # except:
        #     return False
        #     print(line)
    else:
        print("Removed bad record")
        return False


def bulk_insert_hbase(batch):
    table = happybase.Connection(server).table(table_name)
    for t in batch:
        # try:
        key = t[0]
        value = {"raw:OwnerUserId": t[1],
                    "raw:CreationDate": t[2],
                    "raw:ParentId": t[3],
                    "raw:Score": t[4],
                    "raw:Body": t[5],
                    "mod:Body": t[6]
                    }
        table.put(key, value)
        # except:
        #     print(t)


class InsertAnswerData(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def save_node(self, id, owner_id, created_dt, parent_id, score):
        with self._driver.session() as session:
            session.write_transaction(self._create_node_tx, id, owner_id, created_dt, parent_id, score)

    @staticmethod
    def _create_node_tx(tx, id, owner_id, created_dt, parent_id, score):
        tx.run("CREATE (a:Answer {title:$id, id:$id, owner_id:$owner_id, created_dt:$created_dt,parent_id:$parent_id,score:$score}) "
               "WITH a "
               "MATCH (q:Question {id: $parent_id}) "
               "MERGE (a)-[:ANS_OF]->(q)", id=id, owner_id=owner_id, created_dt=created_dt,
               parent_id=parent_id, score=score)


def covert_to_int(val):
    if val == 'NA':
        return -1
    else:
        return int(float(val))


def batch_insert_graph(batch):
    adapator = InsertAnswerData('bolt://localhost:7687', 'neo4j', 'cca')
    for t in batch:
        adapator.save_node(covert_to_int(t[0]), covert_to_int(t[1]), t[2], covert_to_int(t[3]), covert_to_int(t[4]))

    adapator.close()


spark = SparkSession.builder.master("local[*]").appName("CCA") \
    .config("spark.debug.maxToStringFields", 999999) \
    .config("spark.executor.memory", "10gb") \
    .getOrCreate()

df = spark.read.format('csv').option('header', 'true').option('mode', 'DROPMALFORMED').load('hdfs://localhost:8020/demo/data/CCA/Answers_New.csv')

rdd = df.rdd.filter(lambda line: remove_bad_record(line=line))

# # Remove HTML tags
rdd = rdd.map(lambda line: (line[0], line[1], line[2], line[3], line[4], line[5], remove_html_tags(line[5])))

rdd.foreachPartition(bulk_insert_hbase)

# rdd.foreachPartition(batch_insert_graph)

spark.stop()
