#!/usr/bin/env python

from alchemyapi import AlchemyAPI
import json, mysql.connector, math

GAIN = 2.0
weight = 1000.0
alchemyapi = AlchemyAPI()
afail = False
bfail = False

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
	global afail, bfail
	connect = 0
	total = 0
	responsea = alchemyapi.concepts('url', urla)
	responseb = alchemyapi.concepts('url', urlb)
	if responsea['status'] != 'OK' or responseb['status'] != 'OK':
		if responsea['status'] != 'OK':
			print('A: '+urla)
			afail = True
		else:
			print('B: '+urlb)
			bfail = True
		return None
	for conceptb in responseb['concepts']:
		total += float(conceptb['relevance'])
	for concepta in responsea['concepts']:
		total += float(concepta['relevance'])
		for conceptb in responseb['concepts']:
			if conceptb['text'] == concepta['text']:
				connect += math.sqrt(float(conceptb['relevance']) * float(concepta['relevance']))
	return GAIN * connect / (total + 0.000001)

def main(conn):
	global afail, bfail
	cursora = conn.cursor(buffered=True)
	cursorb = conn.cursor(buffered=True)
	cursori = conn.cursor(buffered=True)
	cursora.execute("SELECT id, url FROM sites")
	rowa = cursora.fetchone()
	afail = False
	while rowa is not None:
		print("\t"+str(rowa[1]))
		cursorb.execute("SELECT id, url FROM sites")
		rowb = cursorb.fetchone()
		bfail = False
		while rowb is not None:
			print("\t"+str(rowb[1]))
			cursori.execute("SELECT * FROM connections WHERE (site_id=" + str(rowa[0]) + " AND from_id=" + str(rowb[0]) + ") OR (site_id=" + str(rowb[0]) + " AND from_id=" + str(rowa[0]) + ") LIMIT 1;")
			conn.commit()
			if ((rowa[0] != rowb[0]) and (len(cursori.fetchall()) == 0)):
				connects = compareconcepts(str(rowa[1]), str(rowb[1]))
				print("\t\t"+str(connects))
				if (connects is not None):
					cursori.execute("INSERT INTO connections (site_id, from_id, connections) VALUES (" + str(rowa[0]) + ", " + str(rowb[0]) + ", " + str(connects * weight) + ");")
					print(afail)
				elif afail:
					break

#				print("INSERT INTO connections (site_id, from_id, connections) SELECT " + str(rowa[0]) + ", " + str(rowb[0]) + ", " + str(compareconcepts(str(rowa[1]), str(rowb[1])) * weight) + " FROM dual WHERE NOT EXISTS (SELECT 1 FROM connections WHERE (site_id=" + str(rowa[0]) + " AND from_id=" + str(rowb[0]) + ") OR (site_id=" + str(rowb[0]) + " AND from_id=" + str(rowa[0]) + "))")
				conn.commit()
			rowb = cursorb.fetchone()
			bfail = False
		rowa = cursora.fetchone()
		afail = False

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
