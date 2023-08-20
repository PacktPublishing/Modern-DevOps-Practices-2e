data "kubectl_file_documents" "apps" {
    pattern = "../manifests/argocd/apps.yaml"
}

resource "kubectl_manifest" "apps" {
  depends_on = [
    kubectl_manifest.argocd,
  ]
  for_each  = data.kubectl_file_documents.apps.manifests
  yaml_body = each.value
  override_namespace = "argocd"
}
