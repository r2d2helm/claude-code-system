# Dashboard Observability PAI v2.5

## Vue d'ensemble

Dashboard monitoring temps réel multi-agents avec streaming WebSocket. Frontend Vue 3 + Vite, Backend Bun + TypeScript.

## Architecture

```
$PAI_DIR/observability/
├── manage.sh                          # Script contrôle (start/stop/restart)
├── scripts/
│   ├── reset-system.sh                # Reset état observability
│   ├── test-system.sh                 # Suite de tests
│   └── start-agent-observability-dashboard.sh
├── Tools/
│   └── ManageServer.ts                # Outil gestion TypeScript
└── apps/
    ├── server/                        # Backend
    │   ├── src/
    │   │   ├── index.ts               # Serveur HTTP + WebSocket
    │   │   ├── file-ingest.ts         # Watcher fichiers JSONL
    │   │   ├── task-watcher.ts        # Monitoring tâches background
    │   │   ├── db.ts                  # Base événements in-memory
    │   │   ├── theme.ts               # Définitions thèmes
    │   │   └── types.ts               # Interfaces TypeScript
    │   └── package.json
    └── client/                        # Frontend
        ├── src/
        │   ├── App.vue                # Dashboard principal
        │   ├── components/            # 15+ composants UI
        │   ├── composables/           # Composition utilities Vue
        │   ├── styles/                # Thèmes CSS
        │   ├── utils/                 # Utilitaires
        │   └── types/                 # Types TypeScript
        └── package.json
```

## Port et protocoles

| Service | Port | Protocole | URL |
|---------|------|-----------|-----|
| Dashboard | 4000 | HTTP | `http://localhost:4000` |
| Events API | 4000 | HTTP POST | `http://localhost:4000/events` |
| WebSocket | 4000 | WS | `ws://localhost:4000/ws` |

## Fonctionnalités

- **WebSocket Streaming** : Événements en temps réel
- **Multi-Agent Tracking** : Activité tous agents (main, interns, researchers)
- **Event Timeline** : Vue chronologique opérations
- **Agent Swim Lanes** : Comparaison activité multi-agents
- **Task Monitoring** : Suivi tâches background
- **Thèmes** : Light/dark mode

## Flux de données

```
Hooks (15) → observability.ts (lib) → POST /events → Backend (db.ts)
                                                          ↓
                                                    WebSocket broadcast
                                                          ↓
                                                    Vue 3 Dashboard
```

Les hooks utilisent `lib/observability.ts` pour envoyer des événements au backend via HTTP POST. Le backend stocke en mémoire et diffuse via WebSocket au frontend.

## Gestion du serveur

```bash
# Démarrer
$PAI_DIR/observability/manage.sh start

# Arrêter
$PAI_DIR/observability/manage.sh stop

# Redémarrer
$PAI_DIR/observability/manage.sh restart

# État
$PAI_DIR/observability/manage.sh status
```

## Variable d'environnement

Le endpoint est configurable via :
```
PAI_OBSERVABILITY_URL=http://localhost:4000/events
```

Par défaut dans `settings.json` → `env`.

## Prérequis

- Bun runtime
- Node.js (pour build Vue/Vite)
- Ports 4000 disponible

## Adaptation Linux

Le script `manage.sh` détecte la plateforme :
```bash
# PATH conditionnel (pas de /opt/homebrew/bin sur Linux)
[ -d "/opt/homebrew/bin" ] && export PATH="/opt/homebrew/bin:$PATH"
```

## Diagnostic

```bash
# Vérifier que le serveur tourne
curl -s http://localhost:4000/ > /dev/null && echo "Dashboard OK" || echo "Dashboard DOWN"

# Tester envoi événement
curl -X POST http://localhost:4000/events \
  -H "Content-Type: application/json" \
  -d '{"type":"test","agent":"diagnostic","message":"ping"}'

# Port 4000 utilisé ?
ss -tlnp | grep 4000

# Logs
$PAI_DIR/observability/manage.sh status

# Reset
$PAI_DIR/observability/scripts/reset-system.sh

# Tests
$PAI_DIR/observability/scripts/test-system.sh
```

## Installation dépendances

```bash
# Backend
cd $PAI_DIR/observability/apps/server && bun install

# Frontend
cd $PAI_DIR/observability/apps/client && bun install

# Build frontend
cd $PAI_DIR/observability/apps/client && bun run build
```
