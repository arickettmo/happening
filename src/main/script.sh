#!/bin/bash

echo Creating logstash config file...


echo -n "input { twitter { consumer_key => \"e9QWQDPxITiA8Ci2V2wQ3qSoQ\" consumer_secret =>\"yjmrNsPz3PHX2owLJ1xJ7UXxHDEkdhXiKggWXBoKJMJOelI5TY\" oauth_token => \"283137973-8igpqe6RQgNPPpdAs6qoE5fLO9vNkUtDccg0Q59P\" oauth_token_secret => \"3tc5eKuIoq0C5jprUCKnHT4W8nx5aqBGCBhQ6Q7RrlgAM\" keywords => [" > /etc/logstash/conf.d/logstash_twitter.conf

awk -F ";" '{print $1}' ../../resources/places_test.csv > ../../resources/file.csv


index=0
cat ../../resources/file.csv | while read line; do
  line=( ${line//,/ } )
  if [ $index -eq 1 ]; then
            echo Logstash stream country ${line[@]}
            echo -n "\"${line[@]}\"" >> /etc/logstash/conf.d/logstash_twitter.conf
    elif [ $index -gt 1 ]; then
            echo Logstash stream country ${line[@]}
            echo -n ",\"${line[@]}\"" >> /etc/logstash/conf.d/logstash_twitter.conf
    fi
    index=$((index+1)) 
done


echo -n "] full_tweet => true } } filter { mutate { remove_field => [ \"extended_entities\", \"retweeted_status\", \"entities\", \"user\" ] }} output { elasticsearch { hosts => \"http://localhost:9200\" document_type => \"tweet\" }}" >> /etc/logstash/conf.d/logstash_twitter.conf


# Restart logstash
sudo service logstash restart