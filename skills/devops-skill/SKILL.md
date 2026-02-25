---
name: devops-skill
description: "DevOps et deploiement : CI/CD, pipelines, git workflows, automatisation, infrastructure as code, environments."
prefix: /devops-*
---

# Super Agent DevOps

Agent intelligent pour les pratiques DevOps du homelab r2d2 : deploiements, pipelines, automatisation, gestion des environnements.

## Philosophie

> "Automatiser tout ce qui est fait plus de deux fois."

## Perimetre

| Domaine | Outils | Usage |
|---------|--------|-------|
| Git workflows | git, GitHub | Branching, PRs, releases |
| Deploiement | docker compose, scripts | Rolling updates, rollback |
| Automatisation | cron, Task Scheduler, scripts | Taches repetitives |
| IaC | docker-compose, shell scripts | Infrastructure declarative |
| Environments | .env, configs | Dev, staging, production |
| Monitoring deploy | Uptime Kuma, Beszel | Verification post-deploy |

## Infrastructure de Deploiement

| VM | Role | Methode de deploy |
|----|------|-------------------|
| 100 r2d2-stage | Staging/Monitoring | docker compose up -d |
| 103 r2d2-main | Production dev | docker compose up -d |
| 104 r2d2-store | Base de donnees | docker compose + migrations |
| 105 r2d2-lab | Lab/Test | docker compose up -d |

## Commandes Slash

### Deploiement

| Commande | Description |
|----------|-------------|
| `/devops-deploy` | Deployer un service (pull, build, up, verify) |
| `/devops-rollback` | Rollback vers la version precedente |
| `/devops-status` | Statut des deploiements recents |

### Git & Workflow

| Commande | Description |
|----------|-------------|
| `/devops-git` | Workflows git (branch, merge, tag, release) |
| `/devops-release` | Preparer et publier une release |

### Automatisation

| Commande | Description |
|----------|-------------|
| `/devops-auto` | Creer/gerer des taches automatisees |
| `/devops-cron` | Gerer les crontabs sur les VMs |
| `/devops-script` | Generer des scripts d'automatisation |

### Infrastructure

| Commande | Description |
|----------|-------------|
| `/devops-env` | Gerer les variables d'environnement |
| `/devops-infra` | Etat de l'infrastructure (VMs, services, sante) |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/devops-wizard deploy` | Deploiement guide d'un nouveau service |
| `/devops-wizard pipeline` | Creation d'un pipeline de deploiement |

## Workflow de Deploiement Standard

```
1. Pre-deploy
   ├── Verifier l'espace disque (df -h)
   ├── Backup pre-deploy (/bak-create)
   └── Notifier debut (ntfy)

2. Deploy
   ├── Pull des images (docker compose pull)
   ├── Arreter les services (docker compose down)
   ├── Appliquer les migrations si necessaire
   └── Demarrer les services (docker compose up -d)

3. Post-deploy
   ├── Verifier les containers (docker ps)
   ├── Health checks (curl endpoints)
   ├── Verifier les logs (docker logs --tail 50)
   └── Notifier fin (ntfy)

4. Rollback si echec
   ├── Restaurer le backup
   ├── Redemarrer l'ancienne version
   └── Analyser les logs d'erreur
```

## Git Workflow (GitFlow Simplifie)

```
main ────────────────────────────────────────►
  │                                    ▲
  └── feature/xxx ── commit ── PR ── merge
  │                                    ▲
  └── fix/xxx ────── commit ── PR ── merge
  │
  └── release/v1.x ── tag ── deploy
```

### Conventions

- **Branches** : `feature/`, `fix/`, `release/`, `hotfix/`
- **Commits** : format conventionnel `type(scope): message`
  - `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- **Tags** : `v{MAJOR}.{MINOR}.{PATCH}` (semver)
- **PRs** : description + test plan + review

## Gestion des Environnements

| Env | VM | Fichier | Usage |
|-----|-----|---------|-------|
| dev | local | .env.dev | Developpement local |
| staging | 100 | .env.staging | Tests pre-production |
| production | 103 | .env.production | Services en production |
| lab | 105 | .env.lab | Experimentation |

### Convention .env

```bash
# .env.{environment}
COMPOSE_PROJECT_NAME=myapp
APP_ENV=production
APP_PORT=8080
DB_HOST=192.168.1.164
DB_PORT=5432
DB_NAME=myapp
DB_USER=myapp
DB_PASSWORD=  # Jamais commit, remplir manuellement
```

## Scripts Utiles

### Deploy rapide

```bash
#!/bin/bash
# deploy.sh - Deploiement standard d'un service Docker
set -euo pipefail

SERVICE=$1
VM_IP=$2

echo "=== Deploying $SERVICE to $VM_IP ==="

# Pre-deploy
ssh root@$VM_IP "cd /opt/$SERVICE && docker compose pull"

# Deploy
ssh root@$VM_IP "cd /opt/$SERVICE && docker compose down && docker compose up -d"

# Verify
sleep 5
ssh root@$VM_IP "cd /opt/$SERVICE && docker compose ps"

echo "=== Deploy complete ==="
```

## Integration avec les Autres Skills

| Skill | Relation |
|-------|----------|
| **docker-skill** | `/dk-compose` pour les operations Docker |
| **backup-skill** | `/bak-create` avant chaque deploiement |
| **monitoring-skill** | `/mon-status` pour verification post-deploy |
| **linux-skill** | `/lx-*` pour les operations systeme |
| **security-skill** | `/sec-audit` avant mise en production |
| **network-skill** | `/net-ports` pour verifier les ports apres deploy |

## Best Practices

- **Backup avant deploy** : toujours un snapshot ou dump avant
- **Rollback plan** : definir la procedure avant de deployer
- **Health checks** : verifier que le service repond apres deploy
- **Logs** : consulter les logs immediatement apres deploy
- **Petit pas** : deployer un service a la fois, pas tout en bloc
- **Idempotent** : les scripts doivent etre rejouables sans risque
- **Secrets** : jamais dans le code, toujours en .env ou Docker secrets
