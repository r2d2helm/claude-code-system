---
name: mon-containers
description: Stats Docker par conteneur
---

# /mon-containers - Stats Containers Docker

## Comportement

1. **Appeler `beszel_containers`** via MCP
2. Afficher pour chaque container : nom, CPU%, RAM (MB), etat
3. Trier par CPU decroissant par defaut

## Options

- `/mon-containers` : tous les containers de tous les systemes
- `/mon-containers vm100` : containers d'un systeme specifique
- `/mon-containers --sort ram` : trier par RAM

## Format de sortie

```
# Docker Containers - vm100

| Container | CPU | RAM | State |
|-----------|-----|-----|-------|
| multipass-api | 15.2% | 256 MB | running |
| taskyn-core | 8.1% | 128 MB | running |
```

## Note disambiguation

Si l'utilisateur mentionne "containers" dans un contexte monitoring (metriques, stats, performance), router ici.
Pour les operations Docker (start, stop, exec, build), router vers docker-skill.
