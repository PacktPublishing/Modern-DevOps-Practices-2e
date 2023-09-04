variable project_id {}

variable branch {
  description = "branch"
  type        = string
  default     = "dev"
}

variable cluster_name {
  type      = string
  description = "cluster name"
  default   = "mdo-cluster"
}

variable "location" {
  type        = string
  description = "cluster location"
  default     = "us-central1-a"
}
