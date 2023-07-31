packer {
  required_plugins {
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = "=1.1.0"
    }
    azure = {
      source  = "github.com/hashicorp/azure"
      version = "=1.4.5"
    }
  }
}
