#!/bin/bash

echo Creating logstash config file...


echo -n "input { twitter { consumer_key => \"BYvnonTRKhTSMYEjZ1hqvbh4c\" consumer_secret =>\"n4XZz4wpcJWRYbLbhm1XlxvSxCzn4v8Rfg51omRblYX7qbab8I\" oauth_token => \"283137973-L97BLGeunsf8r8b5Xh8MDVeswFI0B93shjUJZ3OW\" oauth_token_secret => \"RL2iejRKSODZ7Ts6NwOLFpPjNj9vSqnNbrZZ8MTB4lt2G\" keywords => [" > /etc/logstash/conf.d/logstash_twitter.conf

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
