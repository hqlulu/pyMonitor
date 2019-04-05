#!/usr/bin/python
from datetime import datetime
import socket, pycurl
import StringIO, json
import time, sys, threading
from elasticsearch import Elasticsearch

class MyThread(threading.Thread):
	def __init__(self, server):
		threading.Thread.__init__(self)
		self.server = server
	def run(self):
		print("start thread", server)
		check_and_save(server)
		#threadLock.acquire()
		# do something with share data
		#threadLock.release()

def check_and_save(server):
	print("start check_and_save", server, datetime.now())
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, "http://"+server[1]+"/status?json")
	curl.setopt(pycurl.HTTPHEADER, ["host:"+server[2]])
	result = StringIO.StringIO()
	curl.setopt(pycurl.WRITEFUNCTION, result.write)
	curl.perform()
	body = result.getvalue()
	print(body)
	data = json.loads(body)
	data["@timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+0800")
	data["host"] = server[0]
	data["tag"] = "thread"
	es.index(index = "fpm", doc_type="monitor", body=data)

server_list = [
	["mgc01", "172.17.83.146", "fpm9000"],
	["mgc01", "172.17.83.146", "fpm9001"]
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
		time.sleep(sleep)
