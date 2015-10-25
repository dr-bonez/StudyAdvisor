#!/usr/bin/python
import mysql.connector



def printd(string):
    if __name__ == "__main__":
        print(string)

def get_recent_sites(uid, conn, n=1):
    """ return a list of the last n siteids a user has visited """
    cur = conn.cursor()
    recent = []
    cur.execute('SELECT site_id FROM users_join ORDER BY date DESC LIMIT 5;')
    for site in cur.fetchall():
        recent.append(site[0])
    conn.commit()
    return recent;

def get_weight(site, conn):
    cur = conn.cursor()
    cur.execute('SELECT SUM(connections) FROM connections WHERE (site_id=%s OR from_id=%s);', (site, site))
    weight = cur.fetchone()[0]
    conn.commit()
    return int(weight)

def get_url(site, conn):
    cur = conn.cursor()
    cur.execute('SELECT url FROM sites WHERE (id=%s);', (site,))
    url = cur.fetchone()[0]
    conn.commit()
    return url

def get_suggestions(uid, max_len):
    """
    :param uid: The userid
    :return: A at list of length at most max_len (userid, connection) tuples sorted by connection in descending order
    """
    conn = mysql.connector.connect(host='localhost', database='study', user='root', password='password')
    usersites = get_recent_sites(5, conn)
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
        scores.append((site, get_weight(site, conn)))
    scores = sorted(scores, key=lambda x: x[1], reverse = True)
    # return corresponding urls
    urls = []
    for score in scores:
        site = score[0]
        urls.append((site, get_url(site, conn)))
    return urls[:max_len]
