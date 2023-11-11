from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient
from config.config import Config
from lib.scrapers import ScrapeBase

class ScrapeBleepingComputer(ScrapeBase):
    
    RULE = r"bleepingcomputer\.com"

    @classmethod
    def scrape(cls, url):
        print("ScrapeBleepingComputer scraping... ", url)
        
        soup = super().scrape_and_soup(url)

        content_div_tag = soup.find('div', class_='articleBody')

        if content_div_tag is None:  # Check if the div was found
            raise Exception("Content not found or some error message here")
        
        content = content_div_tag.text
        out = super().clean_and_truncate_text(content)

        return out 
