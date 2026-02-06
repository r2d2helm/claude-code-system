# 🏗️ /pve-terraform - Infrastructure as Code

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

## Conteneurs LXC

### CT Simple
```hcl
resource "proxmox_virtual_environment_container" "nginx" {
  node_name   = var.target_node
  vm_id       = 200
  description = "Nginx Proxy"

  unprivileged = true
  start_on_boot = true

  operating_system {
    template_file_id = proxmox_virtual_environment_download_file.debian_ct.id
    type             = "debian"
  }

  cpu {
    cores = 2
  }

  memory {
    dedicated = 512
    swap      = 512
  }

  disk {
    datastore_id = "local-lvm"
    size         = 8
  }

  network_interface {
    name   = "eth0"
    bridge = "vmbr0"
    firewall = true
  }

  initialization {
    hostname = "nginx-proxy"
    ip_config {
      ipv4 {
        address = "192.168.1.200/24"
        gateway = "192.168.1.1"
      }
    }
  }

  features {
    nesting = true  # Pour Docker dans CT
  }
}
```

## Storage & Templates

### Télécharger image Cloud-Init
```hcl
resource "proxmox_virtual_environment_download_file" "ubuntu_cloud_image" {
  content_type = "iso"
  datastore_id = "local"
  node_name    = var.target_node
  url          = "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
  file_name    = "ubuntu-24.04-cloudimg.img"
}

resource "proxmox_virtual_environment_download_file" "debian_ct" {
  content_type = "vztmpl"
  datastore_id = "local"
  node_name    = var.target_node
  url          = "http://download.proxmox.com/images/system/debian-12-standard_12.7-1_amd64.tar.zst"
}
```

### Pool de stockage
```hcl
resource "proxmox_virtual_environment_pool" "production" {
  pool_id = "production"
  comment = "Production VMs pool"
}
```

## Réseau SDN

### Zone VLAN
```hcl
resource "proxmox_virtual_environment_network_zone" "vlans" {
  zone_id = "vlan-zone"
  type    = "vlan"
  bridge  = "vmbr0"
  nodes   = ["pve1", "pve2", "pve3"]
}

resource "proxmox_virtual_environment_network_vnet" "web_vlan" {
  vnet_id = "web-net"
  zone_id = proxmox_virtual_environment_network_zone.vlans.zone_id
  tag     = 100
  alias   = "Web Network"
}

resource "proxmox_virtual_environment_network_subnet" "web_subnet" {
  vnet_id    = proxmox_virtual_environment_network_vnet.web_vlan.vnet_id
  zone_id    = proxmox_virtual_environment_network_zone.vlans.zone_id
  cidr       = "10.100.0.0/24"
  gateway    = "10.100.0.1"
  snat       = true
  dhcp_range = ["10.100.0.100", "10.100.0.200"]
}
```

## Haute Disponibilité

### Groupe HA
```hcl
resource "proxmox_virtual_environment_hagroup" "production" {
  group_id  = "production"
  nodes     = ["pve1:2", "pve2:1", "pve3:1"]
  nofailback = false
  restricted = true
  comment   = "Production HA Group"
}

resource "proxmox_virtual_environment_haresource" "critical_vm" {
  resource_id = "vm:100"
  group       = proxmox_virtual_environment_hagroup.production.group_id
  state       = "started"
  max_relocate = 3
  max_restart  = 3
}
```

## Intégration Ansible

### Provisionner avec Ansible
```hcl
resource "proxmox_virtual_environment_vm" "app" {
  name      = "app-server"
  node_name = var.target_node

  # ... config VM ...

  provisioner "remote-exec" {
    inline = ["echo 'VM ready for Ansible'"]

    connection {
      type        = "ssh"
      user        = "admin"
      private_key = file("~/.ssh/id_ed25519")
      host        = self.ipv4_addresses[0][0]
    }
  }

  provisioner "local-exec" {
    working_dir = "${path.module}/ansible"
    command = <<-EOT
      ANSIBLE_HOST_KEY_CHECKING=False \
      ansible-playbook -u admin \
        -i '${self.ipv4_addresses[0][0]},' \
        --private-key ~/.ssh/id_ed25519 \
        playbook.yml
    EOT
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

## Structure Projet Recommandée

```
proxmox-infra/
├── main.tf              # Resources principales
├── variables.tf         # Variables
├── outputs.tf          # Outputs
├── versions.tf         # Provider versions
├── terraform.tfvars    # Valeurs (gitignore!)
├── modules/
│   ├── vm/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── lxc/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── environments/
    ├── dev/
    │   └── main.tf
    ├── staging/
    │   └── main.tf
    └── prod/
        └── main.tf
```

## Best Practices 2025-2026

1. **Provider bpg/proxmox** plutôt que telmate (deprecated)
2. **API Tokens** plutôt que password
3. **Cloud-Init templates** pour provisioning rapide
4. **State remote** (S3, Consul) pour équipes
5. **Modules** pour réutilisabilité
6. **Workspaces** pour environnements multiples
