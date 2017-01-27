# Please install html2text, requests, textblob modules using pip install

from textblob import TextBlob
import requests
import html2text

page = requests.get("http://www.cnn.com")

blob = TextBlob(html2text.html2text(page.text))
print(blob)
print(blob.tags)

print(blob.noun_phrases)

for sentence in blob.sentences:
    print(sentence)
    print(sentence.sentiment.polarity)
