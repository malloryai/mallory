from google.cloud import firestore

from typing import List
from pydantic import Field

# config 
from config.config import Config

from lib.news_analysis_result import NewsAnalysisResult
from lib.analyst.prompts import *

class DataBreachNewsAnalysisResult(NewsAnalysisResult):
    reporter: str = Field(description="name of the reporter of the breach")
    organization_name: str = Field(description="the name of the organization")
    organization_geographies: List[str] = Field(description="list of geographies associated with the organization")
    organization_verticals: List[str] = Field(description="list of verticals associated with the organization")
    breach_type: str = Field(description="the type of breach")
    data_impact: str = Field(description="the impact of the breach. what data was compromised?")
    actor_name: str = Field(description="the name of the actor or hacking group")
    actor_techniques: List[str] = Field(description="list of techniques used by the actor")

    def persist(self):
        db = firestore.Client(database=Config.MALLORY_DATABASE_NAME)

        print("Persisting as data_breach_news_analysis ", self.hashed_url)

        doc_ref = db.collection(u'data_breach_news_analysis').document(self.hashed_url)
        doc_ref.set({
            u'analysis_type': self.analysis_type,
            u'url': self.url,
            u'hashed_url': self.hashed_url,
            u'source': self.source,
            u'event_synopsis': self.event_synopsis,
            u'related_articles': self.related_articles,
            u'reporter': self.reporter,
            u'organization_name': self.organization_name,
            u'organization_geographies': self.organization_geographies,
            u'organization_verticals': self.organization_verticals,
            u'breach_type': self.breach_type,
            u'data_impact': self.data_impact,
            u'actor_name': self.actor_name,
            u'actor_techniques': self.actor_techniques
        })



class DataBreachNewsAnalyst: 
    
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

            QUESTIONS
            - What is the name of the organization experiencing the breach? Store this in "organization_name" field.
            - What is the geography of the organization experiencing the breach? Store this in "organization_geographies" field. 
            - What is the industry of the organization experiencing the breach? Store this in "organization_verticals" field. 
            - What type of data breach was this? Valid answers are: "hacked", "phishing","ransomware", "insider leak", "unintentional exposure", or "other". Store this in breach_type.
            - What data was compromised in this breach? Store this in "data_impact" field. 
            - Is the name of the attacking group known? If so, store this name in "actor_name".
            - What techniques were used by the attackers? Store this in "actor_techniques".

            {Prompts.append_prompt(content)}"""
            
        return prompt 
