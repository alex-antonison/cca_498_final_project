# setup-cca-project

Once cloned, you need to execute the setup-ec2-instance.sh script.  In this script the following things are done:
- Setup Docker Instances for the Following
    - Hortonworks Sandbox HDP (Hadoop, HBase, Spark)
    - Neo4j
        - Had to use an older verison of Neo4j since the latest version had issues initializing
    - Elasticsearch
    - Kibana connected to Elasticsearch
- Install Python3
- Install and upgrade Pip3
- Install Python Libraries
    - happybase
    - thrift
    - pandas
    - bs4
    - pyspark
    - neo4j-driver
- Install Java