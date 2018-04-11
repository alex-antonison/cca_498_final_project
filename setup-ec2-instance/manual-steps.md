### Manual Steps

Note, when rebooting, all you should have to do is the following:
sudo docker exec -t sandbox-hdp /root/start-sandbox-hdp.sh

I have had some issues with Kibana restarting gracefully, in the event that hapepns, execute the following commands.


### Step 1 - Setup AWS instance
Ec2 instance notes
OS: Ubuntu - ami-43a15f3e (Default Ubuntu)
Size: m5.2xlarge (if you are getting poor performance, use m5.4xlarge)
Configuration Details - Leave default
Storage - EBS: 100 GB EBS
Tags - Key:Name, Label:"cca-project"
Security Group
Type            | Protocol | Port Range | Source
---------------------------------------------------
Custom TCP Rule | TCP      | 8080       | Anywhere
HTTP            | TCP      | 80         | Anywhere
HTTPS           | TCP      | 443        | Anywhere
SSH             | TCP      | 22         | Anywhere
Custom TCP Rule | TCP      | 7474       | Anywhere
Custom TCP Rule | TCP      | 5601       | Anywhere

### Step 1 - Setup SSH Tunnel Based on instance
ssh -i "[aws-key-pair.pem]]" -N \
-L 8080:[ip.amazonaws.com]:8080 \
-L 7474:[ip.amazonaws.com]:7474 \
-L 5601:[ip.amazonaws.com]:5601 \
 ubuntu@[ip.amazonaws.com]

 Example

 ssh -i "aws-boinc-key.pem" -N \
-L 8080:ec2-34-203-224-198.compute-1.amazonaws.com:8080 \
-L 7474:ec2-34-203-224-198.compute-1.amazonaws.com:7474 \
-L 5601:ec2-34-203-224-198.compute-1.amazonaws.com:5601 \
 ubuntu@ec2-34-203-224-198.compute-1.amazonaws.com

### Wait until you see Ambari is up and running on port 8080
### If you do it beforehand, it can cause issues with HDFS

### Step 2 - Set the password in ambari
### Default password is: hadoop
### Gets you into the sandbox-hdp docker
ssh root@127.0.0.1 -p 2222
### Resets ambari-admin-password
ambari-admin-password-reset

### Step 3 - Kick off the start all
sudo docker exec -t sandbox-hdp /root/start-sandbox-hdp.sh

### Step 4 - Go to localhost:8080 in browser
### Turn HBase service on

### Step 5 - Once all services are up and running, need to start hbase
ssh root@127.0.0.1 -p 2222
hbase thrift start &

### Step 6 - Test that hbase is working by running the below code in python3 shell
import happybase as hb
con = hb.Connection()
con.create_table('mytable2', {'cf': {}})

### Step 7 - In Amabari (localhost:8080) - Import files into HDFS using the files
### view.  You can access this by select the button to the left of hte Admin at the top right
### Put the files in the following directory
### Need to run preprocess scripts to stage Answers and Questions to get Answers_New.csv and Questions_New.csv

### Step 8 - Before running, need to source bash_profile


#######################################################################################
### Below are notes for manual commands
#######################################################################################

### Get the setup scripts on there
git clone https://github.com/alex-antonison/setup-cca-project.git

### need to reset ambari admin password - default is hadoop
### This gets you into the happy base
ssh root@127.0.0.1 -p 2222
ambari-admin-password-reset

### Once you have password change, you need to setup an ssh tunnel and connect to ambari

### How to setup a tunnel
ssh -i "aws-boinc-key.pem" -N \
-L 8080:ec2-34-203-224-198.compute-1.amazonaws.com:8080 \
-L 7474:ec2-34-203-224-198.compute-1.amazonaws.com:7474 \
-L 5601:ec2-34-203-224-198.compute-1.amazonaws.com:5601 \
 ubuntu@ec2-34-203-224-198.compute-1.amazonaws.com

ssh -i "aws-boinc-key.pem" -N \
-L 7474:ec2-34-203-224-198.compute-1.amazonaws.com:7474 \
-L 5601:ec2-34-203-224-198.compute-1.amazonaws.com:5601 \
 ubuntu@ec2-34-203-224-198.compute-1.amazonaws.com



### Put the following in your search application such as chrome or safari
http://localhost:8080/

### To start hbase
hbase thrift start &

### If you stop instance
### Do this to reboot it
sudo docker exec -t sandbox-hdp /root/start-sandbox-hdp.sh

### Will then need to ssh in and restart hbase thrift
ssh root@127.0.0.1 -p 2222
hbase thrift start &

### Python to test if it works
import happybase as hb
con = hb.Connection()
con.create_table('mytable2', {'cf': {}})


ssh -i "aws-boinc-key.pem" -N -L 7474:ec2-34-207-195-216.compute-1.amazonaws.com:7474 \
ubuntu@ec2-34-207-195-216.compute-1.amazonaws.com