
from google.cloud import firestore

from typing import List
from pydantic import Field

# config 
from config.config import Config

from lib.news_analysis_result import NewsAnalysisResult
from lib.analyst.prompts import *

class TriageNewsAnalysisResult(NewsAnalysisResult):
    # our own fields 
    law_enforcement_event: bool = Field(description="whether this article discusses a law enforcement agency performing an action against a cyber threat")
    data_breach_event: bool = Field(description="whether this article discusses a data breach event against a specific organization")
    threat_activity_event: bool = Field(description="whether this article discusses a named threat attacker or hacker group performing some action")
    #technique_analysis_event: bool = Field(description="whether this article teaches a new security finding, attacker technique, or vulnerability")
    malware_activity_event: bool = Field(description="whether this article describes a piece of software used by a threat actor in the wild")
    vulnerability_activity_event: bool = Field(description="whether this article describes a software vulnerability, or CVE. ")
    industry_funding_announcement_event: bool = Field(description="whether this article discusses a venture funding event for a cybersecurity product or services company")
    general_educational_event: bool = Field(description="whether this article discussed a general cybersecurity concept")
    patch_release_event: bool = Field(description="whether this article describes new patches being released by a vendor")

    def persist(self):
        db = firestore.Client(database=Config.MALLORY_DATABASE_NAME)
        print("Persisting as triage_analysis ", self.hashed_url)
        doc_ref = db.collection(u'triage_analysis').document(self.hashed_url)
        doc_ref.set({
            u'analysis_type': self.analysis_type,
            u'url': self.url,
            u'hashed_url': self.hashed_url,
            u'source': self.source,
            u'event_synopsis': self.event_synopsis,
            u'related_articles': self.related_articles,
            u'law_enforcement_event': self.law_enforcement_event,
            u'data_breach_event': self.data_breach_event,
            u'threat_activity_event': self.threat_activity_event,
            #u'technique_analysis_event': self.technique_analysis_event,
            u'malware_activity_event': self.malware_activity_event,
            u'vulnerability_activity_event': self.vulnerability_activity_event,
            u'general_educational_event': self.general_educational_event,
            u'industry_funding_announcement_event': self.industry_funding_announcement_event,
            u'patch_release_event': self.patch_release_event

        })



             
class TriageNewsAnalyst: 

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
            - Does this article discuss a  law enforcement action where an agency is working to take down malicious activity? Store the answer in law_enforcement_event field as a true or false.
            - Does this article discuss an organization's Data Breach? Store the answer in data_breach_event field as a true or false.
            - Does this article discuss an attacker or hacker performing some action against a target organization in the wild? Store the answer in threat_activity_event field as a true or false.
            - Does this article discuss the analysis of a piece of malware? Store the answer in malware_analysis_event field as a true or false.
            - Does this article discuss a vulnerability or CVE? Store the answer in vulnerability_analysis field as a true or false.
            - Does this article discuss a general cybersecurity concept? Store the answer in general_educational_analysis field as a true or false.
            - Does this article discuss a venture funding event for a cybersecurity company?? Store the answer in industry_funding_announcement_event field as a true or false.
            - Does this article discuss a new set of patches being released by a vendor? Store the answer in patch_release_event field as a true or false.
            
            {Prompts.append_prompt(content)}"""
        
        return text 

