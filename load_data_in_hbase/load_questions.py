from pyspark.sql import SparkSession
from bs4 import BeautifulSoup

spark = SparkSession.builder.master("local[*]").appName("CCA") \
    .config("spark.executor.memory", "1gb") \
    .getOrCreate()

df = spark.read.format('csv').option('header', 'true').option('mode', 'DROPMALFORMED').load('hdfs://localhost:8020/cca/project/data/small/Questions_10.csv')


def remove_html_tags(text):
    soup = BeautifulSoup(text)
    return soup.getText()


rdd = df.rdd.map(lambda line: (line[0], line[1], line[2], line[3], remove_html_tags(line[4]), remove_html_tags(line[5]), line[4], line[5]))

rdd.take(2)
