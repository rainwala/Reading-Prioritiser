import argparse
import chromadb
import feedparser
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import sys

parser = argparse.ArgumentParser(description="Query a persistent index of PDF files")
parser.add_argument("rss_file_path", help="Path to the RSS file")
parser.add_argument("index_path", help="Path where the index is stored")
parser.add_argument("collection_name", help="Name of the collection to query")
args = parser.parse_args()

# Parse the RSS feed
feed = feedparser.parse(args.rss_file_path)


client = chromadb.PersistentClient(path=args.index_path)
collection = client.get_collection(name=args.collection_name)

for entry in feed.entries:
    if 'link' in entry:
        url = entry.link
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        results = collection.query(
            query_texts=text, 
            n_results=1 
        )
        if results['distances'][0][0] < 0.9:
            print(url, results['distances'][0][0])


