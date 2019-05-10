import json
from collections import Counter, defaultdict
from flask import render_template
from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    with open('compiled.json', 'r') as f:
        data = json.loads(f.read())

    for f in os.listdir('data/z'):
        with open(f'data/z/{f}', 'r') as f:
            try:
                data.append(json.loads(f.read()))
            except:
                pass

    publishers = []
    publisher_types = []
    content_types =  []
    publisher_names = []
    authors = []

    for d in data:
        pub = d.get('publisher', {'@type': None, 'name': None})
        publishers.append(pub)
        publisher_types.append(pub['@type'])
        publisher_names.append(pub['name'])
        content_types.append(d['@type'])
        authors.append(d.get('author', {}))

    author_names = []

    for x in authors:
        try:
            author_names.append(x[0]['name'])
        except KeyError:
            pass

    keyword_by_publisher = defaultdict(Counter)
    for d in data:
        pub = d.get('publisher')
        keywords = d.get('keywords', [])
        if pub is None:
           continue
        if isinstance(keywords, str):
            keywords = keywords.split(',')
        keyword_by_publisher[pub['name']].update(keywords)

    publisher_by_keyword = defaultdict(Counter)
    for d in data:
        pub = d.get('publisher')
        keywords = d.get('keywords', [])
        if pub is None:
           continue
        if isinstance(keywords, str):
            keywords = keywords.split(',')
        for keyword in keywords:
             publisher_by_keyword[keyword].update([pub['name']])

    sort_me = lambda x: sorted([y for y in x if y != None])
    counter_publishers = Counter(sort_me(publisher_names))
    counter_authors = Counter(sort_me(author_names))


    return render_template('./index.html',
        data=data,
        publishers=publishers,
        counter_publishers=counter_publishers,
        counter_authors=counter_authors,
        keyword_by_publisher=keyword_by_publisher,
        publisher_by_keywords=publisher_by_keyword,
    )
