# Gestion des Disques et Stockage

Administration du stockage Windows.

## Mode d'Utilisation
```
/disk                       → Vue d'ensemble du stockage
/disk health                → Santé des disques (SMART)
/disk usage                 → Analyse de l'utilisation de l'espace
/disk usage C:\Users        → Analyse d'un dossier spécifique
/disk cleanup               → Suggestions de nettoyage
/disk partitions            → Gestion des partitions
/disk optimize              → Optimisation (Trim/Défrag)
```

Arguments: $ARGUMENTS

---

## Vue d'Ensemble (défaut)

```
💾 STOCKAGE SYSTÈME
═══════════════════════════════════════════════════════════════

DISQUES PHYSIQUES:
┌─────────────────────────────────────────────────────────────┐
│ 💿 Disk 0: Samsung SSD 970 EVO Plus 500GB                  │
│    Type: NVMe SSD │ Santé: ✅ Healthy │ Temp: 35°C         │
├─────────────────────────────────────────────────────────────┤
│ 💿 Disk 1: WD Blue 2TB                                     │
│    Type: HDD │ Santé: ✅ Healthy │ Temp: 32°C              │
└─────────────────────────────────────────────────────────────┘

VOLUMES:
┌───────┬────────────┬───────────┬───────────┬───────────────┐
│ Lettre│ Label      │ Total     │ Libre     │ Utilisé       │
├───────┼────────────┼───────────┼───────────┼───────────────┤
│ C:    │ System     │ 465.76 GB │ 147.23 GB │ ████████░░ 68%│
│ D:    │ Data       │ 1.82 TB   │ 1.43 TB   │ ██░░░░░░░░ 21%│
│ E:    │ Backup     │ 931.51 GB │ 456.78 GB │ █████░░░░░ 51%│
└───────┴────────────┴───────────┴───────────┴───────────────┘

⚠️ ALERTES:
└─ Aucune alerte
```

---

## Mode `health`

Analyse SMART et santé des disques:

```
🏥 SANTÉ DES DISQUES
═══════════════════════════════════════════════════════════════

💿 Disk 0: Samsung SSD 970 EVO Plus 500GB
├─ État général: ✅ Healthy
├─ Température: 35°C (Normal: < 70°C)
├─ Heures d'utilisation: 8,547h
├─ Cycles d'écriture: 12,456 (Limite estimée: 600,000)
├─ Usure estimée: 2% utilisé
├─ Données écrites: 45.2 TB (Total Bytes Written)
└─ Attributs SMART:
   ├─ Reallocated Sectors: 0 ✅
   ├─ Pending Sectors: 0 ✅
   ├─ Uncorrectable Errors: 0 ✅
   └─ Temperature: 35°C ✅

💿 Disk 1: WD Blue 2TB
├─ État général: ✅ Healthy
├─ Température: 32°C
├─ Heures d'utilisation: 15,234h
└─ Attributs SMART:
   ├─ Reallocated Sectors: 0 ✅
   ├─ Spin Retry Count: 0 ✅
   ├─ Reallocated Event Count: 0 ✅
   ├─ Current Pending Sector: 0 ✅
   └─ Offline Uncorrectable: 0 ✅

RÉSUMÉ:
├─ Disques en bonne santé: 2/2
└─ Actions requises: Aucune
```

Si problème détecté:
```
⚠️ ALERTE: Disk 1 - Secteurs réalloués détectés
   Valeur actuelle: 24 secteurs
   Recommandation: Sauvegarder les données, planifier remplacement
```

---

## Mode `usage`

Analyse de l'utilisation de l'espace:

```
📊 ANALYSE D'UTILISATION: C:\
═══════════════════════════════════════════════════════════════

Top 10 des dossiers les plus volumineux:
┌─────────────────────────────────────────┬───────────┬───────┐
│ Dossier                                 │ Taille    │ %     │
├─────────────────────────────────────────┼───────────┼───────┤
│ C:\Users                                │ 89.5 GB   │ 28.1% │
│ C:\Windows                              │ 45.2 GB   │ 14.2% │
│ C:\Program Files                        │ 32.1 GB   │ 10.1% │
│ C:\Program Files (x86)                  │ 18.7 GB   │ 5.9%  │
│ C:\ProgramData                          │ 12.3 GB   │ 3.9%  │
│ C:\Windows\Installer                    │ 8.4 GB    │ 2.6%  │
│ C:\Windows\WinSxS                       │ 7.8 GB    │ 2.5%  │
│ C:\Users\Jean\AppData                   │ 6.2 GB    │ 1.9%  │
│ C:\$Recycle.Bin                         │ 3.1 GB    │ 1.0%  │
│ C:\Windows\SoftwareDistribution         │ 2.8 GB    │ 0.9%  │
└─────────────────────────────────────────┴───────────┴───────┘

Détail C:\Users:
├─ Jean.Dupont: 65.3 GB
│  ├─ Downloads: 23.4 GB
│  ├─ Documents: 18.2 GB
│  ├─ AppData: 15.1 GB
│  └─ Desktop: 8.6 GB
└─ Marie.Martin: 24.2 GB

FICHIERS VOLUMINEUX (> 1 GB):
├─ C:\Users\Jean\Downloads\installer.iso: 4.7 GB
├─ C:\Users\Jean\VMs\disk.vhdx: 3.2 GB
└─ C:\hiberfil.sys: 6.4 GB

TYPES DE FICHIERS:
├─ Vidéos (.mp4, .mkv, .avi): 34.5 GB
├─ Images (.jpg, .png, .raw): 12.3 GB
├─ Archives (.zip, .rar, .7z): 8.7 GB
└─ Documents (.docx, .pdf, .xlsx): 4.2 GB
```

