# Wizard: Backup Strategy

Aide au choix de la strategie de backup optimale.

## Questions

1. **Budget espace** : Combien d'espace disponible pour les backups ?
2. **RPO** : Combien de donnees pouvez-vous perdre ? (1h, 6h, 24h)
3. **RTO** : En combien de temps devez-vous restaurer ? (15min, 1h, 4h)
4. **Criticite** : Quelles donnees sont les plus critiques ?

## Strategies Predefinies

### Minimale (< 50 GB disponible)

| Cible | Methode | Frequence | Retention |
|-------|---------|-----------|-----------|
| PostgreSQL | pg_dump -Fc | Quotidien | 7 jours |
| Vault Obsidian | git push | A chaque commit | Illimite (git) |
| Config Claude | rsync | Hebdomadaire | 4 semaines |

RPO: 24h | RTO: 1h | Espace: ~10-20 GB

### Standard (50-200 GB disponible) - RECOMMANDEE

| Cible | Methode | Frequence | Retention |
|-------|---------|-----------|-----------|
| VMs critiques (103, 104) | vzdump snapshot | Quotidien | 7j/4sem |
| PostgreSQL | pg_dump -Fc | Toutes les 6h | 7j/4sem/12mois |
| Vault Obsidian | git push | A chaque commit | Illimite |
| Docker volumes | tar + rsync | Hebdomadaire | 4 semaines |
| Config Claude | rsync | Hebdomadaire | 4 semaines |

RPO: 6h | RTO: 30min | Espace: ~50-100 GB

### Complete (> 200 GB disponible)

| Cible | Methode | Frequence | Retention |
|-------|---------|-----------|-----------|
| Toutes VMs (100-105) | vzdump snapshot | Quotidien | 7j/4sem/6mois |
| PostgreSQL | pg_dump -Fc | Toutes les 6h | 7j/4sem/12mois |
| PostgreSQL WAL | archivage continu | Continu | 7 jours |
| Vault Obsidian | git push + rsync | Commit + quotidien | Illimite + 30j |
| Docker volumes | tar + rsync | Quotidien | 7j/4sem |
| Fichiers projets | rsync incremental | Quotidien | 7j/4sem |
| Config systeme | rsync | Quotidien | 30 jours |

RPO: ~0 (WAL) / 6h | RTO: 15min | Espace: ~150-300 GB

## Recommandation pour le Homelab r2d2

Strategie **Standard** avec priorite sur :
1. PostgreSQL (toutes les 6h) - donnees applicatives
2. Vault Obsidian (git) - connaissances
3. VM 103 et 104 (quotidien) - services critiques
4. Config Claude Code (hebdomadaire) - deja en backup manuel

Action immediate : resoudre P2 (disque 74%) avant d'implementer.
