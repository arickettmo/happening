#!/usr/bin/env python
import os
import json
from pprint import pprint
import datetime
from datetime import date, timedelta
from time import strftime
import statistics
from elasticsearch import Elasticsearch
import csv


if __name__ == "__main__":
    
    country=""
    code=""
    places=[]
    rownum=0
    with open('/home/ubuntu/happening/resources/places.csv', 'rU') as csvfile:
        places_file = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in places_file:
            if rownum!=0:
                colnum=0
                for col in row:
                    if colnum==0:
                        country=col
                    elif colnum==4:
                        code=col
                    colnum+=1
                places.append({"country": country, "code": code})
            rownum+=1
    es = Elasticsearch()
    
    search_arr = []
    
    now = datetime.datetime.now()
    timestamp = datetime.datetime(now.year, now.month, now.day, now.hour).isoformat()
       

    for place in places:
        for index in range(-1, 10):
            if index==-1:
                # req_head
                search_arr.append({ })
                # req_body
                search_arr.append({"query":{"bool":{"must":[{"term":{"country.country.keyword":place["country"]}},{"term":{"timestamp":timestamp}}]}}})
            else:
                # req_head
                search_arr.append({ })
                # req_body
                # Temporary as we have data fro Feb 13th to Feb 22nd
                day = 22 - index
                timestamp = datetime.datetime(2017, 2, day, now.hour).isoformat()
                search_arr.append({"query":{"bool":{"must":[{"term":{"country.country.keyword":place["country"]}},{"term":{"timestamp":timestamp}}]}}})

    request = ''
    for each in search_arr:
        request += '%s \n' %json.dumps(each)
   


    response = es.msearch(body=request)
   
# Returning data for plotly:
#
#    data={ "country": [], "code": [], "median": [], "stdev": [], "score": [] }
#    pointer=0
#    for index,place in enumerate(places):
#	values = []
#        for index_b in range(0, 11):
#            values.append(response["responses"][pointer+index_b]["hits"]["hits"][0]["_source"]["volume"])
#        data["country"].append(place["country"])
#        data["code"].append(place["code"])
#        data["median"].append(statistics.mean(values))
#        data["stdev"].append(statistics.stdev(values))
#        if statistics.stdev(values)==0:
#            score = 0
#        else:
#	    score = (response["responses"][pointer]["hits"]["hits"][0]["_source"]["volume"]-statistics.mean(values))/statistics.stdev(values)
#        data["score"].append(score)
#        pointer+=11
 

    data=[]
    pointer=0
    for index,place in enumerate(places):
        values = []
        for index_b in range(0, 11):
            values.append(response["responses"][pointer+index_b]["hits"]["hits"][0]["_source"]["volume"])
        if statistics.stdev(values)==0:
            score = 0
        else:
            score = (response["responses"][pointer]["hits"]["hits"][0]["_source"]["volume"]-statistics.mean(values))/statistics.stdev(values)
	data.append({"country": place["country"], "code": place["code"], "mean": statistics.mean(values), "stdev": statistics.stdev(values), "score": score})
        pointer+=11

    print "Content-type: text/html\n\n";
    print json.dumps(data)   
    
    
    
    
    
#    for place in places:
#        for index in range(0, 2):
#            if index==0:
#                # req_head
#                search_arr.append({ })
#                # req_body
#                search_arr.append({"query": {"bool": {"must": [{"range": {"@timestamp":{"gt": "now-10d"}}},{"match": {"text": {"query": place["country"],"operator": "and"}}}]}}})
#            else:
#                # req_head
#                search_arr.append({ })
#                # req_body
#                search_arr.append({"query": {"bool": {"must": [{"range": {"@timestamp":{"gt": "now-1d"}}},{"match": {"text": {"query": place["country"],"operator": "and"}}}]}}})
#
#    request = ''
#    for each in search_arr:
#        request += '%s \n' %json.dumps(each)
#        
#    response = es.msearch(body=request)
#    
#    
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
