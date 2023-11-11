from google.cloud import firestore

from typing import List
from pydantic import Field

# config 
from config.config import Config

from lib.news_analysis_result import NewsAnalysisResult
from lib.analyst.prompts import *

class ThreatNewsAnalysisResult(NewsAnalysisResult):
    reporter: str = Field(description="Name of the group that identified the threat activity")
    reporter_justify: str = Field(description="justification for the reporter field")
    
    threat_human_names: List[str] = Field(description="List of people associated with a threat actor")
    threat_human_names_justify: str = Field(description="justification for the threat_human_names field")
    
    threat_group_names: List[str] = Field(description="List of threat actor groups or hacking groups")
    threat_group_names_justify: str = Field(description="justification for the threat_group_names field")
    
    techniques: List[str] = Field(description="List any unique techniques or identifiable patterns of cyber activity.")
    techniques_justify: str = Field(description="justification for the techniques field")
    
    collaboration: List[str] = Field(description="List any known partner groups for this threat. Is this threat a collaboration between threat actors - if so, which actors?")
    collaboration_justify: str = Field(description="justification for the collaboration field")

    source_geographies: List[str] = Field(description="list of geographies associated with the event source")
    source_geographies_justify: str = Field(description="justification for the source_geographies field")

    target_organization_names: List[str] = Field(description="list of names associated with the target organization(s)")
    target_organization_names_justify: str = Field(description="justification for the target_organization_names field")

    target_organization_geographies: List[str] = Field(description="list of geographies associated with the target organization(s)")
    target_organization_geographies_justify: str = Field(description="justification for the target_organization_geographies field")

    target_organization_industries: List[str] = Field(description="list of industries associated with the target organization(s)")
    target_organization_industries_justify: str = Field(description="justification for the target_organization_industries field")

    target_software: List[str] = Field(description="list of software that is being targeted. include vendor, product name, and version if available.")    
    target_software_justify: str = Field(description="justification for the target_software field")

    def persist(self):
        db = firestore.Client(database=Config.MALLORY_DATABASE_NAME)
        print("Persisting as threat_news_analysis ", self.hashed_url)
        doc_ref = db.collection(u'threat_news_analysis').document(self.hashed_url)
        doc_ref.set({
            u'analysis_type': self.analysis_type,
            u'url': self.url,
            u'hashed_url': self.hashed_url,
            u'source': self.source,
            u'event_synopsis': self.event_synopsis,
            u'related_articles': self.related_articles,
            u'reporter': self.reporter,
            u'reporter_justify': self.reporter_justify,
            u'threat_human_names': self.threat_human_names,
            u'threat_human_names_justify': self.threat_human_names_justify,
            u'threat_group_names': self.threat_group_names,
            u'threat_group_names_justify': self.threat_group_names_justify,
            u'techniques': self.techniques,
            u'techniques_justify': self.techniques_justify,
            u'collaboration': self.collaboration,
            u'collaboration_justify': self.collaboration_justify,
            u'source_geographies': self.source_geographies,
            u'source_geographies_justify': self.source_geographies_justify,
            u'target_organization_names': self.target_organization_names,
            u'target_organization_names_justify': self.target_organization_names_justify,
            u'target_organization_geographies': self.target_organization_geographies,
            u'target_organization_geographies_justify': self.target_organization_geographies_justify,
            u'target_organization_industries': self.target_organization_industries,
            u'target_organization_industries_justify': self.target_organization_industries_justify,
            u'target_software': self.target_software,
            u'target_software_justify': self.target_software_justify
        })

class ThreatNewsAnalyst:

    @staticmethod
    def generate_prompt(url: str, content: str) -> str:
        prompt = f"""{Prompts.prepend_prompt(url)}
                            
            ACTIONS
             - Ignore the analysis_type, url, hashed_url and source fields. 
             - Store any referenced links in the related_articles field in the JSON output.
             - Perform a summary of the content and store it in the output event_synopsys field in the JSON output. The value should be a paragraph. no more than 5 sentences.
             - Identify any persons named in the article as part of a threat group(s), and store in threat_human_names. Add justification in the threat_human_names_justify field.
             - Identify threat actor names in the content, and store in threat_group_names. Include all aliases mentioned. Add justification in the threat_group_names_justify field..
             - Summarize the techniques used by the actor in techniques field. Specifically list unique & identifiable techniques. Add justification in the techniques_justify field. 
             - List in source_geographies the geographies, countries, or locations where the threat actor group members are located. Do not include extradition-only countries. Add justification in the source_geographies_justify field. 
             - List the discussed target organization geographies. Store this in target_organication_geographies. Add justification in the target_organication_geographies_justify field. 
             - List the discussed target organization industry. Store this in target_organization_industries. Add justification in the target_organization_industries_justify field. 
             - List the discussed target organization name. Store this in target_organization_names. Add justification in the target_organization_names_justify  field. 
             - List the person or organizations that identified any malicious activity. Store this in the 'reporter' field. Add justification in the reporter_justify field. 
             - List software that is being targeted. include vendor, product name, and version in the target_software field. Add justification in the target_software_justify field. 
             - List any known partners for this threat. Is this threat a collaboration between threat actors - if so, which actors? Store in collaboration field.  Add justification in the collaboration_justify field. 
             - Return false for any boolean field you don't have an answer for. 
             - Return "" for any string field you don't have an answer for. 
             - Return [] for any list field you don't have an answer for. 
             


            {Prompts.append_prompt(content)}"""
            
        return prompt
    


   ### 
   ###