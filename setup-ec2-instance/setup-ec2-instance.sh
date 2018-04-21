# Assumes you have run the following command
# git clone https://github.com/alex-antonison/setup-cca-project.git
# Ec2 instance notes
# OS: Ubuntu - ami-43a15f3e
# Size: m5.2xlarge
# Configuration Details - Leave default
# Storage - EBS: 100 GB EBS
# Tags - Key:Name, Label:"cca-project"
# Security Group
# Type            | Protocol | Port Range | Source
# ---------------------------------------------------
# Custom TCP Rule | TCP      | 8080       | Anywhere
# HTTP            | TCP      | 80         | Anywhere
# HTTPS           | TCP      | 443        | Anywhere
# SSH             | TCP      | 22         | Anywhere
# Custom TCP Rule | TCP      | 7474       | Anywhere
# Custom TCP Rule | TCP      | 5601       | Anywhere
# Custom TCP Rule | TCP      | 9090       | Anywhere

# Although you can start off without using a keypair, it is highly recommended to create and use one.

# Updating instance
# git clone https://github.com/alex-antonison/setup-cca-project.git

sudo apt-get update && sudo apt-get upgrade -y
mkdir local-dir

# Installing and starting Docker
sudo apt install docker.io -y

# Setup Python Ubuntu
sudo apt-get install python3-pip -y 
sudo pip3 install --upgrade pip
sudo pip3 install happybase
sudo pip3 install thrift
sudo pip3 install pandas
sudo pip3 install bs4
sudo pip3 install pyspark
sudo pip3 install neo4j-driver
sudo pip3 install html5lib
sudo pip3 install elasticsearch
sudo pip3 install flask

# Setup docker network
sudo docker network create my-net

# Setup neo4j
## Had to go back to 3.0 to get a working version
sudo docker run -d --privileged --restart unless-stopped \
    --network my-net \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    --volume=$HOME/neo4j/logs:/logs \
    --name neo4j \
    neo4j:3.0

# Setup Elasticsearch
sudo docker run -d --restart unless-stopped \
    --network my-net \
    -p 9200:9200 \
    -p 9300:9300 \
    --name elasticsearch \
    -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.2.3

# Seutp Kibana
sudo docker run -d --restart unless-stopped \
    --network my-net \
    -p 5601:5601 \
    -e ELASTICSEARCH_URL=http://elasticsearch:9200 \
    --name kibana \
    docker.elastic.co/kibana/kibana:6.2.3

# Setup Java
echo debconf shared/accepted-oracle-license-v1-1 select true | \
sudo debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | \
sudo debconf-set-selections

sudo add-apt-repository ppa:webupd8team/java -y
sudo apt-get update
sudo apt-get install oracle-java8-installer -y

echo "export PYSPARK_PYTHON=/usr/bin/python3" > ~/.bash_profile
source ~/.bash_profile

# Setting up hortonworks vm
# chmod 770 setup-cca-project/start-sandbox-hdp-standalone_2-6-4.sh
sudo ~/./cca_498_final_project/setup-ec2-instance/start-sandbox-hdp-standalone_2-6-4.sh