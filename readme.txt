1) Connect to AWS: 
ssh -i ~/.ssh/{name} ubuntu@{Public DNS}

2) Install elasticsearch and Kibana in Ubuntu:

-Easier as:

sudo apt-get update
sudo apt-get install elasticsearch
sudo apt-get install kibana
sudo apt-get install logstash

You may need to install the apt-transport-https package on Debian before proceeding:

sudo apt-get install apt-transport-https
Save the repository definition to /etc/apt/sources.list.d/elastic-5.x.list:
echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-5.x.list
You can install the Elasticsearch Debian package with:
sudo apt-get update && sudo apt-get install elasticsearch



-Else:

wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.2.0.deb
sha1sum elasticsearch-5.2.0.deb 
sudo dpkg -i elasticsearch-5.2.0.deb

This results in Elasticsearch being installed in /usr/share/elasticsearch/ with its configuration files placed in /etc/elasticsearch and its init script added in /etc/init.d/elasticsearch.

-Note: 

Once elasticsearch is installed you need to do the following steps:
2.1) “cat /etc/default/elasticsearch”
2.2) set the START_DAEMON parameter to true by uncommenting the line
2.3) Restart elasticsearch service by doing the following: “sudo service elasticsearch restart”.

Why? Usually the default is not to have services running until you have configured them.

3) Start elasticsearch as a service: “sudo service elasticsearch start”
4) List all services available: “systemctl -l --type service --all” or “sudo service --status-all”
5) Stop elasticsearch as a service: “sudo service elasticsearch stop”
6) See all options of elasticsearch as a service: “sudo service elasticsearch status”

For Kibana: wget https://artifacts.elastic.co/downloads/kibana/kibana-5.2.0-amd64.deb

7) Install apache: 

sudo apt install apache2

8) List all services and ports being used:

sudo lsof -i -n -P

9) Logstash configuration file is stored in:

/etc/logstash/conf.d/

10) If the operating system does not let you create the file in the configuration folder of logstash then just execute script.sh and the file output twitter.logstash move it to /etc/logstash/conf.d/. Then restart logstash.

11) Install curator: 

echo "deb http://packages.elastic.co/curator/4/debian stable main" | sudo tee -a /etc/apt/sources.list.d/curator.list

sudo apt-get update && sudo apt-get install elasticsearch-curator

For more details around installing curator:
https://www.elastic.co/guide/en/elasticsearch/client/curator/current/apt-repository.html

12) Create a shell script that runs the command of curator and leave it in the crontab daily folder (sudo mv src/main/elastic_curator.sh /etc/cron.daily/) which involves that command automatically executing it daily.
