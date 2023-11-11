# config.py
import os

class Config:

    # KEYS!!! 
    MALLORY_SCRAPING_BEE_KEY = os.environ['MALLORY_SCRAPING_BEE_KEY']  # Get the API key from the environment variable
    #MALLORY_OPENAI_API_KEY = os.environ['MALLORY_OPENAI_API_KEY']  # NOTE! for now this just uses OPENAI_API_KEY

    # SCRAPING CONFIG
    MAX_SCRAPE_CONTENT_LENGTH = 24000

    # INFRA !!!
    PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'mallory-dev')
    
    # dB 
    MALLORY_DATABASE_NAME = "mallory-dev"

    # Queues 
    TOPIC_NEWSITEM_INGEST = "NewsItem-Ingest"
    SUB_NEWSITEM_INGEST = "NewsItem-Ingest-sub"

    TOPIC_NEWSITEM_ANALYZE = "NewsItem-Analysis"
    SUB_NEWSITEM_ANALYZE = "NewsItem-Analysis-sub"

    TOPIC_NEWSANALYSISRESULT_INGEST = "NewsAnalysisResult-Ingest"
    SUB_NEWSANALYSISRESULT_INGEST = "NewsAnalysisResult-Ingest-sub"
    
    # Managing flow between pub/sub queues. crank these up as needed 
    FLOW_CONTROL_MAX_ANALYSIS_MSGS = 3
    FLOW_CONTROL_MAX_ENRICH_MSGS = 3