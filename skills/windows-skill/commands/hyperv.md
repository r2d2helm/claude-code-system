# Gestion Hyper-V

Administration des machines virtuelles Hyper-V.

## Mode d'Utilisation
```
/hyperv                     → État général et liste des VMs
/hyperv list                → Liste détaillée des VMs
/hyperv info "NomVM"        → Détails d'une VM
/hyperv start "NomVM"       → Démarrer une VM
/hyperv stop "NomVM"        → Arrêter une VM (graceful)
/hyperv snapshot "NomVM"    → Gérer les snapshots
/hyperv create              → Assistant création de VM
/hyperv network             → Configuration réseau virtuel
/hyperv storage             → Gestion des disques virtuels
/hyperv performance         → Métriques de performance
```

Arguments: $ARGUMENTS

---

## État Général (défaut)

```
🖥️ HYPER-V - ÉTAT GÉNÉRAL
═══════════════════════════════════════════════════════════════

STATUT HYPER-V:
├─ Service vmms: ✅ Running
├─ Service vmcompute: ✅ Running
├─ Version: 10.0.19041.1
└─ Virtualisation imbriquée: ✅ Supportée

RESSOURCES HÔTE:
├─ CPU disponible: 16 threads (8 alloués aux VMs)
├─ RAM totale: 32 GB
├─ RAM allouée VMs: 12 GB (8 GB en cours d'utilisation)
└─ Stockage VMs: 245 GB utilisés sur 500 GB

MACHINES VIRTUELLES:
┌─────────────────────┬───────────┬───────┬────────┬─────────────┐
│ Nom                 │ État      │ CPU   │ RAM    │ Uptime      │
├─────────────────────┼───────────┼───────┼────────┼─────────────┤
│ Ubuntu-Server       │ ✅ Running│ 4     │ 4 GB   │ 5j 12h      │
│ Windows-Dev         │ ✅ Running│ 4     │ 8 GB   │ 2h 34m      │
│ Docker-Host         │ ⏸️ Paused │ 2     │ 2 GB   │ -           │
│ Test-Environment    │ ⏹️ Off    │ 2     │ 2 GB   │ -           │
└─────────────────────┴───────────┴───────┴────────┴─────────────┘

Total: 4 VMs (2 running, 1 paused, 1 off)

ALERTES:
└─ ⚠️ Docker-Host en pause depuis 2 jours

Actions rapides: /hyperv start "Test-Environment" | /hyperv info "Ubuntu-Server"
```

---

## Mode `list`

```
📋 LISTE DÉTAILLÉE DES MACHINES VIRTUELLES
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🖥️ Ubuntu-Server                                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ État: ✅ Running                │ Génération: 2                             │
│ vCPU: 4                         │ RAM: 4096 MB (dynamique: 2-8 GB)          │
│ Uptime: 5 jours, 12 heures      │ Checkpoints: 2                            │
│ Réseau: External-Switch         │ IP: 192.168.1.50                          │
│ Disque: Ubuntu-Server.vhdx      │ Taille: 45 GB / 127 GB                    │
│ OS invité: Ubuntu 22.04 LTS     │ Integration Services: ✅                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🖥️ Windows-Dev                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ État: ✅ Running                │ Génération: 2                             │
│ vCPU: 4                         │ RAM: 8192 MB (statique)                   │
│ Uptime: 2 heures, 34 minutes    │ Checkpoints: 5                            │
│ Réseau: External-Switch         │ IP: 192.168.1.51                          │
│ Disque: Windows-Dev.vhdx        │ Taille: 120 GB / 256 GB                   │
│ OS invité: Windows 11 Pro       │ Integration Services: ✅                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🖥️ Docker-Host                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ État: ⏸️ Paused                 │ Génération: 2                             │
│ vCPU: 2                         │ RAM: 2048 MB (dynamique: 1-4 GB)          │
│ Pausé depuis: 2026-02-01 14:30  │ Checkpoints: 1                            │
│ Réseau: Internal-Switch         │ IP: 172.16.0.10                           │
│ Disque: Docker-Host.vhdx        │ Taille: 30 GB / 64 GB                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Mode `info "NomVM"`

```
📊 DÉTAILS: Ubuntu-Server
═══════════════════════════════════════════════════════════════

CONFIGURATION MATÉRIELLE:
├─ Génération: 2 (UEFI)
├─ Processeurs virtuels: 4
├─ Réservation CPU: 10%
├─ Limite CPU: 100%
├─ Poids relatif: 100
├─ Mémoire RAM: 4096 MB
│  ├─ Type: Dynamique
│  ├─ Minimum: 2048 MB
│  ├─ Maximum: 8192 MB
│  └─ Buffer: 20%
├─ Secure Boot: ✅ Activé (Microsoft UEFI CA)
└─ TPM virtuel: ❌ Non configuré

