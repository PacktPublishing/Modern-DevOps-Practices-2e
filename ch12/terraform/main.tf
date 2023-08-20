resource "google_service_account" "main" {
  account_id   = "gke-mdo-cluster-sa"
  display_name = "GKE MDO Cluster Service Account"
}

resource "google_container_cluster" "main" {
  name               = "mdo-cluster"
  location           = "us-central1-a"
  initial_node_count = 3
  node_config {
    service_account = google_service_account.main.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
  timeouts {
    create = "30m"
    update = "40m"
  }
}
