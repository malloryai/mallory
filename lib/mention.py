
from google.cloud import pubsub_v1
from google.cloud import firestore

from pydantic import BaseModel, Field, root_validator
from typing import List
from datetime import datetime
import json
import hashlib

from config.config import Config

# Pydantic model for validation and operations
class Mention(BaseModel):
    url: str
    hashed_url: str = None
    source: str = None
    Snippet: str
    PublishedAt: datetime = None
    NewsItemId: str
    NewsAnalysisResultId: str
    


class Mention:
    def __init__(self, name):
        self.name = name

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