STOCKAGE:
├─ Contrôleur SCSI 0:
│  └─ Disque 0: Ubuntu-Server.vhdx
│     ├─ Chemin: D:\Hyper-V\Virtual Hard Disks\
│     ├─ Format: VHDX (dynamique)
│     ├─ Taille actuelle: 45 GB
│     ├─ Taille maximum: 127 GB
│     └─ Fragmentation: 3%
└─ Lecteur DVD: Ubuntu-22.04-LTS.iso (déconnecté)

RÉSEAU:
├─ Adaptateur 1: External-Switch
│  ├─ MAC: 00-15-5D-XX-XX-XX
│  ├─ VLAN: Aucun
│  ├─ Bande passante: Non limitée
│  └─ IP détectée: 192.168.1.50

CHECKPOINTS (Snapshots):
├─ 📸 "Avant mise à jour" - 2026-01-28 10:00 (2.3 GB)
└─ 📸 "Configuration stable" - 2026-01-15 14:30 (1.8 GB)

SERVICES D'INTÉGRATION:
├─ Heartbeat: ✅ OK
├─ Échange de clés: ✅ OK  
├─ Arrêt système: ✅ OK
├─ Synchronisation horaire: ✅ OK
├─ VSS (sauvegarde): ✅ OK
└─ Services invité: ✅ Connecté

PERFORMANCE (temps réel):
├─ CPU VM: 12%
├─ RAM utilisée: 2.8 GB / 4 GB
├─ IOPS disque: 45 read, 12 write
└─ Réseau: 1.2 Mbps in, 0.5 Mbps out

HISTORIQUE:
├─ Créée le: 2025-06-15
├─ Dernière modification config: 2026-01-28
└─ Temps d'exécution total: 892 heures
```

---

## Mode `start/stop "NomVM"`

```
▶️ DÉMARRAGE: Test-Environment
═══════════════════════════════════════════════════════════════

Vérifications préalables:
├─ Ressources CPU disponibles: ✅ 2 vCPU demandés, 6 disponibles
├─ RAM disponible: ✅ 2 GB demandés, 12 GB disponibles
├─ Disque virtuel accessible: ✅
├─ Switch réseau disponible: ✅
└─ Aucun conflit détecté: ✅

Démarrer la VM "Test-Environment"? [O/N]

---

⏹️ ARRÊT: Ubuntu-Server
═══════════════════════════════════════════════════════════════

Type d'arrêt:
1. [shutdown] Arrêt gracieux (via OS invité) - Recommandé
2. [turnoff]  Arrêt forcé (coupure alimentation)
3. [save]     Sauvegarder l'état (hibernation)
4. [pause]    Mettre en pause (garde en mémoire)

⚠️ Services dépendants:
├─ Cette VM héberge un serveur web
└─ 2 connexions SSH actives détectées

Choix: _
```

---

## Mode `snapshot "NomVM"`

```
📸 GESTION DES CHECKPOINTS: Windows-Dev
═══════════════════════════════════════════════════════════════

CHECKPOINTS EXISTANTS:
┌───┬─────────────────────────────┬──────────────────┬─────────┐
│ # │ Nom                         │ Date             │ Taille  │
├───┼─────────────────────────────┼──────────────────┼─────────┤
│ 1 │ 🌟 Configuration initiale   │ 2025-12-01 09:00 │ 2.1 GB  │
│ 2 │ ├─ Après install VS2022     │ 2025-12-15 14:30 │ 3.4 GB  │
│ 3 │ │  └─ Tests terminés        │ 2026-01-10 11:00 │ 1.2 GB  │
│ 4 │ └─ Branche expérimentale    │ 2026-01-20 16:45 │ 2.8 GB  │
│ 5 │    └─ ⭐ ACTUEL             │ (état courant)   │ -       │
└───┴─────────────────────────────┴──────────────────┴─────────┘

Espace total checkpoints: 9.5 GB

ACTIONS:
1. [create]  Créer un nouveau checkpoint
2. [apply]   Restaurer un checkpoint (⚠️ perte état actuel)
3. [rename]  Renommer un checkpoint
4. [delete]  Supprimer un checkpoint
5. [export]  Exporter un checkpoint

Choix: _
```

---

## Mode `create`

```
🆕 ASSISTANT CRÉATION DE VM
═══════════════════════════════════════════════════════════════

ÉTAPE 1/6 - INFORMATIONS GÉNÉRALES
├─ Nom de la VM: _____
├─ Emplacement: D:\Hyper-V\ (défaut) ou personnalisé
└─ Génération: [1] Legacy BIOS | [2] UEFI (recommandé)

