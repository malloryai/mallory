from google.cloud import pubsub_v1

from pydantic import BaseModel, Field, root_validator
from typing import List

from urllib.parse import urlparse
import hashlib

import json

from config.config import Config

#from lib.news_item import NewsItem

class NewsAnalysisResult(BaseModel):
    analysis_type: str = None 
    url: str =  None
    hashed_url: str = None
    source: str = None
    event_synopsis: str = Field(description="a brief overview of the event data")
    related_articles: List[str] = Field(description="relevant related links that are referenced in the article")


    def calculate_hash_values(self):
        hashed_url = hashlib.sha256(self.url.encode()).hexdigest()
        self.hashed_url = hashed_url

        d = urlparse(self.url).netloc
        self.source = d

        return True 
    
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