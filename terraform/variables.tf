variable "project" {
  type        = string
  description = "GCP project ID"
  default     = "kestra-sandbox-450921"
}

variable "region" {
  type        = string
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "us-central1"
}

variable "mental_health_dataset" {
  type        = string
  description = "Dataset in BigQuery"
  default     = "mental_health_survey"
}