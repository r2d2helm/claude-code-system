# Gestion des Tâches Planifiées

Administration du Planificateur de tâches Windows.

## Mode d'Utilisation
```
/tasks                      → Vue d'ensemble des tâches
/tasks list                 → Liste complète des tâches
/tasks info "nom"           → Détails d'une tâche
/tasks create               → Créer une nouvelle tâche
/tasks run "nom"            → Exécuter immédiatement
/tasks enable "nom"         → Activer une tâche
/tasks disable "nom"        → Désactiver une tâche
/tasks history              → Historique des exécutions
/tasks failed               → Tâches en échec
```

Arguments: $ARGUMENTS

---

## Vue d'Ensemble (défaut)

```
⏰ TÂCHES PLANIFIÉES
═══════════════════════════════════════════════════════════════

STATISTIQUES:
├─ Tâches totales: 156 (89 actives)
├─ En cours: 2
└─ Échecs (24h): 3

PROCHAINES EXÉCUTIONS:
┌────────────────────────────────────────┬─────────────────────┐
│ Tâche                                  │ Prochaine           │
├────────────────────────────────────────┼─────────────────────┤
│ GoogleUpdateTaskMachineCore            │ 11:00 aujourd'hui   │
│ \Custom\DailyBackup                    │ 03:00 demain        │
│ \Custom\WeeklyMaintenance              │ Dimanche 02:00      │
└────────────────────────────────────────┴─────────────────────┘

EN COURS:
├─ Windows Defender Scan (depuis 10:30)
└─ \Custom\DataSync (depuis 10:45)

ÉCHECS RÉCENTS:
├─ \Custom\OldBackupScript - 0x1 (03:00)
└─ SoftwareDistribution\Config - 0x41301

Actions: /tasks failed | /tasks create
```

---

## Mode `create`

```
🆕 CRÉATION D'UNE TÂCHE
═══════════════════════════════════════════════════════════════

1. NOM: _____

2. DÉCLENCHEUR:
   [daily] Quotidien | [weekly] Hebdo | [startup] Démarrage
   Heure: _____ (HH:MM)

3. ACTION:
   Programme: _____
   Arguments: _____

4. COMPTE:
   [user] Utilisateur | [system] SYSTEM

RÉSUMÉ:
├─ Nom: MonitorServices
├─ Déclencheur: Quotidien 03:00
├─ Action: powershell.exe -File C:\Scripts\monitor.ps1
└─ Compte: SYSTEM

Créer? [O/N]
```

---

## Mode `failed`

```
❌ TÂCHES EN ÉCHEC
═══════════════════════════════════════════════════════════════

🔴 \Custom\OldBackupScript
├─ Échec: 2026-02-03 03:00 | Code: 0x1
├─ Programme: C:\Scripts\old-backup.bat
├─ Diagnostic: Script référence chemin inexistant
└─ Action: Désactiver ou corriger le script

🟠 SoftwareDistribution\Config
├─ Code: 0x41301 (Tâche en cours)
└─ Note: Généralement bénin, ignorable

Suggestions: Désactiver les tâches obsolètes
```

---

## Commandes de Référence

```powershell
# Lister
Get-ScheduledTask | Select-Object TaskName, State

# Créer
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\script.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
Register-ScheduledTask -TaskName "MaTâche" -Action $action -Trigger $trigger

# Exécuter
Start-ScheduledTask -TaskName "NomTâche"

# Activer/Désactiver
Enable-ScheduledTask -TaskName "NomTâche"
Disable-ScheduledTask -TaskName "NomTâche"

# Historique
Get-WinEvent -LogName 'Microsoft-Windows-TaskScheduler/Operational' -MaxEvents 50
```
