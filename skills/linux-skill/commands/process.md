# Commande: /lx-process

Gestion des processus.

## Syntaxe

```
/lx-process [action] [pid|name]
```

## Actions

```bash
# Top processus CPU
ps aux --sort=-%cpu | head -15

# Top processus memoire
ps aux --sort=-%mem | head -15

# Chercher un processus
ps aux | grep <name>
pgrep -la <name>

# Arbre des processus
pstree -p

# Tuer un processus
kill <pid>
kill -9 <pid>        # Force kill
killall <name>

# Zombies
ps aux | awk '$8=="Z" {print}'

# Processus d'un utilisateur
ps -u <username>

# Informations detaillees
ls -la /proc/<pid>/fd 2>/dev/null | wc -l    # File descriptors
cat /proc/<pid>/status                        # Status detaille
```

## Exemples

```bash
/lx-process top cpu        # Top CPU
/lx-process top mem        # Top memoire
/lx-process kill 1234      # Tuer PID 1234
/lx-process zombies        # Detecter zombies
```
