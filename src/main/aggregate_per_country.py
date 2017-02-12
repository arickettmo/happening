#!/usr/bin/env python
import os
import json
from pprint import pprint
import datetime
from datetime import date, timedelta
from time import strftime
from elasticsearch import Elasticsearch
import csv


if __name__ == "__main__":
    
    country=""
    places=[]
    rownum=0
    with open('/home/ubuntu/happening/resources/places_test.csv', 'rU') as csvfile:
        places_file = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in places_file:
            if rownum!=0:
                colnum=0
                for col in row:
                    if colnum==0:
                        country=col
                    colnum+=1
                places.append({"country": country})
            rownum+=1
    es = Elasticsearch()
    
    search_arr = []
    
    for place in places:
        # req_head
        search_arr.append({ })
        # req_body
        search_arr.append({"query": {"bool": {"must": [{"range": {"@timestamp":{"gte": "now-1h", "lte": "now"}}},{"match": {"text": {"query": place["country"],"operator": "and"}}}]}}})

    request = ''
    for each in search_arr:
        request += '%s \n' %json.dumps(each)
        
    response = es.msearch(body=request)
    

    bulk_arr = []
    for index,place in enumerate(places):
	volume=response["responses"][index]["hits"]["total"]
	for index_b in range(0, 2):
		if index_b==0:
			bulk_arr.append({ "index":  { "_index": "tweet_volume", "_type": "volume" }})
		else:
			now = datetime.datetime.now()
        		bulk_arr.append({"country": place, "volume": volume, "timestamp": datetime.datetime(now.year, now.month, now.day, now.hour).isoformat()})

    request = ''
    for each in bulk_arr:
        request += '%s \n' %json.dumps(each)
 
 
    es.bulk(body=request, index="tweet_volume", doc_type=None, params=None)
   
