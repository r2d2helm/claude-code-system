# Gestion des Pilotes

Administration des pilotes de périphériques Windows.

## Mode d'Utilisation
```
/drivers                    → Vue d'ensemble des pilotes
/drivers list               → Liste complète
/drivers info "nom"         → Détails d'un pilote
/drivers problems           → Pilotes problématiques
/drivers update             → Vérifier les mises à jour
/drivers backup             → Sauvegarder les pilotes
/drivers rollback "nom"     → Restaurer version précédente
/drivers export             → Exporter pilotes tiers
```

Arguments: $ARGUMENTS

---

## Vue d'Ensemble (défaut)

```
🔌 PILOTES - VUE D'ENSEMBLE
═══════════════════════════════════════════════════════════════

STATISTIQUES:
├─ Pilotes chargés: 245
├─ Pilotes tiers: 34
├─ Mises à jour disponibles: 3
└─ Problèmes détectés: 1

PÉRIPHÉRIQUES PAR CATÉGORIE:
┌─────────────────────────────┬────────┬─────────┬──────────────┐
│ Catégorie                   │ Total  │ Actifs  │ Problèmes    │
├─────────────────────────────┼────────┼─────────┼──────────────┤
│ Cartes graphiques           │ 2      │ 2       │ ✅           │
│ Cartes réseau               │ 3      │ 3       │ ✅           │
│ Contrôleurs de stockage     │ 4      │ 4       │ ✅           │
│ Contrôleurs audio           │ 3      │ 3       │ ✅           │
│ Contrôleurs USB             │ 8      │ 8       │ ✅           │
│ Périphériques d'entrée      │ 5      │ 5       │ ✅           │
│ Périphériques Bluetooth     │ 2      │ 1       │ ⚠️ 1 prob.   │
└─────────────────────────────┴────────┴─────────┴──────────────┘

PROBLÈMES DÉTECTÉS:
├─ ⚠️ Intel Wireless Bluetooth - Code 10 (démarrage impossible)
└─ Action: /drivers problems

PILOTES RÉCEMMENT MIS À JOUR:
├─ NVIDIA GeForce RTX 3080 - 546.33 (2026-01-28)
├─ Intel I219-LM - 12.19.2.40 (2026-01-15)
└─ Realtek Audio - 6.0.9456.1 (2026-01-10)
```

---

## Mode `list`

```
📋 LISTE DES PILOTES
═══════════════════════════════════════════════════════════════

FILTRE: $ARGUMENTS
Options: all, third-party, microsoft, "catégorie"

PILOTES TIERS (non-Microsoft):
┌────────────────────────────────────┬─────────────────┬────────────┐
│ Pilote                             │ Version         │ Date       │
├────────────────────────────────────┼─────────────────┼────────────┤
│ NVIDIA GeForce RTX 3080            │ 546.33          │ 2026-01-28 │
│ NVIDIA High Definition Audio       │ 1.3.40.4        │ 2026-01-28 │
│ Intel I219-LM Ethernet             │ 12.19.2.40      │ 2026-01-15 │
│ Intel Wireless-AC 9560             │ 22.230.0.7      │ 2025-12-10 │
│ Intel Wireless Bluetooth           │ 23.20.0.3       │ 2025-11-05 │
│ Realtek High Definition Audio      │ 6.0.9456.1      │ 2026-01-10 │
│ Samsung NVMe SSD Controller        │ 3.3.0.2003      │ 2025-10-20 │
│ Logitech USB Receiver              │ 6.80.39.0       │ 2025-08-15 │
└────────────────────────────────────┴─────────────────┴────────────┘

PAR CATÉGORIE:

📺 Cartes graphiques:
├─ NVIDIA GeForce RTX 3080 (546.33)
└─ Microsoft Basic Display Adapter (intégré)

🌐 Cartes réseau:
├─ Intel I219-LM Gigabit (12.19.2.40)
├─ Intel Wireless-AC 9560 (22.230.0.7)
└─ Hyper-V Virtual Ethernet Adapter

💾 Stockage:
├─ Samsung NVMe SSD Controller 980 PRO
├─ Standard SATA AHCI Controller
└─ Microsoft Storage Spaces Controller

Total: 245 pilotes (34 tiers, 211 Microsoft)
```

---

## Mode `problems`

```
⚠️ PILOTES PROBLÉMATIQUES
═══════════════════════════════════════════════════════════════

PROBLÈMES ACTUELS:
┌──────────────────────────────────────────────────────────────────────────┐
│ 🔴 Intel Wireless Bluetooth                                             │
├──────────────────────────────────────────────────────────────────────────┤
│ État: ❌ Code d'erreur 10                                               │
│ Message: Ce périphérique ne peut pas démarrer                           │
│ Périphérique: Intel(R) Wireless Bluetooth(R)                            │
│ ID: USB\VID_8087&PID_0AAA                                               │
│ Pilote actuel: 23.20.0.3 (2025-11-05)                                   │
│                                                                          │
│ DIAGNOSTIC:                                                              │
│ ├─ Pilote installé: ✅                                                   │
│ ├─ Fichiers présents: ✅                                                 │
│ ├─ Service: ❌ Ne démarre pas                                           │
│ └─ Événements: Erreur timeout au démarrage                              │
│                                                                          │
│ SOLUTIONS SUGGÉRÉES:                                                     │
│ 1. Redémarrer le périphérique                                           │
│ 2. Mettre à jour le pilote                                              │
│ 3. Restaurer le pilote précédent                                        │
│ 4. Réinstaller le pilote                                                │
│ 5. Désactiver la gestion d'alimentation USB                             │
└──────────────────────────────────────────────────────────────────────────┘

CODES D'ERREUR FRÉQUENTS:
├─ Code 10: Périphérique ne peut pas démarrer
├─ Code 28: Pilotes non installés
├─ Code 31: Périphérique ne fonctionne pas correctement
├─ Code 43: Windows a arrêté ce périphérique (problème signalé)
└─ Code 52: Windows ne peut pas vérifier la signature

HISTORIQUE DES PROBLÈMES (30 jours):
├─ 3 occurrences: Intel Bluetooth Code 10
└─ 1 occurrence: USB composite device Code 43 (résolu)

Action: _
```

