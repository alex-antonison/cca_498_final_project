# cca_498_final_project

## Collaboration

* When working on code, I recommend we maintain a develop branch that we check features into and once we have a baseline, we merge that into master.

* When developing off of develop, a new feature branch should start with feature and then be the branch name such as feature/adjusting-topic-model.

## Server Setup

- Start hadoop
    - `/usr/local/Cellar/hadoop/<version>/sbin/start-dfs.sh`
    - `/usr/local/Cellar/hadoop/<version>/sbin/start-yarn.sh`
- Start HBase 
    - `/usr/local/Cellar/hbase/<version>/bin/start-hbase.sh`
    - `hbase thrift start -p 9090 --infoport 9095`
    - `/usr/hdp/current/hbase-master/bin/hbase-daemon.sh start thrift -p <port> --infoport <infoport>`

- Start Neo4J

## Setup

### HBase
Create following two tables
- `create 'questions','raw','mod'`
- `create 'answers','raw','mod'`

### Neo4j
- Database Name : `cca`
- User Name : `neo4j`
- Password : `cca`
- url : `bolt://localhost:7687`

#### Clean DB
- `MATCH (n); DETACH DELETE n`
- `create index on :Question(id);`

### Data

#### Answers


| Id|OwnerUserId|        CreationDate|ParentId|Score|                Body|
|---|-----------|:-------------------|:-------|:----|:-------------------|
|497|         50|2008-08-02T16:56:53Z|     469|    4|<p>open up a term...|
|518|        153|2008-08-02T17:42:28Z|     469|    2|<p>I haven't been...|
|536|        161|2008-08-02T18:49:07Z|     502|    9|"<p>You can use I...|
|538|        156|2008-08-02T18:56:56Z|     535|   23|<p>One possibilit...|
|595|        116|2008-08-03T01:17:36Z|     594|   25|<p>The canonical ...|
|735|        145|2008-08-03T15:47:22Z|     683|   -2|     <p>I think:</p>|
|745|        154|2008-08-03T15:59:19Z|     683|    8|"<p>Are you looki...|
|750|        199|2008-08-03T16:13:29Z|     683|    2|<p>What I was thi...|
|764|         NA|2008-08-03T17:40:25Z|     742|    0|<p>Sounds to me l...|
|777|        150|2008-08-03T18:32:27Z|     766|    5|"<p>I don't have ...|

## Execution Sequence

- Save the file in UTF-8 format ( manual )
- Pre-Processor Scripts
    - `q_pre_processor.py`
    - `a_pre_processor.py`
- Load Data into HBase and Neo4J
    - `process_questions.py`
    - `process_answers.py`

## Additional Queries
- `MATCH (a)-[:ANS_OF]->(b)
RETURN b, COLLECT(a) as Questions
ORDER BY SIZE(Questions) DESC LIMIT 5`


## Architecture

* We should store our files in a cheap persistent storage, such as S3 or Azure Blob

