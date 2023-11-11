import os
import argparse
import feedparser
import yaml

from typing import List
from datetime import datetime

from config.config import Config

from urllib.parse import urlparse

# Local application/library specific imports
from lib.news_item import NewsItem

# to grab raw data (will be properly scraped later)
import requests
from bs4 import BeautifulSoup

def consume_rss_feeds() -> List[NewsItem]:
    
    news_items = []
    
    current_path = os.path.join(os.path.dirname(__file__))
                                
    with open(current_path + '/data/feeds.yml', 'r') as file:

        feed_list = yaml.safe_load(file)
        
        for feed in feed_list:
    
            # description = feed['description']
            feed_url = feed['url']
            print ("feed: ", feed['url'])

            # Make a request to get the feed
            try:
                response = feedparser.parse(feed_url)
            except Exception as e:
                print(f"Error while parsing feed {feed_url}: {e}")
                continue
            
            # Get each item in the RSS feed
            items = response['items']
        
            for item in items:
                
                # Empty content for now, we'll do this during enrich
                content = ""

                # Create a NewsItem object with the url 
                try:
                    url = item['link']
                except KeyError:
                    url = "unknown"
                    continue
                
                try:
                    authors = item['authors']
                except KeyError:
                    authors = ["unknown"]
                    continue
                
                try:
                    title = item['title']
                except KeyError:
                    title = "unknown"
                    continue
                
                try:
                    summary = item['summary']
                except KeyError:
                    summary = "unknown"
                    continue
                
                try:
                    published_at = item['published']
                    published_at = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    published_at = datetime.now().isoformat()


                news_item = NewsItem(url=url, Authors=authors, Title=title, Content=content, Summary=summary, PublishedAt=published_at)
                #print("Got news item", news_item)
                news_items.append(news_item)

    return news_items

### ARG PARSING 

# Create the parser
arg_parser = argparse.ArgumentParser(description="feed the beast")

# Add the arguments
arg_parser.add_argument('-i', '--input', choices=['single', 'rss'], required=True, help="Input method")
arg_parser.add_argument('-u', '--url', help="url to scrape")

# Parse the arguments
args = arg_parser.parse_args()

# Validate the arguments
# SINGLE MODE 
if args.input == 'single' and not args.url:
    arg_parser.error("the --url parameter is required with 'single' input method")
elif args.input == 'single' and args.url:
    try:
        result = urlparse(args.url)
        if not all([result.scheme, result.netloc]):
            arg_parser.error("the --url parameter must be a well formed url with 'single' input method")
    except ValueError:
        arg_parser.error("the --url parameter must be a well formed url with 'scrape' input method")

###
### Input Handling
###

# Create an array of NewsItem that we will feed to our initial analysis engine 
newsItems = []

if args.input == 'rss':
   
    # Call the function to consume RSS feeds and convert them into NewsItem objects
    newsItems = consume_rss_feeds()

elif args.input == 'single':
    
    # Extract necessary details from the response
    url = args.url
    authors = [{"name": "Author1"}, {"name": "Author2"}]
    publishedAt = datetime.now().isoformat()  # Placeholder

    # add a single News Item in 
    item = NewsItem(
            url=url, 
            Authors=authors, 
            Title="",   # TODO ... gets disregarded now that we pull only content
            Summary="", # filled during enrich
            Content="", # filled during enrich
            PublishedAt=publishedAt)

    newsItems = [item]

for item in newsItems:
    
    # publish to the queue'
    print("Publishing ", item.Title )

    # publish the item and wait for it to complete 
    future = item.publish(Config.TOPIC_NEWSITEM_INGEST)
    future.result()
