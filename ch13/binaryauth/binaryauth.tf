resource "google_kms_key_ring" "qa-attestor-keyring" {
  name     = "qa-attestor-keyring"
  location = var.region
  lifecycle {
    prevent_destroy = false
  }
}

module "qa-attestor" {
  source = "terraform-google-modules/kubernetes-engine/google//modules/binary-authorization"
  attestor-name = "quality-assurance"
  project_id    = var.project_id
  keyring-id    = google_kms_key_ring.qa-attestor-keyring.id
}

resource "google_binary_authorization_policy" "policy" {
  global_policy_evaluation_mode = "ENABLE"
  default_admission_rule {
    evaluation_mode  = "REQUIRE_ATTESTATION"
    enforcement_mode = "ENFORCED_BLOCK_AND_AUDIT_LOG"
    require_attestations_by = [
      module.qa-attestor.attestor
    ]
  }
}
