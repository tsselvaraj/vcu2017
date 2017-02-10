# Please install requests, lxml, bs4 modules using pip install
import requests
from lxml import html
import collections
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import json

es = Elasticsearch()
es.indices.create(index='web', ignore=400)

STARTING_URL = 'http://www.cnn.com/'

urls_queue = collections.deque()
urls_queue.append(STARTING_URL)
found_urls = set()
found_urls.add(STARTING_URL)

data = {}


while len(urls_queue):
    url = urls_queue.popleft()

    response = requests.get(url)
    parsed_body = html.fromstring(response.content)

    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')
    print(url)
    print(soup.title.string)
    print(soup.get_text())

    data['url'] = url
    data['title'] = soup.title.string
    data['content'] = soup.get_text()
    json_data = json.dumps(data)

    es.index("web","webpage", json_data)

    # Find all links
    links = {urljoin(response.url, url) for url in parsed_body.xpath('//a/@href') if
             urljoin(response.url, url).startswith('http')}

    # Set difference to find new URLs
    for link in (links - found_urls):
        found_urls.add(link)
        urls_queue.append(link)
