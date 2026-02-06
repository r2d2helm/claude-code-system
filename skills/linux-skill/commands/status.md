# Commande: /lx-status

Vue d'ensemble du systeme Linux.

## Syntaxe

```
/lx-status [options]
```

## Comportement

Affiche un dashboard systeme complet :

```bash
# Hostname et OS
hostnamectl

# Uptime et load
uptime

# Kernel
uname -r

# CPU
nproc
lscpu | grep "Model name"

# Memoire
free -h

# Swap
swapon --show

# Disque
df -h --type=ext4 --type=xfs --type=btrfs

# Top 5 processus CPU
ps aux --sort=-%cpu | head -6

# Top 5 processus memoire
ps aux --sort=-%mem | head -6

# Connexions reseau
ss -tuln | head -20

# Services en echec
systemctl --failed --no-pager
```

## Options

| Option | Description |
|--------|-------------|
| `--quick` | Seulement uptime, load, memoire |
| `--full` | Inclure reseau et services |

## Exemples

```bash
/lx-status              # Dashboard complet
/lx-status --quick      # Vue rapide
```
