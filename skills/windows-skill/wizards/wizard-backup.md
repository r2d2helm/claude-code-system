# Wizard: Backup Strategy

Configuration stratégie de sauvegarde Windows 11/Server 2025.

## Déclenchement

```
/win-wizard backup
```

## Étapes du Wizard (4)

### Étape 1: Analyse Stockage

```
╔══════════════════════════════════════════════════════════════╗
║           💾 WIZARD BACKUP STRATEGY                          ║
║               Étape 1/4 : Analyse                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📊 ANALYSE DU SYSTÈME:                                      ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ C: (System)  : 120 GB utilisés / 256 GB                 │ ║
║  │ D: (Data)    : 450 GB utilisés / 1 TB                   │ ║
║  │ E: (Backup)  : 200 GB libres / 2 TB                     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📁 DONNÉES CRITIQUES DÉTECTÉES:                             ║
║  • Profils utilisateurs : 45 GB                              ║
║  • Bases de données     : 120 GB                             ║
║  • Documents partagés   : 85 GB                              ║
║  • Applications         : 35 GB                              ║
║                                                              ║
║  Estimation sauvegarde complète : ~285 GB                    ║
║                                                              ║
║  [1] Continuer  [2] Modifier la sélection                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 2: Destination

```
╔══════════════════════════════════════════════════════════════╗
║           💾 WIZARD BACKUP STRATEGY                          ║
║              Étape 2/4 : Destination                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Où sauvegarder ?                                            ║
║                                                              ║
║  Local:                                                      ║
║  [1] Disque local (E:\Backups)                               ║
║  [2] Disque externe USB                                      ║
║  [3] NAS/Partage réseau (\\nas\backups)                      ║
║                                                              ║
║  Cloud (règle 3-2-1):                                        ║
║  [4] Azure Backup                                            ║
║  [5] AWS S3 / Glacier                                        ║
║  [6] Backblaze B2                                            ║
║                                                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Chemin : \\nas.local\backups\serveur01______________    │ ║
║  │ User   : backup-user________________________            │ ║
║  │ Pass   : ********************************               │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Tester connexion partage réseau
Test-Path "\\nas.local\backups"

# Créer credential pour sauvegarde
$Credential = Get-Credential -Message "Compte de sauvegarde"
New-StoredCredential -Target "BackupNAS" -Credentials $Credential

# Configurer destination wbadmin
wbadmin enable backup -addtarget:\\nas.local\backups -user:backup-user -password:P@ssw0rd
```

### Étape 3: Planification

```
╔══════════════════════════════════════════════════════════════╗
║           💾 WIZARD BACKUP STRATEGY                          ║
║             Étape 3/4 : Planification                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📅 STRATÉGIE DE SAUVEGARDE:                                 ║
║                                                              ║
║  Type de sauvegarde:                                         ║
║  [1] Complète uniquement (plus simple)                       ║
║  [2] Complète + Incrémentale (recommandé)                    ║
║  [3] Complète + Différentielle                               ║
║                                                              ║
║  Planification:                                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Complète   : Dimanche 02:00                             │ ║
║  │ Incrémentale: Lun-Sam 02:00                             │ ║
║  │                                                         │ ║
║  │ Rétention:                                              │ ║
║  │ • Quotidienne : 7 jours                                 │ ║
║  │ • Hebdomadaire: 4 semaines                              │ ║
║  │ • Mensuelle   : 12 mois                                 │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Appliquer  [2] Modifier  [3] Avancé                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Activer Windows Server Backup
Install-WindowsFeature Windows-Server-Backup -IncludeManagementTools

# Créer politique de sauvegarde
$Policy = New-WBPolicy
$BackupTarget = New-WBBackupTarget -NetworkPath "\\nas.local\backups"
Add-WBBackupTarget -Policy $Policy -Target $BackupTarget

# Ajouter volumes
$Volume = Get-WBVolume -AllVolumes | Where-Object {$_.MountPath -eq "C:"}
Add-WBVolume -Policy $Policy -Volume $Volume

# Planifier
Set-WBSchedule -Policy $Policy -Schedule 02:00

# Activer System State
Add-WBSystemState -Policy $Policy

# Sauvegarder la politique
Set-WBPolicy -Policy $Policy -Force
```

### Étape 4: Test et Validation

```
╔══════════════════════════════════════════════════════════════╗
║           💾 WIZARD BACKUP STRATEGY                          ║
║              Étape 4/4 : Validation                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🧪 TEST DE SAUVEGARDE:                                      ║
║                                                              ║
║  [██████████████████████████████] 100%                       ║
║                                                              ║
║  ✅ RÉSULTATS:                                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✓ Connexion destination     : OK                        │ ║
║  │ ✓ Espace disponible         : 1.8 TB (suffisant)        │ ║
║  │ ✓ Permissions écriture      : OK                        │ ║
║  │ ✓ Sauvegarde test           : Réussie (285 GB)          │ ║
║  │ ✓ Vérification intégrité    : OK                        │ ║
║  │ ✓ Test restauration fichier : OK                        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📋 STRATÉGIE CONFIGURÉE:                                    ║
║  • Complète: Dimanche 02:00                                  ║
║  • Incrémentale: Lun-Sam 02:00                               ║
║  • Rétention: 7j/4sem/12mois                                 ║
║  • Destination: \\nas.local\backups                          ║
║                                                              ║
║  [1] Terminer  [2] Exécuter sauvegarde maintenant            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes test:**
```powershell
# Lancer sauvegarde immédiate
Start-WBBackup -Policy (Get-WBPolicy)

# Vérifier dernière sauvegarde
Get-WBBackupSet | Sort-Object BackupTime -Descending | Select-Object -First 1

# Historique des sauvegardes
wbadmin get versions

# Test restauration fichier
wbadmin start recovery -version:01/15/2025-02:00 -itemType:File -items:C:\Data\test.txt -recoveryTarget:C:\Restore -quiet
```
