# Wizard: Backup Setup

Assistant de configuration initiale d'une strategie de backup pour le homelab r2d2.

## Questions

1. **Cible** : Que faut-il sauvegarder ? (VMs, PostgreSQL, fichiers, vault, tout)
2. **Destination** : Ou stocker les backups ? (NFS VM 104, local, git remote)
3. **Frequence** : Quelle frequence ? (quotidien, toutes les 6h, hebdomadaire)
4. **Retention** : Combien de temps garder ? (7j/4sem/12mois standard)
5. **Chiffrement** : Chiffrer les backups ? (recommande pour credentials)

## Processus

### Etape 1 : Inventaire des donnees critiques

```bash
# Lister les VMs
ssh root@192.168.1.215 "qm list"

# Lister les bases PostgreSQL
ssh r2d2helm@192.168.1.164 "psql -U postgres -h localhost -l"

# Taille du vault Obsidian
du -sh "C:\Users\r2d2\Documents\Knowledge"

# Volumes Docker par VM
ssh root@{ip} "docker volume ls"
```

### Etape 2 : Verifier les destinations

```bash
# Espace disponible sur NFS (VM 104)
ssh r2d2helm@192.168.1.164 "df -h /mnt/nfs/"

# Creer l'arborescence de backup
ssh r2d2helm@192.168.1.164 "mkdir -p /mnt/nfs/backups/{proxmox,postgresql,rsync,docker-volumes,config}"
```

### Etape 3 : Configurer les planifications

Utiliser `/bak-schedule` pour chaque type de backup identifie.

### Etape 4 : Premier backup + verification

```bash
# Lancer un backup de chaque type
/bak-create {type}

# Verifier l'integrite
/bak-verify {type}
```

### Etape 5 : Documenter

Creer une note dans le vault avec la strategie choisie :
- Quoi, ou, quand, combien de temps
- Procedure de restauration testee
