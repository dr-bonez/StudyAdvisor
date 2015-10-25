#!/usr/bin/python
import mysql.connector


conn = mysql.connector.connect(host='localhost', database='study', user='root', password='password')


def printd(string):
    if __name__ == "__main__":
        print(string)

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
    weight = cur.fetchone()[0]
    conn.commit()
    return weight

def get_suggestions(uid):
    """
    :param uid: The userid
    :return: A list of (userid, connection) tuples sorted by connection in descending order
    """
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
    scores = sorted(scores, key=lambda x: x[1], reverse = True)
    return scores
