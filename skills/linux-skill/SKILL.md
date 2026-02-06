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
| `/lx-backup` | Backup rsync/tar [PREVU] |
| `/lx-ssh` | Configuration SSH [PREVU] |
| `/lx-dns` | Configuration DNS [PREVU] |
| `/lx-nginx` | Gestion Nginx [PREVU] |
| `/lx-certbot` | Certificats SSL [PREVU] |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/lx-wizard setup` | Hardening initial du serveur |
| `/lx-wizard lamp` | Installation stack LAMP |
| `/lx-wizard docker-host` | Configuration hote Docker |
