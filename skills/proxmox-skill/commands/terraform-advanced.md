> Partie avancée de [[terraform]]. Commandes essentielles dans le fichier principal.

# /pve-terraform - LXC, SDN, HA, Ansible et Structure Projet

## Description
Ressources Terraform avancées : conteneurs LXC, storage, SDN, haute disponibilité,
intégration Ansible et structure projet recommandée.

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
