# Wizard: /kwatch-wizard setup

Configuration initiale guidée du Knowledge Watcher.

## Description

Ce wizard vous guide à travers la configuration initiale du Knowledge Watcher Agent pour adapter la surveillance à votre environnement.

## Étapes du Wizard

### Étape 1: Vérification des prérequis

```
╔══════════════════════════════════════════════════════════════╗
║         🔧 KNOWLEDGE WATCHER SETUP WIZARD                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Étape 1/5: Vérification des prérequis                       ║
║                                                              ║
║  ✅ PowerShell 7.4+     : Détecté (7.4.1)                    ║
║  ✅ Claude CLI          : Détecté                            ║
║  ✅ Obsidian Vault      : Détecté                            ║
║                                                              ║
║  [Continuer]                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Vérification PowerShell:**
```powershell
$SkillPath = "$env:USERPROFILE\.claude\skills\knowledge-watcher-skill"
Import-Module "$SkillPath\scripts\KnowledgeWatcher.psm1" -Force

$setup = Test-KWSetup
if ($setup.IsValid) {
    Write-Host "✅ All prerequisites met"
} else {
    Write-Host "❌ Issues found:"
    $setup.Issues | ForEach-Object { Write-Host "   - $_" }
}
```

### Étape 2: Configuration du Vault Obsidian

```
╔══════════════════════════════════════════════════════════════╗
║  Étape 2/5: Configuration du Vault Obsidian                  ║
║                                                              ║
║  Chemin actuel: C:\Users\r2d2\Documents\Knowledge            ║
║                                                              ║
║  [1] Garder ce chemin (Recommandé)                           ║
║  [2] Changer le chemin                                       ║
║  [3] Créer un nouveau vault                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

Demander à l'utilisateur de confirmer ou modifier le chemin du vault.

### Étape 3: Sélection des sources à surveiller

```
╔══════════════════════════════════════════════════════════════╗
║  Étape 3/5: Sources à surveiller                             ║
║                                                              ║
║  TIER 1 - Temps réel:                                        ║
║  [x] Claude History (~\.claude\history.jsonl)                ║
║  [x] Projets (~\Projets)                                     ║
║  [ ] Knowledge Vault (éviter doublons)                       ║
║                                                              ║
║  TIER 2 - Horaire:                                           ║
║  [x] Downloads (~\Downloads)                                 ║
║  [ ] Formations (~\Documents\Formations)                     ║
║                                                              ║
║  TIER 3 - Quotidien:                                         ║
║  [ ] Browser Bookmarks                                       ║
║  [ ] PowerShell Scripts                                      ║
║                                                              ║
║  TIER 4 - Hebdomadaire:                                      ║
║  [ ] Archives                                                ║
║  [ ] Resources                                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 4: Options de traitement

```
╔══════════════════════════════════════════════════════════════╗
║  Étape 4/5: Options de traitement                            ║
║                                                              ║
║  Résumé IA (Claude CLI):                                     ║
║  [x] Activer les résumés automatiques                        ║
║      Timeout: [30] secondes                                  ║
║                                                              ║
║  Daily Note:                                                 ║
║  [x] Mettre à jour automatiquement                           ║
║                                                              ║
║  Déduplication:                                              ║
║  [x] Ignorer les fichiers déjà traités (24h)                 ║
║                                                              ║
║  Langue des résumés:                                         ║
║  [x] Français                                                ║
║  [ ] English                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 5: Récapitulatif et activation

```
╔══════════════════════════════════════════════════════════════╗
║  Étape 5/5: Récapitulatif                                    ║
║                                                              ║
║  📁 Vault     : C:\Users\r2d2\Documents\Knowledge            ║
║  🔍 Sources   : 4 activées (2 real-time, 2 batch)            ║
║  🤖 Résumés   : Activés (timeout 30s)                        ║
║  📅 Daily     : Mise à jour automatique                      ║
║                                                              ║
║  Actions à effectuer:                                        ║
║  • Sauvegarder la configuration                              ║
║  • Démarrer les watchers                                     ║
║  • (Optionnel) Enregistrer les tâches planifiées             ║
║                                                              ║
║  [1] Sauvegarder et démarrer                                 ║
║  [2] Sauvegarder seulement                                   ║
║  [3] Annuler                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Post-Setup

Après le setup:
1. Les watchers démarrent automatiquement
2. `/kwatch-status` affiche le dashboard
3. Pour les tâches planifiées (admin requis): `Register-WatcherTasks.ps1`

## Reconfiguration

Pour reconfigurer:
```
/kwatch-config edit
```

Ou relancer:
```
/kwatch-wizard setup
```
