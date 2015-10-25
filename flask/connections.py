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
    return cur.execute('SELECT site_id FROM users_join ORDER BY date DESCENDING LIMIT 5;').fetchall()

def get_weight(site):
    cur = conn.cursor()
    weight = cur.execute('SELECT SUM(connections) FROM connections WHERE (site_id=%s OR from_id=%s);', (site, site)).fetchone()
    conn.commit()
    print(weight)
    return weight

def main(uid):
    usersites = get_recent_sites(5)
    allsites = list(usersites)  # copy usersites
    for site in usersites:
        cur = conn.cursor()
        neighbors = cur.execute('SELECT siteid, connections FROM sites, connections WHERE sites.id = connections.site_id AND (site_id=%s OR from_id=%s);', (site, site))
        conn.commit()
        if(len(neighbors)==0):
            print("neighbors is empty")
        else:
            for neighbor in neighbors.fetchall():
                neighborid = neighbor[0]
                if(neighborid not in allsites):
                    allsites.append(neighborid)
    scores = []
    for site in allsites:
        scores.append((site, get_weight(site)))
    print(scores)


if __name__ == "__main__":
    main(1)