---

## Mode `update`

```
🔄 MISES À JOUR DE PILOTES
═══════════════════════════════════════════════════════════════

RECHERCHE EN COURS...

MISES À JOUR DISPONIBLES:
┌────────────────────────────────────┬─────────────┬─────────────┬──────────┐
│ Pilote                             │ Actuel      │ Disponible  │ Source   │
├────────────────────────────────────┼─────────────┼─────────────┼──────────┤
│ Intel Wireless Bluetooth           │ 23.20.0.3   │ 23.40.0.1   │ WU       │
│ Realtek HD Audio                   │ 6.0.9456.1  │ 6.0.9512.1  │ WU       │
│ Intel WiFi 6 AX201                 │ 22.230.0.7  │ 23.10.0.5   │ WU       │
└────────────────────────────────────┴─────────────┴─────────────┴──────────┘

PILOTES À JOUR:
├─ NVIDIA GeForce RTX 3080 - 546.33 (dernière version)
├─ Intel I219-LM - 12.19.2.40 (dernière version)
└─ Samsung NVMe - 3.3.0.2003 (dernière version)

OPTIONS:
1. [all] Installer toutes les mises à jour
2. [select] Sélectionner les mises à jour
3. [bluetooth] Intel Bluetooth uniquement (recommandé - corrige Code 10)

⚠️ Recommandation: Créer un point de restauration avant

Choix: _
```

---

## Mode `backup`

```
💾 SAUVEGARDE DES PILOTES
═══════════════════════════════════════════════════════════════

OPTIONS:
1. [third-party] Pilotes tiers uniquement (recommandé)
   ├─ 34 pilotes
   └─ Taille estimée: ~450 MB

2. [all] Tous les pilotes
   ├─ 245 pilotes
   └─ Taille estimée: ~2.5 GB

3. [category] Par catégorie
   └─ Sélectionner: Graphics, Network, Audio, Storage, etc.

Destination: C:\Backups\Drivers\2026-02-03\

---

SAUVEGARDE EN COURS (tiers)...
├─ NVIDIA GeForce... ✅
├─ Intel I219-LM... ✅
├─ Intel Wireless... ✅
├─ Realtek Audio... ✅
└─ (30 autres)... ✅

✅ Sauvegarde terminée!
├─ Pilotes: 34
├─ Taille: 423 MB
└─ Chemin: C:\Backups\Drivers\2026-02-03\

Restauration: pnputil /add-driver "C:\Backups\...\*.inf" /install
```

---

## Mode `info "nom"`

```
📊 DÉTAILS: NVIDIA GeForce RTX 3080
═══════════════════════════════════════════════════════════════

INFORMATIONS GÉNÉRALES:
├─ Nom: NVIDIA GeForce RTX 3080
├─ Fabricant: NVIDIA
├─ Classe: Display adapters
├─ État: ✅ Fonctionnel

PILOTE:
├─ Version: 546.33
├─ Date: 2026-01-28
├─ Signé: ✅ NVIDIA Corporation (WHQL)
├─ Fichier INF: nv_dispi.inf
└─ Fichiers: 156 (1.2 GB)

PÉRIPHÉRIQUE:
├─ ID: PCI\VEN_10DE&DEV_2206&SUBSYS_...
├─ Emplacement: PCI bus 1, device 0
├─ IRQ: Message Signaled
└─ Ressources mémoire: E0000000-EFFFFFFF

VERSIONS PRÉCÉDENTES (rollback disponible):
├─ 545.92 (2025-12-15) ⬅️ Peut restaurer
├─ 545.84 (2025-11-20)
└─ 537.58 (2025-09-10)

ÉVÉNEMENTS RÉCENTS:
├─ 2026-01-28: Pilote mis à jour vers 546.33
├─ 2025-12-15: Pilote mis à jour vers 545.92
└─ Aucune erreur enregistrée

Actions: [update] [rollback] [reinstall] [properties]
```

---

## Commandes de Référence

```powershell
# Lister les pilotes
Get-WmiObject Win32_PnPSignedDriver | Select-Object DeviceName, DriverVersion, Manufacturer

# Pilotes tiers
Get-WindowsDriver -Online | Where-Object {$_.ProviderName -ne "Microsoft"}

# Périphériques avec problèmes
Get-PnpDevice | Where-Object {$_.Status -ne 'OK'}

# Détails d'un périphérique
Get-PnpDeviceProperty -InstanceId "USB\VID_8087..."

# Mettre à jour un pilote
pnputil /scan-devices
Update-Driver -InstanceId "USB\VID_8087..."

# Exporter pilotes
Export-WindowsDriver -Online -Destination "C:\DriversBackup"

# Installer un pilote
pnputil /add-driver "C:\Drivers\*.inf" /install

# Désinstaller un pilote
pnputil /delete-driver oem123.inf /uninstall

# Rollback
# Via Gestionnaire de périphériques ou:
# Get-WmiObject Win32_PnPEntity | Where-Object {$_.Name -like "*NomDevice*"}

# Événements pilotes
Get-WinEvent -LogName System | Where-Object {$_.ProviderName -eq "Microsoft-Windows-DriverFrameworks-UserMode"}
```
