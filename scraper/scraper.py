import sys
import requests
import urllib
import simplejson
import mysql.connector
from alchemyapi import AlchemyAPI


alchemyapi = AlchemyAPI()
concepts_interned = []


def commit_url(url):
    """ Add all urls from urls_interned list to mySQL database """
    try:
        conn = mysql.connector.connect(host='localhost', database='study', user='root', password='password')
        if not (conn.is_connected()):
            print('Could not connect to MySQL database')
            exit()
        cur = conn.cursor()
        cur.execute('INSERT INTO sites (url, visits) SELECT \''+url+'\', 1000 FROM DUAL WHERE NOT EXISTS (SELECT url FROM sites WHERE url=\''+url+'\') LIMIT 1;')
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
        exit()
    else:
        conn.close()

def get_alchemy_concepts(url):
    """ TODO """
    response = alchemyapi.concepts('url', url)
    if response['status'] != 'OK': return None
    return response['concepts']

def google_urls(term):
    """ return list of urls returned by google search """
    urls = []
    url = ('https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%sn&userip=USERS-IP-ADDRESS' % urllib.quote_plus(term))
    response = requests.get(url).content
    results = simplejson.loads(response)
    if results['responseStatus'] != 200: return []
    for result in results['responseData']['results']:
        urls.append(result['unescapedUrl'])
    return urls

def intern_concept(concept):
    """ main recursive function """
    global concepts_interned
    concepts_interned.append(concept)
    urls = google_urls(concept)
    if(len(urls)!=0):
        commit_url(urls[0])
        concepts = get_alchemy_concepts(urls[0])
        for concept in concepts:
            if concept not in concepts_interned:
                intern_concept(concept['text'])
                break


if __name__ == "__main__":
    """ Main Routine """
    start_term = sys.argv[1]
    intern_concept(start_term)

