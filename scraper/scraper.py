import sys
import requests
import urllib
import simplejson


concepts_interned = []
urls_interned = []


def commit_urls():
    """ Add all urls from urls_interned list to mySQL database """
    pass

def get_alchemy_concepts(url):
    """ TODO """
    pass

def google_urls(term):
    """ return list of urls returned by google search """
    urls = []
    url = ('https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%sn&userip=USERS-IP-ADDRESS' % urllib.parse.quote_plus(term))
    response = requests.get(url).content
    results = simplejson.loads(response)
    for result in results['responseData']['results']:
        urls.append(result['unescapedUrl'])
    return urls


def intern_concept(concept):
    """ main recursive function """
    global concepts_interned
    urls = google_urls(start_term)
    concepts = get_alchemy_concepts(urls[0])
    if concepts[0] not in concepts_interned:
        concepts_interned.append(concepts[0])

""" Main Routine """
if __name__ == "__main__":
    start_term = sys.argv[1]
    intern_concept(start_term)

