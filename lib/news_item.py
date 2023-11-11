from google.cloud import pubsub_v1
from google.cloud import firestore

from pydantic import BaseModel, Field, root_validator
from typing import List
from datetime import datetime
import json
import hashlib

from config.config import Config

# Pydantic model for validation and operations
class NewsItem(BaseModel):
    url: str
    Content: str
    PublishedAt: datetime = None
    Authors: List[dict] = None
    Title: str = None
    Summary: str = None
    hashed_url: str = None
    source: str = None

    @root_validator(pre=True)
    def compute_hashed_url(cls, values):
        url = values.get('url')
        hashed_url = hashlib.sha256(url.encode()).hexdigest()
        values["hashed_url"] = hashed_url
        return values

    @root_validator(pre=True)
    def compute_url_domain(cls, values):
        url = values.get('url')
        from urllib.parse import urlparse
        domains = urlparse(url).netloc
        values["source"] = domains
        return values

    def persist(self):
        db = firestore.Client(database=Config.MALLORY_DATABASE_NAME)
        doc_ref = db.collection(u'news_items').document(self.hashed_url)
        doc_ref.set({
            u'url': self.url,
            u'hashed_url': self.hashed_url,
            u'source': self.source,
            u'Content': self.Content,
            u'PublishedAt': self.PublishedAt,
            u'Authors': self.Authors,
            u'Title': self.Title,
            u'Summary': self.Summary
        })


    # Assuming the ready_for_analysis method checks if the news item meets certain conditions for analysis
    def already_exists(self):
        return self.exists(self.hashed_url)
    
    def publish(self, topic_id):
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(Config.PROJECT_ID, topic_id)
        data = self.to_json().encode("utf-8")

        try:
            return publisher.publish(topic_path, data)
        
        except Exception as e:
            print(f"Error publishing message: {str(e)}")
            return None

    def to_json(self):
        item = json.dumps(self.dict(), default=str) 

        if self.hashed_url is None:
            self.hashed_url = hash(self.url)
        
        return item 

    @classmethod
    def consume(cls, callback, subscription_id):
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(Config.PROJECT_ID, subscription_id)

        def wrapper(message):
            news_item = cls.from_json(message.data.decode('utf-8'))
            callback(news_item)
            message.ack()

        subscriber.subscribe(subscription_path, callback=wrapper)

    @classmethod
    def exists(cls, hash):
        db = firestore.Client(Config.MALLORY_DATABASE_NAME)
        doc_ref = db.collection(u'news_items').document(hash)
        doc = doc_ref.get()
        return doc.exists
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        data['PublishedAt'] = datetime.fromisoformat(data['PublishedAt']) if data['PublishedAt'] else None
        return cls(**data)

    # Does what it says on the tin
    @classmethod
    def initialize_database(cls): 
        print("Now using firestore!")
        
        