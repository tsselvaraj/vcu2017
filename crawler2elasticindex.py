import requests
from lxml import html
import collections
from urllib.parse import urljoin
import bleach
from elasticsearch import Elasticsearch
import json

es = Elasticsearch()
#es.indices.create(index='web')

STARTING_URL = 'https://www.vcu.edu/'

urls_queue = collections.deque()
urls_queue.append(STARTING_URL)
found_urls = set()
found_urls.add(STARTING_URL)

data = {}

urlcount = 1

while len(urls_queue):

    url = urls_queue.popleft()

    response = requests.get(url)
    parsed_body = html.fromstring(response.content)

    html_content = response.text
    text_only = bleach.clean(html_content, strip=True, strip_comments=True)
    print(url)

    data['url'] = url
    data['content'] = text_only
    json_data = json.dumps(data)

    #es.index("web","webpage", body=json_data, id=urlcount)
    es.index("web", body=json_data, id=urlcount)

    urlcount = urlcount+1

    # Find all links
    links = {urljoin(response.url, url) for url in parsed_body.xpath('//a/@href') if
             urljoin(response.url, url).startswith('http')}

    # Set difference to find new URLs
    for link in (links - found_urls):
        found_urls.add(link)
        urls_queue.append(link)
