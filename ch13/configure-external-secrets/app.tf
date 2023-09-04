data "kubectl_file_documents" "apps" {
    content = file("../manifests/argocd/apps.yaml")
}

resource "kubectl_manifest" "apps" {
  depends_on = [
    kubectl_manifest.argocd,
  ]
  for_each  = data.kubectl_file_documents.apps.manifests
  yaml_body = each.value
  override_namespace = "argocd"
}

data "kubectl_file_documents" "external-secrets" {
    content = file("../manifests/argocd/external-secrets.yaml")
}

resource "kubectl_manifest" "external-secrets" {
  depends_on = [
    kubectl_manifest.argocd,
  ]
  for_each  = data.kubectl_file_documents.external-secrets.manifests
  yaml_body = each.value
  override_namespace = "argocd"
}

data "kubectl_path_documents" "blog-app-gcpsm-secret" {
    pattern = "../external-secret-manifests/*.yaml"
}

resource "kubectl_manifest" "blog-app-gcpsm-secret" {
  depends_on = [
    kubectl_manifest.external-secrets,
  ]
  for_each  = toset(data.kubectl_path_documents.blog-app-gcpsm-secret.documents)
  yaml_body = each.value
}
