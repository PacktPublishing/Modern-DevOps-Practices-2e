resource "google_kms_key_ring" "qa-attestor-keyring" {
  count = var.branch == "dev" ? 1 : 0
  name     = "qa-attestor-keyring"
  location = var.region
  lifecycle {
    prevent_destroy = false
  }
}

module "qa-attestor" {
  count = var.branch == "dev" ? 1 : 0
  source = "terraform-google-modules/kubernetes-engine/google//modules/binary-authorization"
  attestor-name = "quality-assurance"
  project_id    = var.project_id
  keyring-id    = google_kms_key_ring.qa-attestor-keyring[0].id
}

resource "google_binary_authorization_policy" "policy" {
  count = var.branch == "dev" ? 1 : 0
  admission_whitelist_patterns {
    name_pattern = "gcr.io/google_containers/*"
  }
  admission_whitelist_patterns {
    name_pattern = "gcr.io/google-containers/*"
  }
  admission_whitelist_patterns {
    name_pattern = "k8s.gcr.io/**"
  }
  admission_whitelist_patterns {
    name_pattern = "gke.gcr.io/**"
  }
  admission_whitelist_patterns {
    name_pattern = "gcr.io/stackdriver-agents/*"
  }
  admission_whitelist_patterns {
    name_pattern = "quay.io/argoproj/*"
  }
  admission_whitelist_patterns {
    name_pattern = "ghcr.io/dexidp/*"
  }
  admission_whitelist_patterns {
    name_pattern = "docker.io/redis[@:]*"
  }
  admission_whitelist_patterns {
    name_pattern = "ghcr.io/external-secrets/*"
  }
  global_policy_evaluation_mode = "ENABLE"
  default_admission_rule {
    evaluation_mode  = "REQUIRE_ATTESTATION"
    enforcement_mode = "ENFORCED_BLOCK_AND_AUDIT_LOG"
    require_attestations_by = [
      module.qa-attestor[0].attestor
    ]
  }
}
