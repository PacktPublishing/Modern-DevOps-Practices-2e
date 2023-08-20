provider "google" {
  project     = var.project_id
  region      = "us-central1"
  zone        = "us-central1-c"
}

provider "kubectl" {
  host                   = module.gke_auth.host
  cluster_ca_certificate = module.gke_auth.cluster_ca_certificate
  token                  = module.gke_auth.token
  load_config_file       = false
}

terraform {
  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }
  }
  backend "gcs" {
    prefix  = "mdo-terraform"
  }
}
