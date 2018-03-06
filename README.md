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

## Architecture

* We should store our files in a cheap persistent storage, such as S3 or Azure Blob

* 