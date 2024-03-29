import sys
import requests
import urllib
import re
import mysql.connector
from alchemyapi import AlchemyAPI


conn = None
alchemyapi = AlchemyAPI()
concepts_interned = []


def connect(start_term):
    """ Add all urls from urls_interned list to mySQL database """
    try:
        global conn
        conn = mysql.connector.connect(host='localhost', database='study', user='root', password='password')
        if not (conn.is_connected()):
            print('Could not connect to MySQL database')
            exit()
        intern_concept(start_term)
    except mysql.connector.Error as e:
        print(e)
        exit()
    else:
        conn.close()

def commit_urls(urls):
    global conn
    cur = conn.cursor()
    for url in urls:
        print(url)
        if(0==len(cur.execute("SELECT * FROM sites WHERE url='%s' LIMIT 1;" % url).fetchall())):  # can't handle titles with apostrophes
            cur.execute("INSERT INTO sites (url, visits) VALUES (%s, 1000) ;" % url)
        conn.commit()

def get_alchemy_concepts(url):
    """ get alchemy concepts """
    response = alchemyapi.concepts('url', url)
    print(response)
    if response['status'] != 'OK': return None
    return response['concepts']

def google_urls(term):
    """ return list of urls returned by google search """
    url = ('https://www.google.com/search?q=%s' % urllib.quote_plus(term))
    print('Scraping from url:  '+url)
    html = requests.get(url).content
    print('Response size: '+str(len(html)))
    regex = re.compile('class=\"r\"><a href=\"\/url\?q=http.*?\"')
    return [x[26:x.find("&amp;")] for x in regex.findall(html)]

def url_in_db(url):
    cur = conn.cursor()
    in_db = (1==len(cur.execute("SELECT * FROM sites WHERE url='%s' LIMIT 1;" % url).fetchall()))
    conn.commit()
    return in_db

def intern_concept(concepttext):
    """ main function """
    global concepts_interned
    concepts_interned.append(concepttext)
    urls = google_urls(concepttext)
    for url in urls:
        if(url_in_db(url)): urls.remove(url)  # removes urls already in db
        print('Removed url: '+url)
    commit_urls(urls)
    if(len(urls)!=0):
        i=0
        concepts = get_alchemy_concepts(urls[i])
        out = False
        while(concepts is None and i < len(urls)-1):
            i = i+1
            concepts = get_alchemy_concepts(urls[i])
            print(concepts)
        if (concepts is not None):
            for concept in concepts:
                print('Checking concept: '+str(concept['text']))
                if str(concept['text']) not in concepts_interned:
                    intern_concept(str(concept['text']))
                    break
                else:
                    print(str(concept['text'])+' is already in concepts_interned')
    else:
        print('urls is empty')


if __name__ == "__main__":
    """ Main Routine """
    concepts_interned
    start_term = sys.argv[1]
    connect(start_term)
    print(concepts_interned)

