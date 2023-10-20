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

data "kubectl_file_documents" "gcpsm-secret" {
    content = file("../manifests/argocd/gcpsm-secret.yaml")
}

resource "kubectl_manifest" "gcpsm-secrets" {
  depends_on = [
    kubectl_manifest.external-secrets,
  ]
  for_each  = data.kubectl_file_documents.gcpsm-secret.manifests
  yaml_body = each.value
}

data "kubectl_file_documents" "istio" {
    content = file("../manifests/argocd/istio.yaml")
}

resource "kubectl_manifest" "istio" {
  depends_on = [
    kubectl_manifest.gcpsm-secrets,
  ]
  for_each  = data.kubectl_file_documents.istio.manifests
  yaml_body = each.value
  override_namespace = "argocd"
}
