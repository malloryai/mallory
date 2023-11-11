import re
from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient
from config.config import Config
from lib.scrapers import ScrapeBase

class ScrapeTHN(ScrapeBase):
    
    RULE = r"thehackernews\.com"

    @classmethod
    def scrape(cls, url):
        print("ScrapeTHN Scraping... ", url)
        
        soup = super().scrape_and_soup(url)

        # only grab the body 
        content_div_tag = soup.find('div', id='articlebody')
        if content_div_tag is None:  # Check if the div was found
            raise Exception("Content not found or some error message here")
        
        content = content_div_tag.text

        # remove cruft 
        content = re.sub(r'Found this article interesting.*$', '', content, flags=re.DOTALL)

        out = super().clean_and_truncate_text(content)

        return out 
