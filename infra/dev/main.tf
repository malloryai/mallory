provider "google-beta" {
  project = "mallory-dev"
  region  = "us-central1"
}


### NewsItem Ingest Pub/Sub

resource "google_pubsub_topic" "newsitem_ingest" {
  project = "mallory-dev"
  name = "NewsItem-Ingest"
}

resource "google_pubsub_subscription" "newsitem_ingest_sub" {
  project = "mallory-dev"
  name  = "NewsItem-Ingest-sub"
  topic = google_pubsub_topic.newsitem_ingest.name
}

### NewsItem Analysis Pub/Sub

resource "google_pubsub_topic" "newsitem_analysis" {
  project = "mallory-dev"
  name = "NewsItem-Analysis"
}

resource "google_pubsub_subscription" "newsitem_analysis_sub" {
  project = "mallory-dev"
  name  = "NewsItem-Analysis-sub"
  topic = google_pubsub_topic.newsitem_analysis.name
}

### NewsItem Analysis Pub/Sub

resource "google_pubsub_topic" "newsanalysisresult_ingest" {
  project = "mallory-dev"
  name = "NewsAnalysisResult-Ingest"
}


resource "google_pubsub_subscription" "newsitem_analysis_sub" {
  project = "mallory-dev"
  name  = "NewsAnalysisResult-Ingest-sub"
  topic = google_pubsub_topic.newsitem_analysis.name
}


###
## DB
###

resource "google_project_service" "firestore" {
  project = "mallory-dev"
  service = "firestore.googleapis.com"
}



resource "google_firestore_database" "mallory-test" {
  project     = "mallory-dev"
  name        = "mallory-test" # Replace with your desired database name
 location_id  = "us-west1" # Replace with your desired location
  type        = "FIRESTORE_NATIVE"

  depends_on = [google_project_service.firestore]
}
