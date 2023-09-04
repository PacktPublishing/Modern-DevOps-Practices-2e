resource "time_sleep" "wait_30_seconds" {
  depends_on = [google_container_cluster.main]
  create_duration = "30s"
}

module "gke_auth" {
  depends_on           = [time_sleep.wait_30_seconds]
  source               = "terraform-google-modules/kubernetes-engine/google//modules/auth"
  project_id           = var.project_id
  cluster_name         = google_container_cluster.main.name
  location             = var.location
  use_private_endpoint = false
}

data "kubectl_file_documents" "namespace" {
  content = file("../manifests/argocd/namespace.yaml")
} 

data "kubectl_file_documents" "argocd" {
  content = file("../manifests/argocd/install.yaml")
}

resource "kubectl_manifest" "namespace" {
  for_each  = data.kubectl_file_documents.namespace.manifests
  yaml_body = each.value 
  override_namespace = "argocd"
}

resource "kubectl_manifest" "argocd" {
  depends_on = [
    kubectl_manifest.namespace,
  ]
  for_each  = data.kubectl_file_documents.argocd.manifests
  yaml_body = each.value
  override_namespace = "argocd"
}
