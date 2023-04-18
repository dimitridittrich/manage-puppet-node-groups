locals {
 repo_name = "your_repo_name" 
}

data "azurerm_subscription" "main" {}

resource "null_resource" "create-puppet-node-groups" {
  triggers = {
    build_number = timestamp()
  }
  provisioner "local-exec" {
    command = "chmod +x ${path.module}/scripts/create-puppet-node-groups.py && python3 ${path.module}/create-puppet-node-groups.py ${local.repo_name} ${data.azurerm_subscription.main.display_name}"
  }
}
