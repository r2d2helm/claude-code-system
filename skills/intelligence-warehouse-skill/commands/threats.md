---
name: intel-threats
description: Gerer les Threat Alerts
---

# /intel-threats - Gestion des Threat Alerts

## Cible : $ARGUMENTS

Gerer les Threat Alerts : lister, creer, mitiger.

## Actions

### Lister (defaut)

```
/intel-threats
```

Afficher toutes les alertes actives :

```sql
SELECT * FROM threats
WHERE status = 'active'
ORDER BY severity DESC, created_at DESC;
```

Format :
```
| ID | Titre | Cat. | Severite | Cree le | Status |
|----|-------|------|----------|---------|--------|
```

### Creer

```
/intel-threats create
```

Creation manuelle guidee :
1. Demander le titre de la menace
2. Demander la categorie
3. Demander la severite (1-5)
4. Demander la description
5. Claude propose une strategie de mitigation
6. Demander les finding IDs sources (optionnel)
7. Inserer dans la table `threats`
8. Creer note vault : `Knowledge/References/Intel/THR-{id}_{title-slug}.md`

### Mitiger

```
/intel-threats mitigate <id>
```

Marquer une menace comme mitigee :
1. Lire le threat depuis SQLite
2. Demander la description de la mitigation appliquee
3. Mettre a jour le champ `mitigation` et le status
4. Mettre a jour la note vault

## Types de menaces typiques

| Type | Exemples | Severite typique |
|------|----------|------------------|
| **Securite** | CVE critique, malware, breach | 4-5 |
| **Concurrence** | Nouveau concurrent, offre agressive | 2-3 |
| **Reglementaire** | Nouvelle loi contraignante, deadline | 3-4 |
| **Lock-in** | Vendor lock-in, prix en hausse | 3-4 |
| **Technique** | Deprecation, fin de support | 2-3 |

## Cycle de vie

```
active -> mitigated
       -> expired (automatique apres 90 jours sans action)
```

## Exemples

```
/intel-threats
/intel-threats create
/intel-threats mitigate 3
```
