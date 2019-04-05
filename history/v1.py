#!/usr/bin/python
import pycurl
import StringIO

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

server = ["lhq01", "172.17.83.146", "fpm9000"]
check_and_save(server)