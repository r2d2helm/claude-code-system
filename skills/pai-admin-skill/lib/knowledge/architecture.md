# Architecture PAI v2.5

## Vue d'ensemble

PAI (Personal AI Infrastructure) est un framework open-source qui transforme Claude Code en système IA personnel. Il fournit mémoire, skills, hooks, sécurité et suivi d'objectifs.

## Structure de répertoires (installation complète)

```
$PAI_DIR/                              # ~/.claude par défaut
├── settings.json                      # Configuration centrale
├── .env                               # Clés API (ELEVENLABS_API_KEY, etc.)
├── CLAUDE.md                          # Point d'entrée (charge SKILL.md)
├── skills/                            # Modules de compétences
│   ├── PAI/                           # Skill CORE (auto-chargé)
│   │   ├── SKILL.md                   # Définition principale + routage
│   │   ├── SYSTEM/                    # 19 docs architecture système
│   │   │   └── AISTEERINGRULES.md     # Règles de pilotage IA
│   │   ├── USER/                      # Personnalisation utilisateur
│   │   │   ├── AISTEERINGRULES.md     # Règles utilisateur
│   │   │   └── DAIDENTITY.md          # Identité du DA
│   │   ├── WORK/                      # Travail sensible en cours
│   │   ├── Workflows/                 # 4 workflows (Delegation, SessionContinuity, etc.)
│   │   └── Tools/                     # 4 outils CLI (Inference, SessionProgress, etc.)
│   └── [AutresSkills]/                # Skills additionnels installés par packs
├── hooks/                             # Gestionnaires d'événements (15 hooks)
│   ├── SecurityValidator.hook.ts      # PreToolUse: blocage commandes dangereuses
│   ├── LoadContext.hook.ts            # SessionStart: injection contexte
│   ├── StartupGreeting.hook.ts        # SessionStart: greeting vocal
│   ├── CheckVersion.hook.ts           # SessionStart: version check
│   ├── lib/                           # 12 bibliothèques partagées
│   └── handlers/                      # 4 handlers spécialisés
├── MEMORY/                            # Système mémoire 3-tier
│   ├── History/                       # Historique sessions
│   ├── Learning/                      # Apprentissages capturés
│   └── Signals/                       # Signaux (ratings, sentiment)
├── agents/                            # Configurations d'agents nommés
├── Plans/                             # Fichiers de travail mode plan
├── WORK/                              # Sessions de travail actives
├── tools/                             # Utilitaires CLI
├── bin/                               # Scripts exécutables
├── observability/                     # Dashboard monitoring (optionnel)
│   ├── manage.sh                      # Script contrôle
│   └── apps/
│       ├── server/                    # Backend Bun + TypeScript
│       └── client/                    # Frontend Vue 3 + Vite
├── VoiceServer/                       # Serveur vocal (optionnel)
│   ├── server.ts                      # Serveur HTTP TTS
│   ├── start.sh / stop.sh             # Scripts contrôle
│   └── voices.json                    # Config voix par agent
└── statusline-command.sh              # Status line Claude Code
```

## Couches du système

### 1. Configuration (settings.json)
Fichier central contenant : identité DA, identité principal, hooks, permissions, env vars, contextFiles, techStack.

### 2. CORE Skill (skills/PAI/)
Auto-chargé au démarrage via `contextFiles`. Fournit : routage des skills, format de réponse, architecture, workflows, sécurité.

### 3. Hook System (hooks/)
Middleware événementiel : 15 hooks sur 7 types d'événements. Interception, validation, capture, automatisation.

### 4. Memory System (MEMORY/)
3 tiers : History (sessions), Learning (insights), Signals (feedback). Persistance inter-sessions.

### 5. Skills additionnels
18 skill packs installables indépendamment. Routage intelligent via CORE SKILL.md.

### 6. Intégrations externes
- Voice Server : TTS ElevenLabs (port 8888)
- Observability Dashboard : monitoring temps réel (port 4000)
- Agents : composition dynamique avec personnalités

## Variables d'environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `PAI_DIR` | `~/.claude` | Répertoire racine PAI |
| `TIME_ZONE` | Système | Fuseau horaire |
| `DA` | `PAI` | Nom de l'assistant |
| `PAI_OBSERVABILITY_URL` | `http://localhost:4000/events` | Endpoint dashboard |
| `PAI_TAB_PREFIX` | ` ` | Préfixe titre onglet |
| `ELEVENLABS_API_KEY` | - | Clé API ElevenLabs |
| `PROJECTS_DIR` | - | Répertoire projets |

## Ports réseau

| Service | Port | Protocole |
|---------|------|-----------|
| Voice Server | 8888 | HTTP |
| Observability Server | 4000 | HTTP + WebSocket |

## Flux de données

```
Utilisateur → Claude Code → Événements hooks
                                    ↓
                            Hook System (15 hooks)
                                    ↓
                    ┌───────────────┼───────────────┐
                    ↓               ↓               ↓
              MEMORY/          Observability     Voice Server
           (persistance)       (monitoring)     (notifications)
```
