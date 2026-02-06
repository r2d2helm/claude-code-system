# Gestion WSL 2

Administration de Windows Subsystem for Linux.

## Mode d'Utilisation
```
/wsl                        → État général WSL
/wsl list                   → Liste des distributions
/wsl info "distro"          → Détails d'une distribution
/wsl start "distro"         → Démarrer une distribution
/wsl stop "distro"          → Arrêter une distribution
/wsl install                → Installer une nouvelle distribution
/wsl export "distro"        → Exporter/sauvegarder une distribution
/wsl import                 → Importer une distribution
/wsl config                 → Configuration WSL (.wslconfig)
/wsl network                → Configuration réseau WSL
/wsl disk                   → Gestion des disques virtuels
/wsl troubleshoot           → Dépannage WSL
```

Arguments: $ARGUMENTS

---

## État Général (défaut)

```
🐧 WSL 2 - ÉTAT GÉNÉRAL
═══════════════════════════════════════════════════════════════

STATUT WSL:
├─ Version WSL: 2.0.14.0
├─ Version kernel: 5.15.133.1-microsoft-standard-WSL2
├─ Backend: Hyper-V
├─ Virtualisation imbriquée: ✅ Supportée
└─ Systemd: ✅ Supporté

RESSOURCES (depuis .wslconfig):
├─ Mémoire max: 8 GB (50% de 16 GB)
├─ Processeurs: 4 (sur 8)
├─ Swap: 2 GB
└─ Disk VHD max: Dynamique

DISTRIBUTIONS:
┌───────────────────────┬─────────┬──────────┬────────────┬───────────┐
│ Nom                   │ État    │ Version  │ Défaut     │ Disk      │
├───────────────────────┼─────────┼──────────┼────────────┼───────────┤
│ Ubuntu-22.04          │ Running │ WSL 2    │ ⭐ Oui     │ 25 GB     │
│ Debian                │ Stopped │ WSL 2    │            │ 8 GB      │
│ docker-desktop        │ Running │ WSL 2    │            │ 42 GB     │
│ docker-desktop-data   │ Running │ WSL 2    │            │ 65 GB     │
└───────────────────────┴─────────┴──────────┴────────────┴───────────┘

UTILISATION ACTUELLE:
├─ RAM utilisée: 3.2 GB (Ubuntu) + 4.1 GB (Docker)
├─ CPU: 12% moyen
└─ Disk total: 140 GB

ALERTES:
└─ ℹ️ Nouvelle version kernel disponible: 5.15.146.1
```

---

## Mode `list`

```
📋 DISTRIBUTIONS WSL
═══════════════════════════════════════════════════════════════

INSTALLÉES:
┌─────────────────────────────────────────────────────────────────────────┐
│ 🐧 Ubuntu-22.04 ⭐ (défaut)                                            │
├─────────────────────────────────────────────────────────────────────────┤
│ État: ✅ Running                                                        │
│ Version WSL: 2                                                          │
│ Chemin: C:\Users\Jean\AppData\Local\Packages\Canonical...\LocalState   │
│ Taille disque: 25 GB                                                    │
│ Utilisateur par défaut: jean                                           │
│ Systemd: ✅ Activé                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ 🐧 Debian                                                               │
├─────────────────────────────────────────────────────────────────────────┤
│ État: ⏹️ Stopped                                                        │
│ Version WSL: 2                                                          │
│ Chemin: C:\Users\Jean\AppData\Local\Packages\TheDebianProject...       │
│ Taille disque: 8 GB                                                     │
│ Utilisateur par défaut: root                                           │
├─────────────────────────────────────────────────────────────────────────┤
│ 🐳 docker-desktop (système)                                             │
├─────────────────────────────────────────────────────────────────────────┤
│ État: ✅ Running                                                        │
│ Version WSL: 2                                                          │
│ Note: Distribution interne Docker Desktop                               │
└─────────────────────────────────────────────────────────────────────────┘

DISPONIBLES À L'INSTALLATION:
├─ Ubuntu (dernière LTS)
├─ Ubuntu-24.04
├─ Debian
├─ kali-linux
├─ openSUSE-Leap-15.5
├─ SLES-15-SP4
├─ OracleLinux_9_1
└─ AlmaLinux-9

Installer: /wsl install Ubuntu-24.04
```

---

## Mode `info "distro"`

