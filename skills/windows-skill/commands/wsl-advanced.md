# Gestion WSL 2 - Avancé

Voir aussi: [[wsl]]

Configuration, réseau, disques virtuels et dépannage WSL.

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

## Commandes de Référence (Avancé)

```powershell
# Accéder aux fichiers
explorer.exe \\wsl$\Ubuntu-22.04\home\user
```
