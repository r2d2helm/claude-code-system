# Maintenance quotidienne

Exécute la routine de maintenance quotidienne du système r2d2.

## Checklist

### 1. Health check vault
Exécuter un diagnostic rapide du vault Obsidian :
- Liens cassés
- Notes orphelines
- Frontmatter manquant ou invalide
- Score de santé global

Commande équivalente : `/guardian-health --quick`

### 2. Queue Knowledge Watcher
Vérifier l'état de la queue de traitement :
- Items en attente
- Erreurs récentes
- Statut des watchers (actifs/inactifs)

Commande équivalente : `/kwatch-status`

### 3. Index des notes
Vérifier que l'index est à jour :
- Dernière mise à jour de `notes-index.json`
- Nombre de notes indexées vs notes réelles dans le vault
- Reconstruire si décalage > 5 notes

### 4. Intégrité des skills
Vérification rapide :
- Tous les skills ont un SKILL.md
- Le meta-router référence tous les skills présents
- Pas de commandes orphelines

### 5. Note quotidienne
Créer ou mettre à jour la note quotidienne :
- Chemin : `Knowledge/_Daily/{date-du-jour}.md`
- Template : Template-Daily.md
- Ajouter un résumé des actions de maintenance

## Rapport

```
MAINTENANCE QUOTIDIENNE - [date]
================================

Vault Health:     [score/100] [OK/WARN/FAIL]
Watcher Queue:    [X items] [OK/WARN]
Notes Index:      [X/Y notes] [OK/SYNC NEEDED]
Skills Integrity: [X/11 OK] [OK/FAIL]

Actions effectuées:
- [liste]

Problèmes détectés:
- [liste ou "Aucun"]
```
