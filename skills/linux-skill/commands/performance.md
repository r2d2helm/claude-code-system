# Commande: /lx-performance

Analyse de performance systeme.

## Syntaxe

```
/lx-performance [focus]
```

## Actions

```bash
# === Vue d'ensemble ===
uptime
free -h
vmstat 1 5

# === CPU ===
mpstat 1 5 2>/dev/null
top -bn1 | head -20

# === Memoire ===
free -h
vmstat -s | head -10

# === Disque I/O ===
iostat -x 1 3 2>/dev/null
iotop -bon1 2>/dev/null | head -15

# === Reseau ===
ss -s
sar -n DEV 1 3 2>/dev/null

# === Load history ===
sar -q 2>/dev/null | tail -20

# === Goulots d'etranglement ===
# CPU: load average > nb cores = bottleneck CPU
# Memory: swap used > 0 = bottleneck RAM
# Disk: await > 10ms = bottleneck I/O
# Network: retransmits > 0 = bottleneck reseau
```

## Outils recommandes

```bash
# Installer les outils de perf
sudo apt install -y sysstat htop iotop nmon

# htop (vue interactive)
htop

# nmon (monitoring complet)
nmon
```

## Exemples

```bash
/lx-performance            # Analyse complete
/lx-performance cpu        # Focus CPU
/lx-performance io         # Focus disque I/O
/lx-performance bottleneck # Detecter goulots
```
