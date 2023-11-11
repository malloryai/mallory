from google.cloud import firestore

from typing import List
from pydantic import Field

# config 
from config.config import Config

from lib.news_analysis_result import NewsAnalysisResult
from lib.analyst.prompts import *

class GeneralEducationNewsAnalysisResult(NewsAnalysisResult):

    def persist(self):
        db = firestore.Client(database=Config.MALLORY_DATABASE_NAME)

        print("Persisting as general_education_news_analysis ", self.hashed_url)

        doc_ref = db.collection(u'general_education_news_analysis').document(self.hashed_url)
        doc_ref.set({
            u'analysis_type': self.analysis_type,
            u'url': self.url,
            u'hashed_url': self.hashed_url,
            u'source': self.source,
            u'event_synopsis': self.event_synopsis,
            u'related_articles': self.related_articles,
        })



class GeneralEducationNewsAnalyst: 
    
    @staticmethod
    def generate_prompt(url: str, content: str) -> str:
        prompt = f"""{Prompts.prepend_prompt(url)}                    
            
            ACTIONS
             - Ignore the analysis_type, url, hashed_url and source fields. 
             - Store any referenced links in the referenced_articles field in the JSON output.
             - Perform a summary of the content and store it in the output event_synopsys field in the JSON output. The value should be a paragraph. no more than 5 sentences.
             - Return false for any boolean field you don't have an answer for. 
             - Return "" for any string field you don't have an answer for. 
             - Return [] for any list field you don't have an answer for. 


            {Prompts.append_prompt(content)}"""
            
        return prompt 

    