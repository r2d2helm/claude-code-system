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
║  ✅ bash 5+              : Détecté (5.2.15)                  ║
║  ✅ inotify-tools        : Détecté                           ║
║  ✅ Claude CLI           : Détecté                           ║
║  ✅ Obsidian Vault       : Détecté                           ║
║                                                              ║
║  [Continuer]                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Vérification bash:**
```bash
#!/usr/bin/env bash
SKILL_PATH="$HOME/.claude/skills/knowledge-watcher-skill"
source "$SKILL_PATH/scripts/kw-lib.sh"

issues=()

# Vérifier inotify-tools
if ! command -v inotifywait &>/dev/null; then
    issues+=("inotify-tools non installé (sudo apt install inotify-tools)")
fi

# Vérifier Claude CLI
if ! command -v claude &>/dev/null; then
    issues+=("Claude CLI non trouvé")
fi

# Vérifier vault
if [ ! -d "$HOME/Documents/Knowledge" ]; then
    issues+=("Vault Obsidian non trouvé: ~/Documents/Knowledge")
fi

if [ ${#issues[@]} -eq 0 ]; then
    echo "✅ All prerequisites met"
else
    echo "❌ Issues found:"
    printf '   - %s\n' "${issues[@]}"
fi
```

### Étape 2: Configuration du Vault Obsidian

```
╔══════════════════════════════════════════════════════════════╗
║  Étape 2/5: Configuration du Vault Obsidian                  ║
║                                                              ║
║  Chemin actuel: ~/Documents/Knowledge                        ║
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
║  [x] Claude History (~/.claude/history.jsonl)                ║
║  [x] Projets (~/Projets)                                     ║
║  [ ] Knowledge Vault (éviter doublons)                       ║
║                                                              ║
║  TIER 2 - Horaire:                                           ║
║  [x] Downloads (~/Downloads)                                 ║
║  [ ] Formations (~/Documents/Formations)                     ║
║                                                              ║
║  TIER 3 - Quotidien:                                         ║
║  [ ] Browser Bookmarks                                       ║
║  [ ] Scripts Bash                                            ║
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
║  📁 Vault     : ~/Documents/Knowledge                        ║
║  🔍 Sources   : 4 activées (2 real-time, 2 batch)            ║
║  🤖 Résumés   : Activés (timeout 30s)                        ║
║  📅 Daily     : Mise à jour automatique                      ║
║                                                              ║
║  Actions à effectuer:                                        ║
║  • Sauvegarder la configuration                              ║
║  • Démarrer les watchers                                     ║
║  • (Optionnel) Enregistrer les cron jobs                     ║
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
3. Pour les cron jobs (tâches planifiées): `crontab -e` et ajouter les entrées depuis `scripts/crontab-entries.txt`

## Reconfiguration

Pour reconfigurer:
```
/kwatch-config edit
```

Ou relancer:
```
/kwatch-wizard setup
```
