#!/usr/bin/python
import sys
import mysql.connector

"""

Sites schema: id, url, title, description
Connections schema: id, site_id, from_id, connections

from    to  wgt
1       1
1       2
1       3

"""


conn = mysql.connector.connect(host='localhost', database='study', user='root', password='password')


def get_recent_sites(uid, n=1):
    """ return a list of the last n siteids a user has visited """
    cur = conn.cursor()
    recent = []
    cur.execute('SELECT site_id FROM users_join ORDER BY date DESC LIMIT 5;')
    for site in cur.fetchall():
        recent.append(site[0])
    conn.commit()
    return recent;

def get_weight(site):
    cur = conn.cursor()
    cur.execute('SELECT SUM(connections) FROM connections WHERE (site_id=%s OR from_id=%s);', (site, site))
    weight = cur.fetchone()
    conn.commit()
    return weight

def main(uid):
    usersites = get_recent_sites(5)
    candidatesites = []
    for site in usersites:
        cur = conn.cursor()
        cur.execute('SELECT site_id, connections FROM sites, connections WHERE sites.id = connections.site_id AND (site_id=%s OR from_id=%s);', (site, site))
        for neighbor in cur.fetchall():
            neighborid = neighbor[0]
            if(neighborid not in candidatesites and neighborid not in usersites):
                candidatesites.append(neighborid)
        conn.commit()
    scores = []
    for site in candidatesites:
        scores.append((site, get_weight(site)))
    scores = sorted(scores, key=lambda x: x[1])
    for score in scores:
        print(score)


if __name__ == "__main__":
    main(1)
