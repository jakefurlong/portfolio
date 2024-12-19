provider "google" {
  project = var.gcp_project
  region  = var.default_region
  zone    = var.default_zone
  credentials = file(var.gcp_svc_key)
}