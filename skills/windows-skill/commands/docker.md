# Gestion Docker Desktop

Administration de Docker Desktop sur Windows.

## Mode d'Utilisation
```
/docker                     → État général Docker
/docker ps                  → Conteneurs en cours d'exécution
/docker images              → Liste des images
/docker logs "container"    → Logs d'un conteneur
/docker stats               → Statistiques temps réel
/docker compose             → Gestion Docker Compose
/docker cleanup             → Nettoyage (images/conteneurs/volumes)
/docker network             → Configuration réseau Docker
/docker volumes             → Gestion des volumes
/docker troubleshoot        → Dépannage Docker Desktop
```

Arguments: $ARGUMENTS

---

## État Général (défaut)

```
🐳 DOCKER DESKTOP - ÉTAT GÉNÉRAL
═══════════════════════════════════════════════════════════════

STATUT:
├─ Docker Desktop: ✅ Running
├─ Docker Engine: ✅ v24.0.7
├─ Compose: ✅ v2.23.3
├─ Backend: WSL 2 (Ubuntu)
└─ Kubernetes: ❌ Désactivé

RESSOURCES:
├─ CPU: 4 cores alloués
├─ RAM: 8 GB allouée
├─ Disk: 64 GB (42 GB utilisés)
└─ Swap: 2 GB

CONTENEURS:
┌─────────────────────┬──────────────────┬──────────┬───────────┐
│ Nom                 │ Image            │ État     │ Ports     │
├─────────────────────┼──────────────────┼──────────┼───────────┤
│ postgres-db         │ postgres:15      │ ✅ Up    │ 5432      │
│ redis-cache         │ redis:7-alpine   │ ✅ Up    │ 6379      │
│ nginx-proxy         │ nginx:latest     │ ✅ Up    │ 80, 443   │
│ api-backend         │ myapp/api:v2     │ ✅ Up    │ 3000      │
│ worker-1            │ myapp/worker     │ ⏹️ Exited│ -         │
└─────────────────────┴──────────────────┴──────────┴───────────┘

RÉSUMÉ:
├─ Conteneurs: 5 (4 running, 1 stopped)
├─ Images: 23 (8.5 GB)
├─ Volumes: 12 (15 GB)
└─ Networks: 5

ALERTES:
├─ ⚠️ worker-1 arrêté (exit code 137 - OOM)
└─ ℹ️ 8 images dangling (3 GB récupérables)
```

---

## Mode `ps`

```
📦 CONTENEURS DOCKER
═══════════════════════════════════════════════════════════════

EN COURS:
┌────────────────────────────────────────────────────────────────────────┐
│ 🟢 postgres-db                                                         │
│ Image: postgres:15-alpine | ID: a1b2c3d4                              │
│ Ports: 0.0.0.0:5432->5432/tcp                                         │
│ Uptime: 2 jours | CPU: 2.3% | RAM: 256/512 MB                         │
├────────────────────────────────────────────────────────────────────────┤
│ 🟢 redis-cache                                                         │
│ Image: redis:7-alpine | ID: b2c3d4e5                                  │
│ Ports: 0.0.0.0:6379->6379/tcp                                         │
│ Uptime: 2 jours | CPU: 0.5% | RAM: 45/256 MB                          │
├────────────────────────────────────────────────────────────────────────┤
│ 🟢 api-backend                                                         │
│ Image: myapp/api:v2 | ID: c3d4e5f6                                    │
│ Ports: 0.0.0.0:3000->3000/tcp                                         │
│ Uptime: 5h | CPU: 15% | RAM: 512/1024 MB                              │
└────────────────────────────────────────────────────────────────────────┘

ARRÊTÉS:
┌────────────────────────────────────────────────────────────────────────┐
│ 🔴 worker-1 | Exit Code: 137 (OOMKilled)                              │
│ Arrêté: 2026-02-03 03:45 | Suggestion: Augmenter limite mémoire       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Mode `images`

```
🖼️ IMAGES DOCKER
═══════════════════════════════════════════════════════════════

UTILISÉES:
┌─────────────────────────────┬───────────┬────────────┐
│ Repository:Tag              │ Taille    │ Créée      │
├─────────────────────────────┼───────────┼────────────┤
│ postgres:15-alpine          │ 238 MB    │ 2 semaines │
│ redis:7-alpine              │ 32 MB     │ 3 semaines │
│ nginx:1.25-alpine           │ 43 MB     │ 1 mois     │
│ myapp/api:v2                │ 456 MB    │ 5 heures   │
│ myapp/worker:latest         │ 389 MB    │ 1 jour     │
└─────────────────────────────┴───────────┴────────────┘

