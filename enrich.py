from google.cloud import pubsub_v1
from config.config import Config
import time
#import json

# import scrapers 
from bs4 import BeautifulSoup # for followon parsing 
from lib.scrapers import *

from lib.news_item import NewsItem
import threading  # Import threading for Semaphore

# Initialize subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(Config.PROJECT_ID, Config.SUB_NEWSITEM_INGEST)

# Semaphore to limit to 5 concurrent processes
semaphore = threading.Semaphore(5)

def callback(message):
    with semaphore:
        try:
            # load the message into a NewsItem object
            news_item = NewsItem.from_json(message.data.decode('utf-8'))

            if news_item.already_exists():
                print(f"Item already exists, removing from queue: {news_item.Title}")
                message.ack()
                return

            # okay good to scrape & save, it's new to us 
            content = scrape(news_item.url)

            # set content 
            news_item.Content = content

            # set summary
            news_item.Summary = content 
            if news_item.Summary == "":
                news_item.Summary = content[:200] + "..."

            #soup = BeautifulSoup(content, 'html.parser')
            #title = soup.find('title').text
            #news_item.Title = title

            news_item.persist()

            # and we're moving on... 
            print ("Publishing item to analysis queue: ", news_item.Title)
            out = news_item.publish(Config.TOPIC_NEWSITEM_ANALYZE)
            
            if out != None:
                print(f"Message successfully published to analysis queue with ID: {out.result()}" )
            else:
                print("Error publishing message!")
            
            # Don't forget to acknowledge the original message
            message.ack()

        except Exception as e:
            print(f"Error processing or publishing message: {str(e)}")
            # Optionally, you can nack the message so it can be redelivered
            message.nack()

def scrape(url):
    s = ScrapeFactory.get_scraper_for_url(url)
    return s.scrape(url)

def main():
    
    # Ensure local database is available for use 
    NewsItem.initialize_database()

    try:    
        print("Listening for messages...")
        # Use flow_control to ensure only 5 messages are processed at once
        subscriber.subscribe(subscription_path, callback=callback, flow_control=pubsub_v1.types.FlowControl(max_messages=Config.FLOW_CONTROL_MAX_ENRICH_MSGS))
    except Exception as e:
        print(f"Exception occurred while subscribing: {str(e)}")

    # Keep the process running
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