```
📊 DÉTAILS: Ubuntu-22.04
═══════════════════════════════════════════════════════════════

INFORMATIONS SYSTÈME:
├─ OS: Ubuntu 22.04.3 LTS (Jammy Jellyfish)
├─ Kernel: 5.15.133.1-microsoft-standard-WSL2
├─ Architecture: x86_64
├─ Hostname: DESKTOP-ABC123
└─ Utilisateur: jean (uid=1000)

CONFIGURATION:
├─ Version WSL: 2
├─ Distribution par défaut: ✅ Oui
├─ Systemd: ✅ Activé
├─ Interop Windows: ✅ Activé
├─ Automount: ✅ /mnt/c, /mnt/d
└─ Chemin Windows dans PATH: ✅ Oui

STOCKAGE:
├─ VHD: ext4.vhdx
├─ Chemin: C:\Users\Jean\AppData\Local\Packages\...\LocalState
├─ Taille fichier: 25 GB
├─ Taille max: Dynamique (256 GB)
└─ Espace utilisé (dans Linux): 18 GB / 25 GB

UTILISATION RESSOURCES (en cours):
├─ Mémoire: 3.2 GB
├─ CPU: 8% moyen
├─ Processus: 45
└─ Connexions réseau: 12

SERVICES ACTIFS:
├─ systemd: ✅ PID 1
├─ sshd: ✅ Port 22
├─ cron: ✅ Running
└─ snapd: ✅ Running

PAQUETS:
├─ Installés: 1,247
├─ Mise à jour disponibles: 23
└─ Dernière mise à jour: 2026-02-01

CONFIGURATION /etc/wsl.conf:
```ini
[boot]
systemd=true

[interop]
enabled=true
appendWindowsPath=true

[automount]
enabled=true
mountFsTab=true
```
```

---

## Mode `install`

```
📥 INSTALLATION D'UNE DISTRIBUTION
═══════════════════════════════════════════════════════════════

DISTRIBUTIONS DISPONIBLES:
┌───┬─────────────────────┬─────────────────────────────────────┐
│ # │ Nom                 │ Description                         │
├───┼─────────────────────┼─────────────────────────────────────┤
│ 1 │ Ubuntu              │ Ubuntu (dernière LTS) - Recommandé  │
│ 2 │ Ubuntu-24.04        │ Ubuntu 24.04 LTS                    │
│ 3 │ Ubuntu-22.04        │ Ubuntu 22.04 LTS                    │
│ 4 │ Debian              │ Debian GNU/Linux                    │
│ 5 │ kali-linux          │ Kali Linux (pentesting)             │
│ 6 │ openSUSE-Leap-15.5  │ openSUSE Leap 15.5                  │
│ 7 │ OracleLinux_9_1     │ Oracle Linux 9.1                    │
│ 8 │ AlmaLinux-9         │ AlmaLinux 9                         │
└───┴─────────────────────┴─────────────────────────────────────┘

Choix (numéro ou nom): _

OPTIONS D'INSTALLATION:
├─ Emplacement: Défaut (AppData) ou personnalisé
├─ Utilisateur: Sera créé au premier lancement
└─ Version WSL: 2 (recommandé)

Commande: wsl --install -d <distribution>
```

---

## Mode `export/import`

```
📤 EXPORT: Ubuntu-22.04
═══════════════════════════════════════════════════════════════

Cette opération va créer une archive tar de la distribution.

Destination: _____
(ex: D:\Backups\ubuntu-22.04-backup.tar)

Taille estimée: ~20 GB (compressé)
Durée estimée: 5-15 minutes

⚠️ La distribution sera brièvement arrêtée pendant l'export.

Exporter? [O/N]

---

📥 IMPORT
═══════════════════════════════════════════════════════════════

Fichier source: _____
(ex: D:\Backups\ubuntu-22.04-backup.tar)

Nom de la distribution: _____
Emplacement d'installation: _____
(ex: D:\WSL\Ubuntu-Import)

Version WSL: [1] | [2] (recommandé)

Commande: wsl --import <nom> <emplacement> <fichier.tar> --version 2
```

---

## Mode `config`

```
⚙️ CONFIGURATION WSL (.wslconfig)
═══════════════════════════════════════════════════════════════

Fichier: C:\Users\Jean\.wslconfig

CONFIGURATION ACTUELLE:
```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
localhostForwarding=true
kernelCommandLine=
nestedVirtualization=true

[experimental]
autoMemoryReclaim=gradual
sparseVhd=true
```

PARAMÈTRES DISPONIBLES:

[wsl2]
├─ memory          : RAM max (ex: 8GB, 50%)
├─ processors      : Nombre de CPU (ex: 4)
├─ swap            : Taille swap (ex: 2GB, 0 pour désactiver)
├─ swapFile        : Chemin fichier swap
├─ localhostForwarding : Accès localhost depuis Windows
├─ kernelCommandLine : Options kernel
├─ kernel          : Kernel personnalisé
├─ nestedVirtualization : VM dans WSL
└─ pageReporting   : Libération mémoire inutilisée

[experimental]
├─ autoMemoryReclaim : gradual, dropcache, disabled
├─ sparseVhd       : VHD creux (économise espace)
├─ networkingMode  : NAT, mirrored
└─ dnsTunneling    : DNS via Windows

MODIFIER:
1. Éditer memory (RAM)
2. Éditer processors (CPU)
3. Activer/désactiver swap
4. Configurer réseau
5. Ouvrir le fichier dans éditeur

Choix: _

⚠️ Redémarrage WSL requis après modification: wsl --shutdown
```

---

## Mode `network`

