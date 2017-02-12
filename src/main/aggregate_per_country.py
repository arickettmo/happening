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
    with open('places_test.csv', 'rU') as csvfile:
        places_file = csv.reader(csvfile, delimiter=',', quotechar='|')
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
    
    print response
    
#    places_volume={}
#    data={ "country": [], "code": [], "volume_a": [], "volume_b": [], "diff": [] }
#    pointer=0
#    for index,place in enumerate(places):
#        for index_b in range(0, 2):
#            if index_b==0:
#                volume_a=response["responses"][pointer+index_b]["hits"]["total"]
#                if volume_a==0:
#                    volume_a=1
#            else:
#                volume_b=response["responses"][pointer+index_b]["hits"]["total"]
#                diff=((volume_b-volume_a)/volume_a)*100
#        pointer+=2
#        data["country"].append(place["country"])
#        data["code"].append(place["code"])
#        data["volume_a"].append(volume_a)
#        data["volume_b"].append(volume_b)
#        data["diff"].append(diff)
#    print "Content-type: text/html\n\n";
#    print json.dumps(data)   