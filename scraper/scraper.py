import sys
import requests
import urllib
import simplejson


def get_alchemy_content(url):
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


""" Main Routine """
if __name__ == "__main__":
    start_term = sys.argv[1]
    print(google_urls(start_term))
