#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json
import re
import urllib.parse
import urllib.request
import urllib.error

filenames = [
    'cnn-nxivm-trial-week-1-wrap.html',
    'foxnews-ben-shapiro-bbc-host-andrew-neil-destroyed-him.html',
    'wapo-nike-takes-beating-after-zion-williamsons-shoe-explodes.html'
]

##############################################################################

valid_at_types = set(['AnalysisNewsArticle',
    'AskPublicNewsArticle',
    'BackgroundNewsArticle',
    'OpinionNewsArticle',
    'ReportageNewsArticle',
    'ReviewNewsArticle',
    'NewsArticle'])

def scrape_metadata(html):
    if html is None:
        return []
    ld_jsons = []
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup.find_all('script'):
        if script.attrs.get('type') == 'application/ld+json':
            try:
                ld_json = json.loads(script.text)
            except json.decoder.JSONDecodeError:
                try:
                    ld_json = json.loads(re.sub(',\s*}\s*$', '}', script.text))
                except json.decoder.JSONDecodeError:
                    continue
            if ld_json is None:
                ld_json = {}
            if ld_json.get('@type') in valid_at_types:
                ld_jsons.append(json.dumps(ld_json))
    return ld_jsons

def get_domain(url):
    domain = urllib.parse.urlparse(url).netloc
    if domain[:4] == 'www.':
        domain = domain[4:]
    return domain

def scrape_url(url, cnt):
    with urllib.request.urlopen(url.strip()) as response:
            if response.code == 200:
                ld_jsons = scrape_metadata(response.read())
                with open(str(cnt) + '.json', 'w') as file_obj:
                    for ldj in ld_jsons:
                        file_obj.write(ldj + "\n")

##############################################################################

cnt = 5
with open('urls.txt') as urls:
    for raw_url in urls:
        url = raw_url.strip()
        print('scraping', cnt, url)
        try:
            scrape_url(url, cnt)
        except urllib.error.HTTPError as e:
            print(str(e))
        cnt += 1
