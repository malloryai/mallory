## About 

Mallory uses machine intelligence to turn cyber threat intel, gathered primarily via OSINT, into a knowledge graph - establishing a foundation for further analysis and better understanding of the current threat landscape. 

Mallory is written in python and designed to be run in a cloud environment atop GCP, utilizing OpenAI APIs for analysis. Extending to other cloud providers, LLMs, and other APIs is left to the reader.  

Mallory is open source software, available under the MIT license.

## Configuring Mallory

### Infra setup & configuraiton

Mallory operates on GCP pub/sub for message passing, and thus, you must have a GCP account & project configured in order to use it. Use the `gcloud` binary to configure your account and project. 

Then, in dev, ensure you have configured application-default auth: `gcloud auth application-default login`

Set up the necessary infrastructure using terraform init, terraform apply in the infra/dev folder.  

### API setup & configuration 

Mallory relies on several external APIs, so you'll need to setup and configured keys for the following: 
 * ScrapingBee API (For chrome-headless scraping)
 * OpenAI API (for access to gpt-3.5 model)

Configure those keys in your profile with: 
`export OPENAI_API_KEY=[KEY]`
`export MALLORY_SCRAPING_BEE_KEY=[KEY]`

### Additional Configuration 

All scraped RSS feeds are defined in data/feeds.yml

Additional config can be found in the config/config.py file, including topic and subscription names, flow control, and other fun stuff. 

## Running Mallory

Mallory is intended to run with many processes operating in parallel, passing messages between processes using pub/sub. Specifically

* (Beta) Collect RSS feeds (described in data/feeds.yml) & creating NewsItems (collect.py)
* (Beta) Scrape Raw Content & Enriching NewsItems (enrich.py)
* (Beta) Analyze NewsItems & Crafting NewsAnalysisResults JSON (analyze.py)
* (Alpha) Publish content to slack using (publish.py) < not yet well thought through
* (Future) EventDB publisher - pushes to an event db for historical event record
* (Future) GraphDB publisher - parses JSON and pushes to a graph database (schema has not yet been defined)
* (Future) GraphDB analyst - reviews recent additions to the graph and creates/adjusts/removes connections accordingly
* (Future) Daily Digest analyst - reviews recent additions and crafts narrative of new / interesting connections

## Questions / Comments / Concerns? 

Reach out via mallory@mallory.ai 