#!/usr/bin/env python

from alchemyapi import AlchemyAPI
import json, mysql.connector

GAIN = 2.0
alchemyapi = AlchemyAPI()

def connect():
	try:
		conn = mysql.connector.connect(host='localhost', database='study', user='root', password='password')
		if not (conn.is_connected()):
			print('Could not connect to MySQL database')
			exit()
	except mysql.connector.Error as e:
		print(e)
		exit()
	else:
		conn.close()

def compareconcepts(urla, urlb):
	connect = 0
	responsea = alchemyapi.concepts('url', urla)
	responseb = alchemyapi.concepts('url', urlb)
	if responsea['status'] != 'OK' or responseb['status'] != 'OK':
		print('alchemy is fail')
		exit()
	for concepta in responsea['concepts']:
		for conceptb in responseb['concepts']:
			if conceptb['text'] == concepta['text']:
				connect += float(conceptb['relevance']) * float(concepta['relevance'])
	return GAIN * connect / len(responsea)

if __name__ == '__main__':
	connect()
	print(compareconcepts("https://en.wikipedia.org/wiki/Mathematics", "http://mathematics.stanford.edu/"))
#response = alchemyapi.concepts('url', demo_url)

#if response['status'] == 'OK':
#    print(json.dumps(response, indent=4))
#
#    for concept in response['concepts']:
#        print('text: ', concept['text'])
#        print('relevance: ', concept['relevance'])
#else:
