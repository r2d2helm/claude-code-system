# Commande: /sec-scan

Scanner les vulnerabilites : ports ouverts, CVE sur images Docker, paquets obsoletes, configurations dangereuses.

## Cible : $ARGUMENTS

Accepte : `all`, un nom de VM, une IP, ou `docker` pour scanner uniquement les images Docker.

## Syntaxe

```
/sec-scan [cible] [--type <type>] [--severity <level>]
```

## Processus

### 1. Scan des Ports Ouverts

```bash
# Depuis le PC Windows (scan reseau local)
# Avec nmap si installe
nmap -sT -p 1-65535 <IP> --open

# Alternative sans nmap : scan des ports connus
for port in 22 80 443 3000 3003 3020 5432 8006 8020 8082 8084 8091 19999 45876; do
  (echo >/dev/tcp/<IP>/$port) 2>/dev/null && echo "OPEN: $port"
done

# Depuis une VM (scan interne)
ssh root@<IP> "ss -tuln | grep LISTEN | sort -t: -k2 -n"
```

### 2. Scan des Ports Attendus vs Reels

```bash
# Ports attendus par machine (reference)
# VM 100: 22, 8091, 3003, 19999, 8082, 8084, 45876
# VM 103: 22, 8020, 3020, 8091, 3003, 8082, 8084, 45876, + supabase
# VM 104: 22, 5432, 8091, 3003, 8082, 8084, 45876
# VM 105: 22, 8020, 3020
# Proxmox: 22, 8006, 45876

# Comparer : tout port non dans la liste = ALERTE
ssh root@<IP> "ss -tuln | awk '/LISTEN/ {print \$5}' | grep -oP '\d+$' | sort -nu"
```

### 3. Scan CVE Images Docker

```bash
# Avec Docker Scout (integre Docker Desktop/CLI)
ssh root@<IP> "docker scout cves --only-severity critical,high <image>"

# Avec Trivy (si installe)
ssh root@<IP> "trivy image --severity HIGH,CRITICAL <image>"

# Scanner toutes les images en cours d'utilisation
ssh root@<IP> 'docker ps --format "{{.Image}}" | sort -u | while read img; do
  echo "=== $img ==="
  docker scout quickview "$img" 2>/dev/null || echo "Scout non disponible"
done'

# Alternative : verifier l'age des images
ssh root@<IP> 'docker images --format "{{.Repository}}:{{.Tag}}\t{{.CreatedSince}}" | sort'
```

### 4. Scan des Paquets Systeme

```bash
# Paquets avec CVE connues (Debian/Ubuntu)
ssh root@<IP> "apt list --upgradable 2>/dev/null"

# Specifiquement les mises a jour de securite
ssh root@<IP> "apt list --upgradable 2>/dev/null | grep -i security"

# Verifier les paquets obsoletes
ssh root@<IP> "apt list --installed 2>/dev/null | wc -l"
```

### 5. Scan des Configurations Dangereuses

```bash
# Fichiers avec permissions trop larges
ssh root@<IP> "find /etc -perm -002 -type f 2>/dev/null"
ssh root@<IP> "find /opt -name '*.env' -perm -044 2>/dev/null"

# Docker daemon config
ssh root@<IP> "cat /etc/docker/daemon.json 2>/dev/null"

# Verifier si Docker ecoute sur un socket TCP (dangereux)
ssh root@<IP> "ps aux | grep dockerd | grep -i tcp"

# Verifier les volumes montes en ecriture sur des chemins sensibles
ssh root@<IP> 'docker ps -q | xargs docker inspect --format "{{.Name}}: {{range .Mounts}}{{.Source}}:{{.Destination}}({{.RW}}) {{end}}" 2>/dev/null'
```

### 6. Scan Reseau

```bash
# ARP table (detecter des machines inconnues)
arp -a

# Connexions etablies suspectes
ssh root@<IP> "ss -tunap | grep ESTAB | grep -v '192.168.1\.\|127.0.0.1'"
```

## Format de Rapport

```
=== SCAN VULNERABILITES ===
Date: YYYY-MM-DD
Cible: [machine]

[CRITICAL] Vulnerabilites critiques
  - CVE-XXXX-YYYY: description (image: xxx)
  - Port inattendu : XXXX ouvert sur <IP>

[HIGH] Vulnerabilites hautes
  - N paquets avec mises a jour de securite
  - .env avec permissions 644

[MEDIUM] Points d'attention
  - Images Docker de plus de 90 jours
  - N connexions non-locales

[INFO] Informations
  - N ports ouverts (N attendus)
  - N images Docker scannees
```

## Options

| Option | Description |
|--------|-------------|
| `--type ports\|docker\|packages\|config\|network` | Type de scan specifique |
| `--severity critical\|high\|medium\|all` | Severite minimale (defaut: high) |
| `--quick` | Scan rapide (ports + Docker critiques uniquement) |

## Exemples

```bash
/sec-scan all                          # Scan complet toute l'infra
/sec-scan vm103 --type docker          # CVE Docker sur VM 103
/sec-scan all --type ports             # Scan ports toutes machines
/sec-scan vm100 --quick                # Scan rapide VM 100
/sec-scan docker --severity critical   # CVE critiques sur toutes les images
```

## Voir Aussi

- `/sec-audit` - Audit complet (inclut le scan)
- `/dk-security` - Scan Docker detaille
- `/sec-harden` - Corriger les vulnerabilites trouvees
