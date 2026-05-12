---
name: mon-logs
description: Logs Docker via Dozzle
---

# /mon-logs - Logs Docker

## Comportement

Dozzle fournit une UI web pour les logs Docker. Cette commande :

1. **Pour consultation rapide** : utiliser `docker logs <container>` via SSH
2. **Pour consultation avancee** : diriger vers Dozzle Web UI

## Usage

- `/mon-logs <container>` : derniers logs d'un container
  ```bash
  ssh root@192.168.1.162 "docker logs --tail 50 <container>"
  ```
- `/mon-logs <container> --follow` : non supporte en CLI, suggerer Dozzle
- `/mon-logs` : lien vers Dozzle UI

## Dozzle Web UI

- URL : http://192.168.1.162:8082
- Fonctionnalites : recherche, filtrage, multi-container, SQL queries sur logs

## Note disambiguation

Si l'utilisateur demande des "logs" dans un contexte monitoring/containers, router ici.
Pour les logs systeme Linux (journalctl, syslog), router vers linux-skill.