ÉTAPE 2/6 - MÉMOIRE
├─ RAM de démarrage: _____ MB (recommandé: 2048-4096)
├─ Mémoire dynamique: [O/N]
│  ├─ Minimum: _____ MB
│  └─ Maximum: _____ MB

ÉTAPE 3/6 - RÉSEAU
├─ Connecter à un switch: 
│  [1] External-Switch (accès réseau physique)
│  [2] Internal-Switch (hôte + VMs uniquement)
│  [3] Private-Switch (VMs uniquement)
│  [4] Default Switch (NAT automatique)
│  [5] Non connecté

ÉTAPE 4/6 - STOCKAGE
├─ Créer un disque virtuel:
│  ├─ Taille: _____ GB
│  └─ Type: [Dynamique] | Fixe
├─ Ou attacher un disque existant

ÉTAPE 5/6 - INSTALLATION
├─ Source d'installation:
│  [1] Fichier ISO: _____
│  [2] Réseau (PXE)
│  [3] Installer plus tard

ÉTAPE 6/6 - PROCESSEURS
├─ Nombre de processeurs virtuels: _____ (1-16)

═══════════════════════════════════════════════════════════════
RÉSUMÉ:
├─ Nom: Ubuntu-Test | Génération: 2
├─ RAM: 4 GB (dynamique) | vCPU: 4
├─ Réseau: External-Switch
└─ Disque: 64 GB dynamique

Créer cette VM? [O/N]
```

---

## Mode `network`

```
🌐 CONFIGURATION RÉSEAU HYPER-V
═══════════════════════════════════════════════════════════════

SWITCHES VIRTUELS:
┌───────────────────────┬──────────────┬─────────────────────────┬─────────┐
│ Nom                   │ Type         │ Connexion               │ VMs     │
├───────────────────────┼──────────────┼─────────────────────────┼─────────┤
│ External-Switch       │ External     │ Intel I219-LM           │ 3       │
│ Internal-Switch       │ Internal     │ vEthernet (172.16.0.1)  │ 1       │
│ Private-Switch        │ Private      │ Isolé                   │ 0       │
│ Default Switch        │ Internal     │ NAT (172.17.x.x)        │ 0       │
└───────────────────────┴──────────────┴─────────────────────────┴─────────┘

ACTIONS:
1. Créer un nouveau switch virtuel
2. Modifier un switch existant
3. Supprimer un switch
4. Configurer NAT
```

---

## Mode `performance`

```
📈 PERFORMANCE HYPER-V
═══════════════════════════════════════════════════════════════

UTILISATION GLOBALE:
┌─────────────────────────────────────────────────────────────┐
│ CPU Hôte: ████████████░░░░░░░░ 58%                         │
│ ├─ Hyperviseur: 2% | VMs: 45% | Hôte: 11%                  │
│                                                             │
│ RAM: ████████████████░░░░ 78% (25/32 GB)                   │
│ ├─ VMs allouée: 14 GB | VMs utilisée: 11 GB                │
└─────────────────────────────────────────────────────────────┘

PAR VM:
┌─────────────────────┬────────┬────────────┬─────────┬─────────┐
│ VM                  │ CPU %  │ RAM        │ Disk IO │ Net IO  │
├─────────────────────┼────────┼────────────┼─────────┼─────────┤
│ Ubuntu-Server       │ 12%    │ 2.8/4 GB   │ 45 IOPS │ 1.2 Mbps│
│ Windows-Dev         │ 28%    │ 6.2/8 GB   │ 120 IOPS│ 0.8 Mbps│
└─────────────────────┴────────┴────────────┴─────────┴─────────┘
```

---

## Commandes de Référence

```powershell
# Lister les VMs
Get-VM | Select-Object Name, State, CPUUsage, MemoryAssigned, Uptime

# Démarrer/Arrêter
Start-VM -Name "NomVM"
Stop-VM -Name "NomVM" -Force

# Créer un checkpoint
Checkpoint-VM -Name "NomVM" -SnapshotName "Mon snapshot"

# Restaurer un checkpoint
Restore-VMCheckpoint -Name "Mon snapshot" -VMName "NomVM" -Confirm:$false

# Créer une VM
New-VM -Name "NouvelleVM" -MemoryStartupBytes 4GB -Generation 2 -NewVHDPath "C:\VM\disk.vhdx" -NewVHDSizeBytes 64GB

# Configuration réseau
Get-VMSwitch
New-VMSwitch -Name "MonSwitch" -SwitchType Internal

# Métriques
Measure-VM -Name "NomVM"
```