---

## Mode `cleanup`

Suggestions de nettoyage avec estimation:

```
🧹 OPPORTUNITÉS DE NETTOYAGE
═══════════════════════════════════════════════════════════════

Catégorie                          │ Taille    │ Risque │ Action
───────────────────────────────────┼───────────┼────────┼────────
Fichiers temporaires utilisateur   │ 2.3 GB    │ ✅ Sûr │ [Nettoyer]
Fichiers temporaires Windows       │ 1.8 GB    │ ✅ Sûr │ [Nettoyer]
Cache Windows Update               │ 2.8 GB    │ ✅ Sûr │ [Nettoyer]
Corbeille                          │ 3.1 GB    │ ✅ Sûr │ [Vider]
Logs anciens (> 30j)               │ 0.8 GB    │ ✅ Sûr │ [Nettoyer]
Miniatures                         │ 0.4 GB    │ ✅ Sûr │ [Nettoyer]
───────────────────────────────────┼───────────┼────────┼────────
Cache navigateurs                  │ 4.2 GB    │ 🟡 Mod │ [Nettoyer]
  ├─ Chrome                        │ 2.1 GB    │        │
  ├─ Edge                          │ 1.5 GB    │        │
  └─ Firefox                       │ 0.6 GB    │        │
───────────────────────────────────┼───────────┼────────┼────────
Fichiers d'installation obsolètes  │ 3.4 GB    │ 🟠 Att │ [Analyser]
Anciens Windows (Windows.old)      │ 15.2 GB   │ 🟠 Att │ [Supprimer]
───────────────────────────────────┴───────────┴────────┴────────

TOTAL RÉCUPÉRABLE: ~34 GB

Options:
1. Nettoyage sûr uniquement (~11 GB)
2. Nettoyage modéré (~15 GB)
3. Nettoyage complet (~34 GB) - Confirmation requise
```

---

## Mode `partitions`

```
📦 PARTITIONS
═══════════════════════════════════════════════════════════════

Disk 0 (465.76 GB - Samsung SSD):
┌─────────┬─────────────┬───────────┬────────────┬───────────┐
│ #       │ Type        │ Taille    │ Système    │ Statut    │
├─────────┼─────────────┼───────────┼────────────┼───────────┤
│ 1       │ EFI System  │ 100 MB    │ FAT32      │ Healthy   │
│ 2       │ MSR         │ 16 MB     │ -          │ Healthy   │
│ 3       │ Primary (C:)│ 465.63 GB │ NTFS       │ Healthy   │
└─────────┴─────────────┴───────────┴────────────┴───────────┘

Disk 1 (1.82 TB - WD Blue):
┌─────────┬─────────────┬───────────┬────────────┬───────────┐
│ #       │ Type        │ Taille    │ Système    │ Statut    │
├─────────┼─────────────┼───────────┼────────────┼───────────┤
│ 1       │ Primary (D:)│ 1.82 TB   │ NTFS       │ Healthy   │
└─────────┴─────────────┴───────────┴────────────┴───────────┘

Espace non alloué: 0 GB
```

---

## Mode `optimize`

```
⚡ OPTIMISATION DES DISQUES
═══════════════════════════════════════════════════════════════

C: (SSD NVMe)
├─ Type d'optimisation: TRIM
├─ Dernière optimisation: 2026-02-01
├─ Planification: Hebdomadaire ✅
└─ Action recommandée: Aucune (optimisé récemment)

D: (HDD)
├─ Type d'optimisation: Défragmentation
├─ Fragmentation actuelle: 12%
├─ Dernière optimisation: 2026-01-15
├─ Planification: Hebdomadaire ✅
└─ Action recommandée: Défragmenter (> 10%)

Lancer l'optimisation maintenant?
⚠️ Durée estimée: 
   - C: ~2 minutes (TRIM)
   - D: ~45 minutes (Défrag 12%)
```

---

## Commandes de Référence

```powershell
# Vue d'ensemble
Get-Volume | Format-Table DriveLetter, FileSystemLabel, Size, SizeRemaining, HealthStatus

# Disques physiques
Get-PhysicalDisk | Select-Object FriendlyName, MediaType, Size, HealthStatus

# SMART (nécessite droits admin)
Get-PhysicalDisk | Get-StorageReliabilityCounter

# Taille d'un dossier
(Get-ChildItem -Path "C:\Users" -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB

# Fichiers volumineux
Get-ChildItem -Path C:\ -Recurse -ErrorAction SilentlyContinue | Where-Object {$_.Length -gt 1GB} | Sort-Object Length -Descending

# Optimisation
Optimize-Volume -DriveLetter C -ReTrim -Verbose
Optimize-Volume -DriveLetter D -Defrag -Verbose
```
