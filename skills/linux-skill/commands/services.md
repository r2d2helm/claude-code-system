# Commande: /lx-services

Gestion des services systemd.

## Syntaxe

```
/lx-services [action] [service]
```

## Actions

```bash
# Lister les services actifs
systemctl list-units --type=service --state=running --no-pager

# Status d'un service
systemctl status <service>

# Demarrer / Arreter / Redemarrer
sudo systemctl start <service>
sudo systemctl stop <service>
sudo systemctl restart <service>
sudo systemctl reload <service>

# Activer / Desactiver au boot
sudo systemctl enable <service>
sudo systemctl disable <service>

# Services en echec
systemctl --failed --no-pager

# Logs d'un service
journalctl -u <service> -n 50 --no-pager

# Dependances
systemctl list-dependencies <service>
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister tous les services |
| `failed` | Services en echec |
| `--all` | Inclure services inactifs |

## Exemples

```bash
/lx-services list              # Tous les services actifs
/lx-services status nginx      # Status de nginx
/lx-services restart postgresql # Redemarrer postgres
/lx-services failed            # Services en echec
```
