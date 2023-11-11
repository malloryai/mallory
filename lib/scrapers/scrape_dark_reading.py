from bs4 import BeautifulSoup
from config.config import Config
from scrapingbee import ScrapingBeeClient
from lib.scrapers import ScrapeBase

class ScrapeDarkReading(ScrapeBase):
    
    RULE = r"darkreading\.com"

    @classmethod
    def scrape(cls, url):
        print("ScrapeDarkReadking scraping... ", url)
        
        soup = super().scrape_and_soup(url)

        content_div_tag = soup.find('div', class_='article-content')

        if content_div_tag is None:  # Check if the div was found
            raise Exception("Content not found or some error message here")
        
        content = content_div_tag.text
        out = super().clean_and_truncate_text(content)

        return out 
