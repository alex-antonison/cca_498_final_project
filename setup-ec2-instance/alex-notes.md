
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