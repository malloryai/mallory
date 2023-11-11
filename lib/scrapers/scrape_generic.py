from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient

from config.config import Config
from lib.scrapers import ScrapeBase

class ScrapeGeneric(ScrapeBase):
    #RULE = None  # no rule required, this is a default class 

    @classmethod
    def scrape(cls, url):
        print("ScrapeGeneric Scraping... ", url)
        
        soup = super().scrape_and_soup(url)
        
        content = soup.text
        out = super().clean_and_truncate_text(content)

        return out 


