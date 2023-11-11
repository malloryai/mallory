from google.cloud import firestore

from typing import List
from pydantic import Field

# config 
from config.config import Config

from lib.news_analysis_result import NewsAnalysisResult
from lib.analyst.prompts import *

class IndustryFundingAnnouncementNewsAnalysisResult(NewsAnalysisResult):
    funded_company: str = Field(description="the company receiving funding")
    funded_amount: str = Field(description="the amount of funding received")
    funding_round: str = Field(description="the round of funding")
    total_funding_to_date: str = Field(description="the total amount of funding received to date")
    backers: List[str] = Field(description="the entities providing funding")
   
    def persist(self):
        db = firestore.Client(database=Config.MALLORY_DATABASE_NAME)
        print("Persisting as industry_funding_announcement_news_analysis ", self.hashed_url)
        doc_ref = db.collection(u'industry_funding_announcement_news_analysis').document(self.hashed_url)
        doc_ref.set({
            u'analysis_type': self.analysis_type,
            u'url': self.url,
            u'hashed_url': self.hashed_url,
            u'source': self.source,
            u'event_synopsis': self.event_synopsis,
            u'related_articles': self.related_articles,
            u'funded_company': self.funded_company,
            u'funded_amount': self.funded_amount,
            u'funding_round': self.funding_round,
            u'total_funding_to_date': self.total_funding_to_date,
            u'backers': self.backers
        })


class IndustryFundingAnnoucementNewsAnalyst:
    @staticmethod
    def generate_prompt(url: str, content: str) -> str:
        text = f"""{Prompts.prepend_prompt(url)}
         
            ACTIONS
             - Ignore the analysis_type, url, hashed_url and source fields. 
             - Store any referenced links in the related_articles field in the JSON output.
             - Perform a summary of the content and store it in the output event_synopsys field in the JSON output. The value should be a paragraph. no more than 5 sentences.
             - Return false for any boolean field you don't have an answer for. 
             - Return "" for any string field you don't have an answer for. 
             - Return [] for any list field you don't have an answer for. 

            QUESTIONS
             - Who is recieving funding? 
             - How much is the funding?
             - What round is this? 
             - How much funding has been received to date?
             - Who is providing funding?
             
   

            {Prompts.append_prompt(content)}"""
            
        return text 