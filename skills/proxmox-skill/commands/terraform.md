# /pve-terraform - Infrastructure as Code

## Description
Provisioning Proxmox VE 9+ avec Terraform et OpenTofu.

## Syntaxe
```
/pve-terraform [action] [options]
```

## Providers Terraform

### Provider bpg/proxmox (Recommandé 2025+)
```hcl
# versions.tf
terraform {
  required_version = ">= 1.7.0"
  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "~> 0.70.0"
    }
  }
}

# provider.tf
provider "proxmox" {
  endpoint = var.proxmox_api_url
  api_token = var.proxmox_api_token
  insecure = true  # Pour certificat auto-signé

  ssh {
    agent = true
    # Ou avec clé
    # private_key = file("~/.ssh/id_ed25519")
  }
}
```

### Variables
```hcl
# variables.tf
variable "proxmox_api_url" {
  description = "Proxmox API URL"
  type        = string
  default     = "https://pve.example.com:8006/"
}

variable "proxmox_api_token" {
  description = "Proxmox API Token"
  type        = string
  sensitive   = true
}

variable "target_node" {
  description = "Target Proxmox node"
  type        = string
  default     = "pve1"
}
```

### Fichier secrets
```hcl
# terraform.tfvars (NE PAS COMMITER)
proxmox_api_url   = "https://192.168.1.10:8006/"
proxmox_api_token = "terraform@pve!terraform-token=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
target_node       = "pve1"
```

## Ressources VM

### VM Simple
```hcl
# vm.tf
resource "proxmox_virtual_environment_vm" "web_server" {
  name        = "web-01"
  description = "Web Server"
  node_name   = var.target_node
  vm_id       = 100

  tags = ["web", "production"]

  cpu {
    cores   = 2
    sockets = 1
    type    = "host"
  }

  memory {
    dedicated = 2048
  }

  agent {
    enabled = true
  }

  disk {
    datastore_id = "local-lvm"
    file_id      = proxmox_virtual_environment_download_file.ubuntu_cloud_image.id
    interface    = "scsi0"
    size         = 32
    iothread     = true
    discard      = "on"
  }

  network_device {
    bridge   = "vmbr0"
    model    = "virtio"
    firewall = true
  }

  initialization {
    ip_config {
      ipv4 {
        address = "192.168.1.100/24"
        gateway = "192.168.1.1"
      }
    }
    user_account {
      username = "admin"
      keys     = [file("~/.ssh/id_ed25519.pub")]
    }
  }

  lifecycle {
    ignore_changes = [
      initialization,
    ]
  }
}
```

### VM depuis Clone/Template
```hcl
resource "proxmox_virtual_environment_vm" "cloned_vm" {
  name      = "app-01"
  node_name = var.target_node
  vm_id     = 101

  clone {
    vm_id = 9000  # Template ID
  }

  cpu {
    cores = 4
    type  = "host"
  }

  memory {
    dedicated = 4096
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = 50
    iothread     = true
  }

  initialization {
    ip_config {
      ipv4 {
        address = "192.168.1.101/24"
        gateway = "192.168.1.1"
      }
    }
    dns {
      servers = ["8.8.8.8", "8.8.4.4"]
    }
  }
}
```

### Plusieurs VMs (count)
```hcl
variable "vm_count" {
  default = 3
}

resource "proxmox_virtual_environment_vm" "workers" {
  count     = var.vm_count
  name      = "worker-${format("%02d", count.index + 1)}"
  node_name = var.target_node
  vm_id     = 110 + count.index

  clone {
    vm_id = 9000
  }

  cpu {
    cores = 2
    type  = "host"
  }

  memory {
    dedicated = 2048
  }

  initialization {
    ip_config {
      ipv4 {
        address = "192.168.1.${110 + count.index}/24"
        gateway = "192.168.1.1"
      }
    }
  }
}

output "worker_ips" {
  value = proxmox_virtual_environment_vm.workers[*].ipv4_addresses
}
```

### VM avec for_each
```hcl
variable "vms" {
  type = map(object({
    cores  = number
    memory = number
    ip     = string
  }))
  default = {
    "web" = {
      cores  = 2
      memory = 2048
      ip     = "192.168.1.100"
    }
    "db" = {
      cores  = 4
      memory = 8192
      ip     = "192.168.1.101"
    }
    "cache" = {
      cores  = 2
      memory = 4096
      ip     = "192.168.1.102"
    }
  }
}

resource "proxmox_virtual_environment_vm" "servers" {
  for_each  = var.vms
  name      = each.key
  node_name = var.target_node

  clone {
    vm_id = 9000
  }

  cpu {
    cores = each.value.cores
    type  = "host"
  }

  memory {
    dedicated = each.value.memory
  }

  initialization {
    ip_config {
      ipv4 {
        address = "${each.value.ip}/24"
        gateway = "192.168.1.1"
      }
    }
  }
}
```

## Commandes Terraform

```bash
# Initialiser
terraform init

# Valider
terraform validate

# Plan
terraform plan -out=tfplan

# Appliquer
terraform apply tfplan

# Détruire
terraform destroy

# État
terraform state list
terraform state show proxmox_virtual_environment_vm.web_server

# Import existant
terraform import proxmox_virtual_environment_vm.existing pve1/qemu/100
```

## Voir Aussi
- `/pve-vm` - Gestion VMs manuelle
- `/pve-ct` - Gestion conteneurs manuelle

> Voir aussi : [[terraform-advanced]]
