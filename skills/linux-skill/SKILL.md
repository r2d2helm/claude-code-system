---
name: linux-skill
description: "Administration serveurs Linux : services, packages, securite, performance, backup, SSH, DNS, Nginx, SSL."
---

# Super Agent Linux Administration

Agent intelligent pour administrer les systemes Linux : services, packages, securite, performance.

## Philosophie

> "Un serveur Linux bien configure est un serveur qu'on oublie."

## Compatibilite

| Composant | Support |
|-----------|---------|
| Ubuntu | 22.04+, 24.04 |
| Debian | 12+ |
| RHEL/Rocky | 9+ |
| Acces | SSH ou terminal local |

## Commandes Slash

### Systeme

| Commande | Description |
|----------|-------------|
| `/lx-status` | Vue d'ensemble systeme |
| `/lx-services` | Gestion services systemd |
| `/lx-packages` | Gestion packages (apt/dnf) |
| `/lx-process` | Gestion des processus |

### Utilisateurs & Securite

| Commande | Description |
|----------|-------------|
| `/lx-users` | Gestion utilisateurs/groupes |
| `/lx-firewall` | Firewall (ufw/firewalld) |
| `/lx-security` | Audit de securite |

### Reseau & Stockage

| Commande | Description |
|----------|-------------|
| `/lx-network` | Configuration reseau |
| `/lx-disk` | Disques, LVM, montages |

### Monitoring

| Commande | Description |
|----------|-------------|
| `/lx-logs` | Analyse des logs (journalctl) |
| `/lx-cron` | Gestion cron/timers |
| `/lx-performance` | Analyse de performance |

### Avance

| Commande | Description |
|----------|-------------|
| `/lx-backup` | Backup rsync/tar (incremental, rotation, cron) |
| `/lx-ssh` | Configuration SSH (cles, hardening, tunnels) |
| `/lx-dns` | Configuration DNS (resolv, systemd-resolved, dig) |
| `/lx-nginx` | Gestion Nginx (vhosts, reverse proxy, SSL) |
| `/lx-certbot` | Certificats SSL Let's Encrypt (obtain, renew, wildcard) |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/lx-wizard setup` | Hardening initial du serveur |
| `/lx-wizard lamp` | Installation stack LAMP |
| `/lx-wizard docker-host` | Configuration hote Docker |

## Best Practices

- **Mises a jour** : `unattended-upgrades` pour les patchs securite automatiques
- **Firewall** : activer ufw/firewalld, politique deny par defaut
- **SSH** : cles Ed25519, desactiver password auth, port non-standard
- **Utilisateurs** : pas de login root direct, utiliser sudo avec audit
- **Backups** : rsync incremental quotidien, test de restauration mensuel
- **Monitoring** : surveiller CPU, RAM, disque, et services critiques
- **Logs** : centraliser avec journald, rotation avec logrotate
- **SELinux/AppArmor** : laisser en mode enforcing quand possible

## References

- [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- [Debian Admin Handbook](https://debian-handbook.info/)
- [RHEL Documentation](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9)
- [Linux Hardening Guide (CIS)](https://www.cisecurity.org/benchmark/distribution_independent_linux)
- [SSH Best Practices](https://infosec.mozilla.org/guidelines/openssh)
