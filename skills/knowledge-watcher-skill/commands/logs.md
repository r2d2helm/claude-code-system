# Commande: /kwatch-logs

Affiche les logs du Knowledge Watcher.

## Syntaxe

```
/kwatch-logs [--lines=N] [--level=LEVEL] [--date=DATE]
```

## Description

Affiche les logs de capture et de traitement du Knowledge Watcher.

## Exécution

**Afficher les 50 dernières lignes:**

```powershell
$SkillPath = "$env:USERPROFILE\.claude\skills\knowledge-watcher-skill"
$logDir = "$SkillPath\data\logs"
$today = Get-Date -Format "yyyy-MM-dd"
$logFile = "$logDir\kwatch_$today.log"

if (Test-Path $logFile) {
    Get-Content $logFile -Tail 50
} else {
    Write-Host "No logs for today"
}
```

## Options

| Option | Description | Défaut |
|--------|-------------|--------|
| `--lines=N` | Nombre de lignes | 50 |
| `--level=LEVEL` | Filtrer par niveau (INFO, WARN, ERROR) | all |
| `--date=DATE` | Date spécifique (YYYY-MM-DD) | today |

## Format des logs

```
[2026-02-05 10:30:45] [INFO] Started watcher for: Projets Actifs
[2026-02-05 10:31:12] [INFO] Added to queue: C:\Users\r2d2\Projets\script.ps1
[2026-02-05 10:31:15] [INFO] Processed: script.ps1 → 2026-02-05_Script.md
[2026-02-05 10:32:00] [WARN] File too large: bigfile.txt
[2026-02-05 10:33:00] [ERROR] Claude CLI timeout
```

## Filtrer par niveau

**Erreurs seulement:**
```powershell
Get-Content $logFile | Select-String "\[ERROR\]"
```

**Warnings et erreurs:**
```powershell
Get-Content $logFile | Select-String "\[(WARN|ERROR)\]"
```

## Logs des jours précédents

```powershell
$date = "2026-02-04"
$logFile = "$logDir\kwatch_$date.log"
Get-Content $logFile -Tail 100
```

## Lister les fichiers de log

```powershell
Get-ChildItem "$logDir\*.log" | Sort-Object LastWriteTime -Descending
```

## Rotation des logs

Les logs sont créés quotidiennement avec le format `kwatch_YYYY-MM-DD.log`.
Les anciens logs ne sont pas automatiquement supprimés - nettoyez manuellement si nécessaire.

## Exemple de sortie

```
[2026-02-05 08:00:01] [INFO] Knowledge Watcher started with 3 watchers (PID: 12345)
[2026-02-05 08:15:32] [INFO] Added to queue: C:\Users\r2d2\Projets\api\handler.ps1
[2026-02-05 08:15:33] [INFO] Captured file (Changed): handler.ps1
[2026-02-05 08:20:00] [INFO] Processed: handler.ps1 → Code/PowerShell/2026-02-05_handler.md
[2026-02-05 08:20:00] [INFO] Updated Daily Note with: [[2026-02-05_handler]]
[2026-02-05 09:00:00] [INFO] Scanned Downloads: found 3 files, added 2 to queue
[2026-02-05 09:00:15] [WARN] Duplicate detected, skipping: readme.md
```
