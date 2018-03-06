from pyspark.sql import SparkSession
from bs4 import BeautifulSoup
import happybase

server = "localhost"
table_name = "questions"

spark = SparkSession.builder.master("local[*]").appName("CCA") \
    .config("spark.executor.memory", "1gb") \
    .getOrCreate()

df = spark.read.format('csv').option('header', 'true').option('mode', 'DROPMALFORMED').load('hdfs://localhost:8020/cca/project/data/small/Questions_10.csv')


def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html5lib')
    return soup.getText()


# Remove HTML tags
rdd = df.rdd.map(lambda line: (line[0], line[1], line[2], line[3], line[4], line[5], remove_html_tags(line[4]), remove_html_tags(line[5])))


def bulk_insert(batch):
    table = happybase.Connection(server).table(table_name)
    for t in batch:
        key = t[0]
        value = {"raw:OwnerUserId": t[1],
                 "raw:CreationDate": t[2],
                 "raw:Score": t[3],
                 "raw:Title": t[4],
                 "raw:Body": t[5],
                 "mod:Title": t[6],
                 "mod:Body": t[7]
                 }

        print(key, value)
        table.put(key, value)


rdd.foreachPartition(bulk_insert)



spark.stop()
