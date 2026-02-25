---
name: security-skill
description: "Securite infrastructure : audit, hardening, SSL/TLS, firewall, vulnerabilites, acces, logs securite."
prefix: /sec-*
---

# Super Agent Security Infrastructure

Agent intelligent pour securiser l'infrastructure homelab : audit, hardening, certificats, firewall, vulnerabilites, acces, logs.

## Philosophie

> "La securite n'est pas un produit, c'est un processus. Un homelab non audite est un homelab compromis."

## Perimetre

| Cible | IP | OS | Services exposes |
|-------|----|----|------------------|
| PC Windows | locale | Windows 11 | RDP, SSH agent Beszel |
| Proxmox Host | 192.168.1.215 | Proxmox VE | Web UI :8006, SSH |
| VM 100 r2d2-stage | 192.168.1.162 | Ubuntu 24.04 | Beszel :8091, Uptime Kuma :3003, Netdata :19999, Dozzle :8082, ntfy :8084 |
| VM 103 r2d2-main | 192.168.1.163 | Ubuntu | Taskyn :8020/:3020, Supabase, LiteLLM, Langfuse, monitoring |
| VM 104 r2d2-store | 192.168.1.164 | Ubuntu | PostgreSQL :5432, NFS, monitoring |
| VM 105 r2d2-lab | 192.168.1.161 | Ubuntu | RAG, Taskyn |

## Commandes Slash

### Audit & Scan

| Commande | Description |
|----------|-------------|
| `/sec-audit` | Audit de securite complet (SSH, ports, users, perms, Docker) |
| `/sec-scan` | Scanner vulnerabilites (ports ouverts, CVE images Docker) |
| `/sec-users` | Audit comptes utilisateurs et permissions |
| `/sec-logs` | Analyser les logs de securite (auth.log, fail2ban, syslog) |

### Hardening & Protection

| Commande | Description |
|----------|-------------|
| `/sec-harden` | Appliquer le hardening (SSH, sysctl, services inutiles) |
| `/sec-firewall` | Gerer les regles firewall (ufw/iptables) |
| `/sec-ssl` | Gerer certificats SSL/TLS (creation, renouvellement, verification) |

### Docker & Credentials

| Commande | Description |
|----------|-------------|
| `/sec-docker` | Securite Docker (images, runtime, secrets, privileges) |
| `/sec-passwords` | Audit mots de passe et credentials |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/sec-wizard audit` | Audit complet guide (questionnaire + scan + rapport) |
| `/sec-wizard harden` | Hardening guide pas a pas (SSH, firewall, services, Docker) |

## Principes de Securite

### Moindre Privilege
- Chaque service tourne avec le minimum de permissions
- Pas de `--privileged` sur les containers Docker
- sudo avec mot de passe, jamais NOPASSWD sauf exception justifiee
- Utilisateurs applicatifs separes (pas de root pour les services)

### Defense en Profondeur
- Firewall : deny all by default, allow list
- SSH : cles Ed25519 uniquement, pas de password auth, pas de root login
- Docker : non-root containers, capabilities minimales, read-only rootfs si possible
- Reseau : Docker networks isoles par stack, pas de `--network host` sauf monitoring

### Secrets & Credentials
- Jamais de secrets en clair dans les fichiers versionnes
- Utiliser variables d'environnement ou Docker secrets
- Fichiers .env avec permissions 600
- Rotation des mots de passe tous les 90 jours
- Credentials stockes dans `Documents/claude-config-backup/` (protege par path_guard hook)

### Mises a Jour
- `unattended-upgrades` actif sur toutes les VMs Ubuntu
- Images Docker : scan CVE regulier, rebuilds mensuels
- Proxmox : mises a jour via `pveupdate` + `pveupgrade`
- Surveillance des CVE critiques via Uptime Kuma ou alertes manuelles

### Logs & Detection
- auth.log centralise et surveille
- fail2ban actif sur SSH (toutes VMs)
- Rotation des logs via logrotate
- Alertes Telegram via ntfy pour evenements critiques
- Dozzle pour les logs Docker en temps reel

### Reseau
- Pas d'exposition directe sur Internet (homelab local)
- Segmentation via Docker networks (chaque stack isolee)
- SSH inter-VMs avec cles, pas de password
- Ports exposes uniquement ceux necessaires

## Score de Securite

Systeme de scoring pour evaluer la posture de securite :

| Categorie | Points | Criteres |
|-----------|--------|----------|
| SSH Hardening | /20 | Root desactive, password auth off, cles Ed25519, MaxAuthTries |
| Firewall | /15 | Actif, deny default, regles minimales |
| Mises a jour | /15 | Pas de CVE critiques, unattended-upgrades actif |
| fail2ban | /10 | Actif, jails SSH configurees |
| Docker | /15 | Non-root, pas de privileged, images scannees |
| Credentials | /10 | Pas de secrets en clair, .env protege |
| Logs | /10 | auth.log accessible, rotation, surveillance |
| Users | /5 | Pas de comptes inutiles, shells restreints |
| **Total** | **/100** | |

## Integration avec les Autres Skills

| Skill | Relation |
|-------|----------|
| **linux-skill** | `/lx-security`, `/lx-firewall`, `/lx-ssh` pour les actions unitaires |
| **docker-skill** | `/dk-security` pour le scan CVE images |
| **monitoring-skill** | `/mon-alerts` pour les alertes securite |
| **proxmox-skill** | `/pve-firewall` pour le firewall Proxmox |
| **windows-skill** | `/win-security`, `/win-defender` pour Windows |

**Difference avec les skills existants** : security-skill est transversal. Il orchestre un audit multi-machines et multi-domaines, tandis que les skills individuels (linux, docker, windows) gerent la securite de leur perimetre specifique.

## Troubleshooting

### SSH refuse la connexion
1. Verifier que le service tourne : `systemctl status sshd`
2. Verifier les logs : `journalctl -u sshd -n 20`
3. Verifier le firewall : `ufw status` ou `iptables -L`
4. Verifier les cles : `ls -la ~/.ssh/authorized_keys`

### fail2ban bloque une IP legitime
1. Verifier les bans : `fail2ban-client status sshd`
2. Debloquer : `fail2ban-client set sshd unbanip <IP>`
3. Ajouter en whitelist : `ignoreip` dans jail.local

### Certificat SSL expire
1. Verifier : `openssl x509 -in cert.pem -noout -dates`
2. Renouveler : `certbot renew`
3. Verifier le renouvellement auto : `systemctl status certbot.timer`

## References

- [CIS Benchmarks Linux](https://www.cisecurity.org/benchmark/distribution_independent_linux)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Mozilla SSH Guidelines](https://infosec.mozilla.org/guidelines/openssh)
- [OWASP Infrastructure Security](https://owasp.org/www-project-web-security-testing-guide/)
- [fail2ban Documentation](https://www.fail2ban.org/wiki/index.php/Main_Page)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
