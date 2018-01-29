#!/bin/bash

echo Creating logstash config file...


echo -n "input { twitter { consumer_key => \"$CONSUMER_KEY\" consumer_secret =>\"$CONSUMER_SECRET\" oauth_token => \"$OAUTH_TOKEN\" oauth_token_secret => \"$OAUTH_TOKEN_SECRET\" keywords => [" > /etc/logstash/conf.d/logstash_twitter.conf

awk -F ";" '{print $1}' ../../resources/places.csv > ../../resources/file.csv


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


echo -n "] full_tweet => true } } filter { mutate { remove_field => [ \"extended_entities\", \"retweeted_status\", \"entities\", \"user\" ] }} output { elasticsearch { hosts => \"http://localhost:9200\" index => \"logstash-%{+YYYY.MM.dd.HH}\" document_type => \"tweet\" }}" >> /etc/logstash/conf.d/logstash_twitter.conf


# Restart logstash
sudo service logstash restart