```
🌐 RÉSEAU WSL
═══════════════════════════════════════════════════════════════

MODE RÉSEAU ACTUEL: NAT (défaut)

CONFIGURATION:
├─ IP WSL (vEthernet): 172.25.160.1
├─ IP Distribution: 172.25.163.45
├─ DNS: Hérité de Windows
├─ localhost forwarding: ✅ Activé
└─ Ports exposés: Accessibles via localhost Windows

INTERFACES (dans Ubuntu):
```
eth0: 172.25.163.45/20
      gateway: 172.25.160.1
      dns: 172.25.160.1
```

PORTS EN ÉCOUTE (WSL):
┌────────┬─────────────────┬──────────────────┐
│ Port   │ Service         │ Accès Windows    │
├────────┼─────────────────┼──────────────────┤
│ 22     │ sshd            │ localhost:22     │
│ 3000   │ node (dev)      │ localhost:3000   │
│ 5432   │ postgresql      │ localhost:5432   │
└────────┴─────────────────┴──────────────────┘

OPTIONS:
1. Passer en mode "mirrored" (même IP que Windows)
2. Configurer port forwarding manuel
3. Configurer DNS personnalisé
4. Résoudre problèmes de connectivité
```

---

## Mode `disk`

```
💾 GESTION DISQUES WSL
═══════════════════════════════════════════════════════════════

DISQUES VIRTUELS (VHDX):
┌─────────────────────┬────────────────────────────────┬──────────┐
│ Distribution        │ Fichier                        │ Taille   │
├─────────────────────┼────────────────────────────────┼──────────┤
│ Ubuntu-22.04        │ ext4.vhdx                      │ 25 GB    │
│ Debian              │ ext4.vhdx                      │ 8 GB     │
│ docker-desktop-data │ data/ext4.vhdx                 │ 65 GB    │
└─────────────────────┴────────────────────────────────┴──────────┘

Total: 98 GB

ACTIONS:
1. [compact] Compacter un VHD (récupérer espace)
   ├─ Ubuntu-22.04: ~5 GB récupérables
   └─ docker-desktop-data: ~15 GB récupérables

2. [resize] Redimensionner un VHD
   └─ Augmenter la taille max (défaut: 256 GB)

3. [move] Déplacer un VHD vers un autre disque
   └─ Utile si C: manque d'espace

COMPACTAGE Ubuntu-22.04:
```powershell
# 1. Arrêter WSL
wsl --shutdown

# 2. Lancer diskpart
diskpart
select vdisk file="C:\...\ext4.vhdx"
compact vdisk
detach vdisk
exit
```

⚠️ Sauvegarder avant toute opération sur les VHD
```

---

## Mode `troubleshoot`

```
🔧 DÉPANNAGE WSL
═══════════════════════════════════════════════════════════════

DIAGNOSTIC EN COURS...

PRÉREQUIS SYSTÈME:
├─ Windows 10 version: ✅ 22H2 (19045)
├─ Fonctionnalité WSL: ✅ Activée
├─ Fonctionnalité VM Platform: ✅ Activée
├─ Hyper-V: ✅ Disponible
└─ Virtualisation BIOS: ✅ Activée

COMPOSANTS WSL:
├─ wsl.exe: ✅ Présent
├─ Kernel WSL: ✅ 5.15.133.1
├─ WSLg (GUI): ✅ Installé
└─ Service LxssManager: ✅ Running

RÉSEAU:
├─ vEthernet (WSL): ✅ OK
├─ NAT: ✅ Fonctionnel
├─ DNS: ✅ Résolution OK
└─ Internet depuis WSL: ✅ OK

PROBLÈMES COURANTS:

1. "WSL 2 requires an update to its kernel"
   → wsl --update

2. "Cannot access Windows files from WSL"
   → Vérifier /etc/wsl.conf [automount]
   → ls /mnt/c devrait fonctionner

3. "Network unreachable"
   → wsl --shutdown puis relancer
   → Vérifier pare-feu Windows

4. "Out of memory"
   → Configurer .wslconfig [memory]
   → Réduire consommation ou augmenter RAM

5. "Disk full" mais espace disponible
   → Compacter le VHD: /wsl disk compact

6. WSL très lent
   → Éviter d'accéder /mnt/c depuis WSL
   → Travailler dans le filesystem Linux

RÉSULTAT: ✅ Aucun problème détecté
```

---

## Commandes de Référence

```powershell
# Liste des distributions
wsl --list --verbose

# Démarrer/arrêter
wsl -d Ubuntu-22.04
wsl --terminate Ubuntu-22.04
wsl --shutdown

# Installer
wsl --install -d Ubuntu-24.04

# Définir par défaut
wsl --set-default Ubuntu-22.04

# Export/Import
wsl --export Ubuntu-22.04 D:\backup.tar
wsl --import NewUbuntu D:\WSL\NewUbuntu D:\backup.tar

# Mise à jour
wsl --update

# Version WSL
wsl --set-version Ubuntu-22.04 2

# Accéder aux fichiers
explorer.exe \\wsl$\Ubuntu-22.04\home\user

# Exécuter commande
wsl -d Ubuntu-22.04 -- ls -la /home
```
