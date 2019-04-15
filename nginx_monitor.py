#!/usr/bin/python
from datetime import datetime
import socket, pycurl
import StringIO, json
import time, sys, threading
from elasticsearch import Elasticsearch
import re

class MyThread(threading.Thread):
	def __init__(self, server):
		threading.Thread.__init__(self)
		self.server = server
	def run(self):
		print("start thread", self.server)
		check_and_save(self.server)
		#threadLock.acquire()
		# do something with share data
		#threadLock.release()

def check_and_save(server):
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, "http://"+server[1]+"/nginx_status")
	curl.setopt(pycurl.HTTPHEADER, ["host:"+server[2]])
	result = StringIO.StringIO()
	curl.setopt(pycurl.WRITEFUNCTION, result.write)
	curl.perform()
	body = result.getvalue()
	print("check_and_save", server, datetime.now())
	print(body)
	data = {}
	searchObj = re.search(r"Active connections: (\d+)", body)
	if searchObj:
		data['ActiveConnections'] = int(searchObj.group(1))
	searchObj = re.search(r" (\d+) (\d+) (\d+)", body)
	if searchObj:
		data['accepts'] = int(searchObj.group(1))
		data['handled'] = int(searchObj.group(2))
		data['requests'] = int(searchObj.group(3))
	searchObj = re.search(r":.+(\d+).+:.+(\d+).+:.+(\d+)", body)
	if searchObj:
		data['Reading'] = int(searchObj.group(1))
		data['Writing'] = int(searchObj.group(2))
		data['Waiting'] = int(searchObj.group(3))
	print(data)
	try:
		data["@timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+0800")
		data["host"] = server[0]
		es.index(index = "nginx_monitor", doc_type="monitor", body=data)
	except:
		print("error process json")

server_list = [
	["lhq01", "172.17.83.146", "nginx.monitor"],
	["lhq02", "172.17.83.147", "nginx.monitor"]
]

es = Elasticsearch("172.17.83.146:9200")
threadLock = threading.Lock()
threads = []

length = int(sys.argv[1]) if len(sys.argv)>1 else 1
sleep = int(sys.argv[2]) if len(sys.argv)>2 else 10
for i in range(0,length):
	for server in server_list:
		try:
			thread = MyThread(server)
			thread.start()
			threads.append(thread)
		except:
			print("error start new thread")
	for t in threads:
		t.join()
	print("tasks all done")
	if i < length-1:
		print("wait for next loop %d second", (sleep))
		time.sleep(sleep)

