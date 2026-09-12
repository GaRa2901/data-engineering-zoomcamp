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

# Credentials defined on GOOGLE_CREDENTIALS environment variable.

# Google storage bucket creation
# google_storage_bucket is the common denominator for all buckets that are created -> Meaning that if it is wished to perform any kind of action on all
# buckets, the command would reffer to the "google_storage_bucket". Whereas the "auto-expire" is local identificator for a given bucket

resource "google_storage_bucket" "test-bucket" {
  name          = "dataengineeringzoomcamp-507920-terra-bucket"  # this identification must be unique across all GCP project.
  # there are lots of ways and strategies to ensure that each resource is unique, the instructor uses the project name (which is globally unique) and appends another name to it.
  location      = "EU"  # since we are in Europe.
  force_destroy = true
  
  # Not going to be used on this course.
  # lifecycle_rule {
  #   condition {
  #     age = 3  # according to the docs, this time measurement reffers to days.
  #   }
  #   action {
  #     type = "Delete"  # after the defined timeframe, the given resource will be deleted.
  #   }
  # }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"  # An strategy for uploading large files to the bucket is to process them by chunks. Using less resources
      # for processing it and it may be faster than using the whole content. However, this process might not be succesful and may get stuck in a middle of
      # a processing, thus this action defines that when a given file gets stuck under this processing, if it takes longer than one day, terraform will abort it.
      # Avoiding the consuption of unecessary resources.
    }
  }
}