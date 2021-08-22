# Please install requests, lxml, bleach modules using pip install

import collections
from urllib.parse import urljoin

import requests
from lxml import html
import bleach

#from bs4 import BeautifulSoup
#from textblob import TextBlob

STARTING_URL = 'https://www.cnn.com/'

urls_queue = collections.deque()
urls_queue.append(STARTING_URL)
found_urls = set()
found_urls.add(STARTING_URL)

while len(urls_queue):
    url = urls_queue.popleft()

    response = requests.get(url)
    parsed_body = html.fromstring(response.content)
    # print(parsed_body)
    html_content = response.text
    text_only = bleach.clean(html_content, strip=True)
    print(text_only)
    #soup = BeautifulSoup(html_content, 'lxml')
    #soup2 = soup.text
    # print(html2text.html2text(soup2))
    #try:
    #    print(url)
    #    print(soup.title.string)
    #    print(soup.body.text)
    #except:
    #    pass
    #blob = TextBlob(soup2)
    #print(blob)

    # Find all links
    links = {urljoin(response.url, url) for url in parsed_body.xpath('//a/@href') if
             urljoin(response.url, url).startswith('http')}

    # Set difference to find new URLs
    for link in (links - found_urls):
        found_urls.add(link)
        urls_queue.append(link)
