#!/usr/bin/env python

from alchemyapi import AlchemyAPI
import json, mysql.connector, math

GAIN = 2.0
weight = 1000.0
alchemyapi = AlchemyAPI()

def connect():
	try:
		conn = mysql.connector.connect(host='localhost', database='study', user='root', password='password')
		if not (conn.is_connected()):
			print('Could not connect to MySQL database')
			exit()
		main(conn)
	except mysql.connector.Error as e:
		print(e)
		exit()
	else:
		conn.close()

def compareconcepts(urla, urlb):
	connect = 0
	total = 0
	responsea = alchemyapi.concepts('url', urla)
	responseb = alchemyapi.concepts('url', urlb)
	if responsea['status'] != 'OK' or responseb['status'] != 'OK':
		print('alchemy is fail')
		exit()
	for conceptb in responseb['concepts']:
		total += float(conceptb['relevance'])
	for concepta in responsea['concepts']:
		total += float(concepta['relevance'])
		for conceptb in responseb['concepts']:
			if conceptb['text'] == concepta['text']:
				connect += math.sqrt(float(conceptb['relevance']) * float(concepta['relevance']))
	return GAIN * connect / total

def main(conn):
	cursora = conn.cursor(buffered=True)
	cursorb = conn.cursor(buffered=True)
	cursori = conn.cursor(buffered=True)
	cursora.execute("SELECT id, url FROM sites")
	rowa = cursora.fetchone()
	while rowa is not None:
		cursorb.execute("SELECT id, url FROM sites")
		rowb = cursorb.fetchone()
		while rowb is not None:
			if (rowa[0] != rowb[0]):
				cursori.execute("INSERT INTO connections (site_id, from_id, connections) SELECT " + str(rowa[0]) + ", " + str(rowb[0]) + ", " + str(compareconcepts(str(rowa[1]), str(rowb[1])) * weight) + " FROM dual WHERE NOT EXISTS (SELECT 1 FROM connections WHERE (site_id=" + str(rowa[0]) + " AND from_id=" + str(rowb[0]) + ") OR (site_id=" + str(rowb[0]) + " AND from_id=" + str(rowa[0]) + "));")
#				print("INSERT INTO connections (site_id, from_id, connections) SELECT " + str(rowa[0]) + ", " + str(rowb[0]) + ", " + str(compareconcepts(str(rowa[1]), str(rowb[1])) * weight) + " FROM dual WHERE NOT EXISTS (SELECT 1 FROM connections WHERE (site_id=" + str(rowa[0]) + " AND from_id=" + str(rowb[0]) + ") OR (site_id=" + str(rowb[0]) + " AND from_id=" + str(rowa[0]) + "))")
				conn.commit()
			rowb = cursorb.fetchone()
		rowa = cursora.fetchone()

if __name__ == '__main__':
	connect()
#response = alchemyapi.concepts('url', demo_url)

#if response['status'] == 'OK':
#    print(json.dumps(response, indent=4))
#
#    for concept in response['concepts']:
#        print('text: ', concept['text'])
#        print('relevance: ', concept['relevance'])
#else:
