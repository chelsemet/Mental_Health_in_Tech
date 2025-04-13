provider "google" {
  project = var.project
  region  = var.region
}

# Create BigQuery dataset
resource "google_bigquery_dataset" "mental_health_dataset" {
  dataset_id                  = var.mental_health_dataset
  friendly_name               = "Mental Health Survey Data"
  description                 = "Dataset for analyzing mental health in tech"
  location                    = var.region

  # Set access permissions
  access {
    role          = "OWNER"
    special_group = "projectOwners"
  }
  
  access {
    role          = "READER"
    special_group = "projectReaders"
  }
  
  access {
    role          = "WRITER"
    special_group = "projectWriters"
  }
}

# Create the table with proper partitioning and clustering
resource "google_bigquery_table" "survey_table" {
  dataset_id = google_bigquery_dataset.mental_health_dataset.dataset_id
  table_id   = "clean_data"

  range_partitioning {
    field = "Age"
    range {
      start    = 0
      end      = 100
      interval = 10
    }
  }
  
  clustering = ["Country", "tech_company", "gender_clean"]
  
  schema = <<EOF
  [
    {"name": "Age", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "Country", "type": "STRING", "mode": "NULLABLE"},
    {"name": "self_employed", "type": "STRING", "mode": "NULLABLE"},
    {"name": "family_history", "type": "STRING", "mode": "NULLABLE"},
    {"name": "treatment", "type": "STRING", "mode": "NULLABLE"},
    {"name": "work_interfere", "type": "STRING", "mode": "NULLABLE"},
    {"name": "no_employees", "type": "STRING", "mode": "NULLABLE"},
    {"name": "remote_work", "type": "STRING", "mode": "NULLABLE"},
    {"name": "tech_company", "type": "STRING", "mode": "NULLABLE"},
    {"name": "benefits", "type": "STRING", "mode": "NULLABLE"},
    {"name": "care_options", "type": "STRING", "mode": "NULLABLE"},
    {"name": "wellness_program", "type": "STRING", "mode": "NULLABLE"},
    {"name": "seek_help", "type": "STRING", "mode": "NULLABLE"},
    {"name": "anonymity", "type": "STRING", "mode": "NULLABLE"},
    {"name": "leave", "type": "STRING", "mode": "NULLABLE"},
    {"name": "mental_health_consequence", "type": "STRING", "mode": "NULLABLE"},
    {"name": "phys_health_consequence", "type": "STRING", "mode": "NULLABLE"},
    {"name": "coworkers", "type": "STRING", "mode": "NULLABLE"},
    {"name": "supervisor", "type": "STRING", "mode": "NULLABLE"},
    {"name": "mental_health_interview", "type": "STRING", "mode": "NULLABLE"},
    {"name": "phys_health_interview", "type": "STRING", "mode": "NULLABLE"},
    {"name": "mental_vs_physical", "type": "STRING", "mode": "NULLABLE"},
    {"name": "obs_consequence", "type": "STRING", "mode": "NULLABLE"},
    {"name": "gender_clean", "type": "STRING", "mode": "NULLABLE"},
    {"name": "age_range", "type": "STRING", "mode": "NULLABLE"}
  ]
  EOF

  deletion_protection = false

}

resource "google_bigquery_table" "correlation" {
  dataset_id = google_bigquery_dataset.mental_health_dataset.dataset_id
  table_id   = "correlation"
  
  deletion_protection = false
}

resource "google_bigquery_table" "pca_result" {
  dataset_id = google_bigquery_dataset.mental_health_dataset.dataset_id
  table_id   = "pca_result"
  
  deletion_protection = false
}

# Set up storage bucket for data
resource "google_storage_bucket" "data_bucket" {
  name          = "mental-health-data-${var.project}"
  location      = "US"
  force_destroy = true
  
  uniform_bucket_level_access = true
}