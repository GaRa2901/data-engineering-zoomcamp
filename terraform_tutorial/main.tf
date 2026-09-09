terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "8.2.0"
    }
  }
}

# Configuration retrieved from terraform google provider docs.
provider "google" {
  project = "dataengineeringzoomcamp-507920"  # retrived from GCP project Dashboard page (accessible through the lateral nav bar within the option Cloud Overview)
  region  = "europe-southwest1"  # Portugal Region.
}