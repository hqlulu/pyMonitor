#!/usr/bin/python
from datetime import datetime
import socket, pycurl
import StringIO, json
import time, sys
from elasticsearch import Elasticsearch

def check_and_save(server):
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, "http://"+server[1]+"/status?json")
	curl.setopt(pycurl.HTTPHEADER, ["host:"+server[2]])
	result = StringIO.StringIO()
	curl.setopt(pycurl.WRITEFUNCTION, result.write)
	curl.perform()
	body = result.getvalue()
	print(server)
	print(body)
	data = json.loads(body)
	#print(data)
	data["@timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+0800")
	data["host"] = server[0]
	#print(data)
	es.index(index = "fpm", doc_type="monitor", body=data)

list = [
	["mgc01", "172.17.83.146", "fpm9000"],
	["mgc01", "172.17.83.146", "fpm9001"]
]
es = Elasticsearch("172.17.83.146:9200")
length = int(sys.argv[1]) if len(sys.argv)>1 else 1
sleep = int(sys.argv[2]) if len(sys.argv)>2 else 10
for i in range(0,length):
	for server in list:
		check_and_save(server)
	time.sleep(sleep)
