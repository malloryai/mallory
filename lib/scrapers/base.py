from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient

from config.config import Config

import re

class ScrapeFactory:
    registry = {}  # Map of rule to class
    
    @classmethod
    def register(cls, pattern, class_ref):
        print(f"{class_ref} registering {pattern}")
        if pattern in cls.registry:
            print(f"Pattern {pattern} already registered: {cls}")
        cls.registry[pattern] = class_ref
    
    @classmethod
    def get_scraper_for_url(cls, url):
        from lib.scrapers import ScrapeGeneric
        for pattern, class_ref in cls.registry.items():
            if re.search(pattern, url):
                return class_ref
        return ScrapeGeneric # deafult    

class ScrapeMeta(type):
    """Metaclass for ScrapeBase"""
    def __init__(cls, name, bases, attrs):
        # If it's a subclass of ScrapeBase and has a RULE attribute, register it
        if "RULE" in attrs and name != 'ScrapeBase' and name != 'ScrapeGeneric':
            ScrapeFactory.register(attrs["RULE"], cls)
        super().__init__(name, bases, attrs)


class ScrapeBase(metaclass=ScrapeMeta):
    RULE = None  # Should be overridden by subclasses
    def __init__(self, name):
        self.name = name

    def scrape_and_soup(url):
        sb_client = ScrapingBeeClient(api_key=Config.MALLORY_SCRAPING_BEE_KEY)
        response = sb_client.get(url)
        return BeautifulSoup(response.content, "lxml")
        

    def clean_and_truncate_text(text):
        cleansed_text = text.replace('\n', '')

        # see: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
        # 1 token ~= 4 chars in English
        # 1 token ~= ¾ words
        # 100 tokens ~= 75 words
        out = cleansed_text[:Config.MAX_SCRAPE_CONTENT_LENGTH]
        
        return out