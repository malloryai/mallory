
from google.cloud import firestore

from typing import List
from pydantic import Field

# config 
from config.config import Config

from lib.news_analysis_result import NewsAnalysisResult
from lib.analyst.prompts import *

class PatchNewsAnalysisResult(NewsAnalysisResult):
    cve_ids: List[str] = Field(description="list of Common Vulnerabilities and Exposures (CVE) IDs associated with the event")
    vendor: List[str] = Field(description="the software vendor releasing patches")
    products: List[str] = Field(description="the software products are being patched")
    exploited: bool = Field(description="are the patches being released due to exploitation in the wild")

    def persist(self):
        db = firestore.Client(database=Config.MALLORY_DATABASE_NAME)
        print("Persisting as patch_news_analysis", self.hashed_url)
        doc_ref = db.collection(u'patch_news_analysis').document(self.hashed_url)
        doc_ref.set({
            u'analysis_type': self.analysis_type,
            u'url': self.url,
            u'hashed_url': self.hashed_url,
            u'source': self.source,
            u'event_synopsis': self.event_synopsis,
            u'related_articles': self.related_articles,
            u'vendor': self.vendor,
            u'products': self.products,
            u'exploited': self.exploited,
        })


class PatchNewsAnalyst:
    @staticmethod
    def generate_prompt(url: str, content: str) -> str:
        prompt = f"""{Prompts.prepend_prompt(url)}

            ACTIONS
             - Ignore the analysis_type, url, hashed_url and source fields. 
             - Store any referenced links in the related_articles field in the JSON output.
             - Perform a summary of the content and store it in the output event_synopsys field in the JSON output. The value should be a paragraph. no more than 5 sentences.
             - Return false for any boolean field you don't have an answer for. 
             - Return "" for any string field you don't have an answer for. 
             - Return [] for any list field you don't have an answer for. 

            QUESTIONS
             - Which vendor is releasing patches? Name the specific vendor in the 'vendor' field. 
             - Which products are being patched? Name the specific products in the 'products' field. 
             - Were any of the products exploited in the wild, causing the patches to be released? 
             
            {Prompts.append_prompt(content)}"""
        
        return prompt 