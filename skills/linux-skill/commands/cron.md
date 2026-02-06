# Commande: /lx-cron

Gestion des taches planifiees (cron et systemd timers).

## Syntaxe

```
/lx-cron [action]
```

## Actions

```bash
# Lister les crontabs
crontab -l
sudo crontab -l

# Editer
crontab -e

# Crontabs systeme
ls -la /etc/cron.d/
ls -la /etc/cron.daily/
ls -la /etc/cron.hourly/

# Systemd timers
systemctl list-timers --no-pager

# Status d'un timer
systemctl status <timer>.timer

# Logs d'execution cron
journalctl -u cron -n 20 --no-pager
```

## Format cron

```
# ┌───────────── minute (0-59)
# │ ┌───────────── heure (0-23)
# │ │ ┌───────────── jour du mois (1-31)
# │ │ │ ┌───────────── mois (1-12)
# │ │ │ │ ┌───────────── jour semaine (0-7, 0=7=dimanche)
# │ │ │ │ │
# * * * * * commande

0 2 * * * /usr/local/bin/backup.sh        # Tous les jours a 2h
*/15 * * * * /usr/local/bin/check.sh       # Toutes les 15 min
0 0 * * 0 /usr/local/bin/weekly.sh         # Dimanche minuit
```

## Exemples

```bash
/lx-cron list              # Voir les crontabs
/lx-cron timers            # Systemd timers
/lx-cron add "0 2 * * * /path/script.sh"  # Ajouter
```