DANGLING (non utilisées):
├─ <none>:<none> - 1.2 GB (3 jours)
├─ <none>:<none> - 890 MB (5 jours)
├─ myapp/api:v1 - 445 MB (1 semaine)
└─ Total récupérable: 3.0 GB

💡 /docker cleanup images pour libérer l'espace
```

---

## Mode `stats`

```
📊 STATISTIQUES TEMPS RÉEL
═══════════════════════════════════════════════════════════════

┌─────────────────┬────────┬─────────────────┬─────────────────┐
│ CONTAINER       │ CPU %  │ MEM / LIMIT     │ NET I/O         │
├─────────────────┼────────┼─────────────────┼─────────────────┤
│ postgres-db     │ 2.34%  │ 256 MB / 512 MB │ 45 MB / 12 MB   │
│ redis-cache     │ 0.45%  │ 45 MB / 256 MB  │ 123 MB / 98 MB  │
│ nginx-proxy     │ 0.12%  │ 12 MB / 128 MB  │ 2.3 GB / 2.1 GB │
│ api-backend     │ 15.67% │ 512 MB / 1 GB   │ 890 MB / 1.2 GB │
└─────────────────┴────────┴─────────────────┴─────────────────┘

Total: CPU 18.58% | RAM 825 MB / 8 GB
```

---

## Mode `compose`

```
🐙 DOCKER COMPOSE
═══════════════════════════════════════════════════════════════

PROJETS:
┌────────────────────┬────────────────────────────┬───────────┐
│ Projet             │ Chemin                     │ État      │
├────────────────────┼────────────────────────────┼───────────┤
│ myapp              │ C:\Projects\myapp          │ 4/5 Up    │
│ monitoring         │ C:\Projects\monitoring     │ 3/3 Up    │
│ dev-tools          │ C:\Projects\dev-tools      │ 0/2 Down  │
└────────────────────┴────────────────────────────┴───────────┘

ACTIONS:
├─ docker compose up -d        → Démarrer
├─ docker compose down         → Arrêter
├─ docker compose logs -f      → Voir logs
├─ docker compose pull         → Mettre à jour images
└─ docker compose build        → Reconstruire
```

---

## Mode `cleanup`

```
🧹 NETTOYAGE DOCKER
═══════════════════════════════════════════════════════════════

ESPACE RÉCUPÉRABLE:
├─ Images dangling: 3.0 GB
├─ Conteneurs arrêtés: 450 MB
├─ Volumes orphelins: 2.3 GB
├─ Build cache: 4.2 GB
└─ TOTAL: 10.0 GB

OPTIONS:
1. [safe] Nettoyage sûr (~3.5 GB)
   Images dangling + conteneurs > 24h

2. [moderate] Modéré (~6.0 GB)
   + Images non utilisées > 7 jours + volumes orphelins

3. [aggressive] Agressif (~10.0 GB) ⚠️
   Tout ce qui n'est pas actuellement utilisé

Choix: _
```

---

## Mode `troubleshoot`

```
🔧 DÉPANNAGE DOCKER DESKTOP
═══════════════════════════════════════════════════════════════

VÉRIFICATIONS:
├─ Docker Desktop: ✅ Running
├─ Docker daemon: ✅ Responding
├─ WSL 2 backend: ✅ OK
├─ Virtualisation: ✅ Activée
├─ Espace disque: ✅ 22 GB libre
├─ Réseau Docker: ✅ OK
└─ Hub Docker: ✅ Accessible

PROBLÈMES COURANTS:
1. "Cannot connect to daemon" → Redémarrer Docker Desktop
2. "No space left" → /docker cleanup
3. "Port already in use" → netstat -ano | findstr :PORT
4. Conteneurs lents → Vérifier ressources allouées

RÉSULTAT: ✅ Aucun problème détecté
```

---

## Commandes de Référence

```powershell
# Conteneurs
docker ps -a
docker logs -f <container>
docker exec -it <container> /bin/sh
docker stats

# Images
docker images
docker pull <image>
docker build -t <name> .

# Compose
docker compose up -d
docker compose down
docker compose logs -f

# Nettoyage
docker system prune -a --volumes
docker image prune -a
docker volume prune
```
