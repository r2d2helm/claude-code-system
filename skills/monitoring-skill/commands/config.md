---
name: mon-config
description: Configuration de la stack monitoring
---

# /mon-config - Configuration

## Comportement

Affiche la configuration actuelle de la stack monitoring et permet de la modifier.

## Fichiers de configuration

| Fichier | Localisation | Role |
|---------|-------------|------|
| docker-compose.yml | /opt/monitoring/ | Definition des services |
| .env | /opt/monitoring/ | Variables (cle agent) |
| server.yml | /opt/monitoring/ntfy/ | Config ntfy |
| MCP beszel | ~/.claude.json | Config MCP Beszel |
| MCP netdata | ~/.claude.json | Config MCP Netdata |

## Operations

- `/mon-config show` : affiche la configuration actuelle
- `/mon-config ports` : liste les ports utilises
- `/mon-config restart <service>` : redemarre un service monitoring

## Ports utilises

| Service | Port | Protocole |
|---------|------|-----------|
| Beszel Hub | 8091 | HTTP |
| Beszel Agent | 45876 | SSH |
| Netdata | 19999 | HTTP |
| Uptime Kuma | 3003 | HTTP |
| Dozzle | 8082 | HTTP |
| ntfy | 8084 | HTTP |
