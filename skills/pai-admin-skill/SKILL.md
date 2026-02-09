# Agent PAI Admin — Installation, Configuration et Administration de PAI

Agent specialise dans l'installation, la configuration, l'administration et le depannage de PAI (Personal AI Infrastructure) sur Ubuntu Linux. Le DA s'appelle R2D2.

## Environnement

| Composant | Valeur |
|-----------|--------|
| DA | R2D2 |
| PAI Version | 2.5 |
| OS | Ubuntu Linux |
| PAI_DIR | `~/.claude` |
| Depot PAI | `/home/r2d2helm/Personal_AI_Infrastructure/` |
| Runtime | Bun (`~/.bun/bin/bun`) |
| Voice Server | `http://localhost:8888` |
| Observability | `http://localhost:4000` |
| Settings | `$PAI_DIR/settings.json` |
| Env vars | `$PAI_DIR/.env` |
| Hooks | `$PAI_DIR/hooks/` (15 hooks) |
| CORE Skill | `$PAI_DIR/skills/PAI/SKILL.md` |
| MEMORY | `$PAI_DIR/MEMORY/` (History, Learning, Signals) |
| Packs source | `/home/r2d2helm/Personal_AI_Infrastructure/Packs/` (23 packs) |
| Release source | `/home/r2d2helm/Personal_AI_Infrastructure/Releases/v2.5/.claude/` |

## Commandes Slash

### Installation

| Commande | Description |
|----------|-------------|
| `/pai-install` | Dispatch installation interactive (choix methode) |
| `/pai-prereqs` | Verifier/installer prerequis (Bun, Git, mpg123, notify-send) |
| `/pai-release-install` | Installer depuis release v2.5 (methode recommandee) |
| `/pai-bundle-install` | Installer via Bundle + packs individuels |
| `/pai-pack-install` | Installer un pack individuel |

### Verification

| Commande | Description |
|----------|-------------|
| `/pai-verify` | Verification complete du systeme PAI |
| `/pai-verify-hooks` | Verifier hooks (15 hooks, 12 libs, 4 handlers) |
| `/pai-verify-core` | Verifier CORE (SKILL.md, SYSTEM/, USER/) |
| `/pai-verify-voice` | Verifier voice system |
| `/pai-verify-observability` | Verifier observability dashboard |

### Etat et Inspection

| Commande | Description |
|----------|-------------|
| `/pai-status` | Etat complet du systeme PAI |
| `/pai-hooks` | Lister/inspecter/tester les hooks |
| `/pai-packs` | Lister packs disponibles/installes |
| `/pai-settings` | Voir/valider settings.json |
| `/pai-env` | Verifier variables d'environnement |
| `/pai-memory` | Inspecter MEMORY/ (History, Learning, Signals) |
| `/pai-logs` | Lire les logs MEMORY/ |

### Securite

| Commande | Description |
|----------|-------------|
| `/pai-security` | Audit securite (patterns, validator, logs) |

### Maintenance

| Commande | Description |
|----------|-------------|
| `/pai-upgrade` | Mettre a jour PAI (git pull + re-install) |
| `/pai-backup` | Sauvegarder l'installation PAI |
| `/pai-restore` | Restaurer depuis backup |

### Services

| Commande | Description |
|----------|-------------|
| `/pai-voice` | Gestion voice server (start/stop/status) |
| `/pai-observability` | Gestion dashboard observability (start/stop/status) |

### Depannage

| Commande | Description |
|----------|-------------|
| `/pai-diagnose` | Suite de diagnostic automatique |
| `/pai-fix-hooks` | Correctifs hooks courants |
| `/pai-fix-settings` | Reparer settings.json |

### Personnalisation

| Commande | Description |
|----------|-------------|
| `/pai-customize` | Personnaliser USER/ (identite, preferences) |

## Wizards Interactifs

| Wizard | Etapes | Description |
|--------|--------|-------------|
| Fresh Install | 8 | Installation complete depuis zero |
| Migrate | 5 | Migration settings existants vers PAI |
| Troubleshoot | - | Depannage interactif (arbre de decision) |
| Pack Selector | 4 | Selection guidee de packs |
| Voice Setup | 5 | Configuration voix ElevenLabs |
| Security Audit | 6 | Audit securite complet |

## Syntaxe

```
/pai-<commande> [action] [options]
```

### Exemples

```
/pai-prereqs
/pai-prereqs --install
/pai-install
/pai-release-install
/pai-pack-install pai-voice-system
/pai-status
/pai-verify
/pai-hooks list
/pai-hooks test SecurityValidator
/pai-packs
/pai-settings
/pai-voice start
/pai-voice stop
/pai-voice status
/pai-backup
/pai-diagnose
/pai-security
```

## Architecture PAI (resume)

PAI est un framework en 5 couches :

1. **Configuration** (`settings.json`) : Identite DA/principal, hooks, permissions, env vars
2. **CORE Skill** (`skills/PAI/`) : Auto-charge au demarrage, routage, format reponse, 19 docs SYSTEM/
3. **Hook System** (`hooks/`) : 15 hooks sur 7 evenements, middleware evenementiel
4. **Memory System** (`MEMORY/`) : 3 tiers — History, Learning, Signals
5. **Services** : Voice Server (port 8888), Observability (port 4000)

Details complets : `lib/knowledge/architecture.md`

## References techniques

| Fichier | Contenu |
|---------|---------|
| `lib/knowledge/architecture.md` | Architecture PAI complete |
| `lib/knowledge/hooks-reference.md` | Catalogue 15 hooks + payloads + exit codes |
| `lib/knowledge/packs-catalog.md` | 23 packs avec descriptions et dependances |
| `lib/knowledge/memory-system.md` | Systeme memoire 3-tier |
| `lib/knowledge/security-model.md` | SecurityValidator + .pai-protected.json |
| `lib/knowledge/settings-schema.md` | Schema complet settings.json |
| `lib/knowledge/voice-system.md` | Architecture serveur vocal |
| `lib/knowledge/observability.md` | Dashboard Vue.js + WebSocket |
| `lib/knowledge/linux-specifics.md` | Adaptations Ubuntu/Linux |
| `lib/knowledge/troubleshooting-kb.md` | Base de connaissances problemes/solutions |

## Points critiques

### Merge settings.json
L'utilisateur a deja un `~/.claude/settings.json` avec config MCP. L'installation PAI doit **fusionner** (preserver `mcpServers`) et non ecraser.

### Prerequis manquants
- **Bun** : `curl -fsSL https://bun.sh/install | bash`
- **mpg123** : `sudo apt install mpg123` (audio Linux)
- **notify-send** : `sudo apt install libnotify-bin` (notifications)

### Adaptations Linux
- Audio : mpg123/mpv au lieu de afplay
- Notifications : notify-send au lieu de osascript
- Auto-start : systemd user service au lieu de LaunchAgent
- Chemins : `~/.config/systemd/user/` au lieu de `~/Library/LaunchAgents/`
- sed : GNU sed (pas de `-i ''`)

### Configuration R2D2
- `daidentity.name` = "R2D2"
- `principal.name` = a demander pendant le wizard
- `TIME_ZONE` = a demander pendant le wizard

## Structure du Skill

```
pai-admin-skill/
  SKILL.md                  # Ce fichier
  commands/                 # 27 commandes slash
  wizards/                  # 6 assistants interactifs
  lib/knowledge/            # 10 fichiers reference technique
```
