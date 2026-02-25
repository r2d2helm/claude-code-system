# Commande: /bak-prune

Nettoyer les vieux backups selon la politique de retention.

## Syntaxe

```
/bak-prune [type] [options]
```

## Politique de Retention par Defaut

| Type | Quotidien | Hebdo | Mensuel |
|------|-----------|-------|---------|
| VM snapshot | 7 jours | 4 semaines | 6 mois |
| pg_dump | 7 jours | 4 semaines | 12 mois |
| rsync | 7 jours | 4 semaines | 6 mois |
| Docker volumes | - | 4 semaines | 6 mois |

## Nettoyage PostgreSQL

```bash
# Lister les dumps et leur age
ssh r2d2helm@192.168.1.164 "ls -lth /mnt/nfs/backups/postgresql/"

# Dry-run : voir ce qui serait supprime (> 7 jours)
ssh r2d2helm@192.168.1.164 "find /mnt/nfs/backups/postgresql/ -name '*.dump' -mtime +7 -ls"

# Supprimer les dumps > 7 jours (garder hebdo/mensuel manuellement)
ssh r2d2helm@192.168.1.164 "find /mnt/nfs/backups/postgresql/ -name '*.dump' -mtime +7 -delete -print"
```

## Nettoyage Proxmox

```bash
# Lister les backups vzdump
ssh root@192.168.1.215 "ls -lth /var/lib/vz/dump/"

# Voir l'espace utilise
ssh root@192.168.1.215 "du -sh /var/lib/vz/dump/"

# Supprimer les vieux backups (> 30 jours)
ssh root@192.168.1.215 "find /var/lib/vz/dump/ -name 'vzdump-*.vma.zst' -mtime +30 -ls"
ssh root@192.168.1.215 "find /var/lib/vz/dump/ -name 'vzdump-*.vma.zst' -mtime +30 -delete -print"
```

## Nettoyage rsync

```bash
# Lister les repertoires rsync
ssh r2d2helm@192.168.1.164 "ls -lth /mnt/nfs/backups/rsync/"

# Supprimer les incrementaux > 7 jours
ssh r2d2helm@192.168.1.164 "find /mnt/nfs/backups/rsync/ -maxdepth 1 -type d -mtime +7 -ls"
```

## Nettoyage Docker Volumes

```bash
# Lister les exports de volumes
ssh {user}@{ip} "ls -lth /mnt/nfs/backups/docker-volumes/"

# Supprimer > 30 jours
ssh {user}@{ip} "find /mnt/nfs/backups/docker-volumes/ -name '*.tar.gz' -mtime +30 -delete -print"
```

## Rapport d'Espace

```bash
# Espace par type de backup
echo "=== Espace Backups ==="
du -sh /mnt/nfs/backups/proxmox/ 2>/dev/null
du -sh /mnt/nfs/backups/postgresql/ 2>/dev/null
du -sh /mnt/nfs/backups/rsync/ 2>/dev/null
du -sh /mnt/nfs/backups/docker-volumes/ 2>/dev/null
echo "--- Total ---"
du -sh /mnt/nfs/backups/
df -h /mnt/nfs/backups/
```

## Precautions

- **Toujours dry-run d'abord** : utiliser `-ls` avant `-delete`
- **Garder les backups mensuels** : ne pas supprimer les 1er du mois
- **Verifier l'espace avant** : `df -h` sur la destination
- **Logger les suppressions** : rediriger vers un fichier de log
