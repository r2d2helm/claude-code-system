# Commande: /kwatch-process

Traite manuellement la queue de capture.

## Syntaxe

```
/kwatch-process [--batch=N] [--force]
```

## Description

Lance le traitement du pipeline pour transformer les éléments capturés en notes Obsidian:
1. **Classification** - Détermine le type et le dossier de destination
2. **Résumé** - Génère un résumé via Claude CLI
3. **Formatage** - Crée le fichier Markdown avec frontmatter

## Exécution

**IMPORTANT**: Exécute ce script bash:

```bash
SKILL_PATH="$HOME/.claude/skills/knowledge-watcher-skill"
bash "$SKILL_PATH/scripts/invoke-queue-processor.sh"
```

Avec options:
```bash
bash "$SKILL_PATH/scripts/invoke-queue-processor.sh" --batch-size 5
```

## Options

| Option | Description | Défaut |
|--------|-------------|--------|
| `--batch=N` | Nombre d'items à traiter | 10 |
| `--force` | Continuer malgré les erreurs | false |

## Exemple de sortie

```
🔄 Processing 3 item(s)...

  📄 Configuration du serveur Proxmox
     → Classifying...
       Type: troubleshooting, Folder: Références/Troubleshooting
     → Summarizing...
       Source: claude
     → Formatting...
     → Writing note...
     ✅ Created: 2026-02-05_Fix_Configuration-du-serveur-Proxmox.md

  📄 Script de backup automatique
     → Classifying...
       Type: code, Folder: Code/Bash
     → Summarizing...
       Source: claude
     → Formatting...
     → Writing note...
     ✅ Created: 2026-02-05_Script-de-backup-automatique.md

═══════════════════════════════════════════════════════════════
  ✅ Processed : 2
  ❌ Errors    : 0
  ⏭️  Skipped   : 1
═══════════════════════════════════════════════════════════════
```

## Notes

- Si Claude CLI timeout, un résumé basique est généré (fallback)
- Les doublons sont automatiquement ignorés (hash-based)
- Les items traités restent dans la queue 24h pour debug
- Les notes sont créées avec le bon template Obsidian

## Pipeline de traitement

```
Queue Item
    ↓
┌─────────────┐
│ Classifier  │ → Type, Folder, Tags
└─────────────┘
    ↓
┌─────────────┐
│ Summarizer  │ → Summary, Key Points, Concepts
└─────────────┘
    ↓
┌─────────────┐
│ Formatter   │ → Markdown + Frontmatter
└─────────────┘
    ↓
Obsidian Vault + Daily Note
```
