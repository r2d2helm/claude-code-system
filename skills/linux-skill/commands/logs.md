# Commande: /lx-logs

Analyse des logs systeme via journalctl.

## Syntaxe

```
/lx-logs [service|filter] [options]
```

## Actions

```bash
# Logs recents
journalctl -n 50 --no-pager

# Logs d'un service
journalctl -u <service> -n 50 --no-pager

# Erreurs seulement
journalctl -p err -n 50 --no-pager

# Depuis une date
journalctl --since "2026-02-06 10:00" --no-pager

# Logs du boot actuel
journalctl -b --no-pager

# Suivre en temps reel
journalctl -f

# Logs kernel
journalctl -k --no-pager

# Espace utilise par les logs
journalctl --disk-usage

# Nettoyer les vieux logs
sudo journalctl --vacuum-time=7d
sudo journalctl --vacuum-size=500M
```

## Options

| Option | Description |
|--------|-------------|
| `-u service` | Filtrer par service |
| `-p priority` | err, warning, info, debug |
| `-n N` | Dernières N lignes |
| `--since` | Depuis une date |
| `-f` | Suivre en temps reel |
| `-b` | Boot actuel seulement |

## Exemples

```bash
/lx-logs                       # 50 derniers logs
/lx-logs nginx                 # Logs nginx
/lx-logs errors                # Erreurs seulement
/lx-logs --since "1 hour ago"  # Derniere heure
```
