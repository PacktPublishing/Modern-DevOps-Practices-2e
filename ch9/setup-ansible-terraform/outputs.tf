output "control_node_ip_addr" {
  value = azurerm_public_ip.control_node_publicip.ip_address
}

output "k8s-control-plane_ip_addr" {
  value = azurerm_public_ip.k8s-control-plane_publicip.ip_address
}
