import os
import json 
import time
import threading  # Import threading for Semaphore
from datetime import datetime 
from config.config import Config
from typing import List
from lib.news_item import NewsItem
from lib.analyst.analyst import Analyst 
from google.cloud import pubsub_v1

# Initialize subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(Config.PROJECT_ID, Config.SUB_NEWSITEM_ANALYZE)

# Semaphore to limit to 10 concurrent processes
semaphore = threading.Semaphore(5)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def process_news_item(news_item: NewsItem):
    analysis_list = []
    
    # First, add in our news item data 
    #analysis_list.append(news_item)

    print("Processing news item: ", news_item.hashed_url)

    # instanciate an analyst and preform our triage 
    analyst_instance = Analyst()
    news_triage_result = analyst_instance.triage_news_event(news_item)
    news_triage_result.persist()

    # append the initial analysis 
    analysis_list.append(news_triage_result)
    analysis = None

    if news_triage_result.data_breach_event:
        print("performing data breach analysis")        
        analysis = analyst_instance.analyze_data_breach_news_event(news_item)


    if news_triage_result.vulnerability_activity_event:
        print("performing vulnerability analysis")
        analysis = analyst_instance.analyze_vulnerability_news_event(news_item)

    if news_triage_result.malware_activity_event:
        print("performing malware analysis")
        analysis = analyst_instance.analyze_malware_news_event(news_item)

    if news_triage_result.threat_activity_event:
        print("Performing threat analysis")
        analysis = analyst_instance.analyze_threat_news_event(news_item)

    if news_triage_result.industry_funding_announcement_event:
        print("Performing industry funding announcement analysis")
        analysis = analyst_instance.analyze_industry_funding_announcement_news_event(news_item)

    if news_triage_result.patch_release_event:
        print("Performing patch release analysis")
        analysis = analyst_instance.analyze_patch_release_news_event(news_item)

    if news_triage_result.general_educational_event:
        print("Performing general education analysis")
        analysis = analyst_instance.analyze_general_education_news_event(news_item)
        
    # okay we have an analysis, let's publish it 
    if analysis:
        
        # persist 
        print ("Persisting item: ", analysis.hashed_url)
        analysis.persist()
        
        # publish to our results queue 
        print ("Publishing to result queue: ", analysis.hashed_url)
        out = analysis.publish(Config.TOPIC_NEWSANALYSISRESULT_INGEST)

        # and send it out 
        analysis_list.append(analysis)

    else:
        print("No analysis produced for ", news_item.hashed_url )
        


    # Export analysis results
    return [x.dict() for x in analysis_list if x is not None]


def callback(message):
    with semaphore: 
        #try:
        # load the message into a NewsItem object
        news_item = NewsItem.from_json(message.data.decode('utf-8'))
        
        analysis_dicts = process_news_item(news_item)

        for item in analysis_dicts:
            # create the analysis type directory if it doesnt exist 
            directory = f'tmp/{item["analysis_type"]}'
            os.makedirs(directory, exist_ok=True)

            # write the file 
            with open(f'{directory}/{news_item.hashed_url}.json', 'w') as file:
                file.write(json.dumps(item, cls=CustomJSONEncoder, indent=4))

        # only ack if we didnt get an exception
        message.ack()

        #except Exception as e:
        #    print(f"Error processing message: {str(e)}")
        #    
        #    # Optionally, you can nack the message so it can be redelivered
        #    message.nack()
        

def main():
    try:
        print("Listening for messages from analysis topic...")
        subscriber.subscribe(subscription_path, callback=callback, flow_control=pubsub_v1.types.FlowControl(max_messages=Config.FLOW_CONTROL_MAX_ANALYSIS_MSGS))
        #subscriber.close 
        #time.sleep(5)
    except Exception as e:
        print(f"Exception occurred while subscribing: {str(e)}")

    # Keep the process running
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
