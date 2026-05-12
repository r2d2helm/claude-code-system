---
name: intel-opportunities
description: Gerer les Opportunity Cards
---

# /intel-opportunities - Gestion des Opportunity Cards

## Cible : $ARGUMENTS

Gerer le cycle de vie des Opportunity Cards : lister, creer, valider, activer, expirer.

## Actions

### Lister (defaut)

```
/intel-opportunities
```

Afficher toutes les Opportunity Cards actives (status != expired) :

```sql
SELECT * FROM opportunities
WHERE status != 'expired'
ORDER BY urgency DESC, created_at DESC;
```

Format tableau :
```
| ID | Titre | Cat. | Urgence | Valeur | Status | Expire |
|----|-------|------|---------|--------|--------|--------|
```

### Creer

```
/intel-opportunities create
```

Creation manuelle guidee :
1. Demander le titre
2. Demander la categorie
3. Demander l'urgence (1-5)
4. Demander la valeur potentielle estimee
5. Demander la description du marche/opportunite
6. Claude genere automatiquement :
   - Le pitch (argumentaire commercial)
   - Les skills R2D2 necessaires (depuis skill-registry.json)
   - Les leviers financiers (depuis connection-rules.json)
   - La date d'expiration estimee
7. Demander les finding IDs sources (optionnel)
8. Inserer dans la table `opportunities`
9. Creer note vault avec template `templates/opportunity-card.md`

### Valider

```
/intel-opportunities validate <id>
```

Passer une carte de "detected" a "validated" :
1. Lire l'opportunity depuis SQLite
2. Afficher le resume complet
3. Mettre a jour le status
4. Mettre a jour la note vault si elle existe

### Activer

```
/intel-opportunities activate <id>
```

Passer une carte de "validated" a "activated" (action en cours) :
1. Mettre a jour le status
2. Mettre a jour la note vault

### Expirer

```
/intel-opportunities expire <id>
```

Marquer une carte comme expiree :
1. Mettre a jour le status
2. Mettre a jour la note vault

## Contenu d'une Opportunity Card

Chaque carte contient :

- **Titre** : description courte
- **Categorie** : IT_Tech, Business_Reglementaire, Concurrence, Strategique
- **Urgence** : 1-5 (5 = agir immediatement)
- **Valeur potentielle** : estimation revenue/impact
- **Description** : contexte marche, pourquoi c'est une opportunite
- **Pitch** : argumentaire commercial pret a l'emploi (2-3 paragraphes)
- **Skills R2D2** : liste des skills necessaires avec liens
- **Leviers financiers** : subsides, cheques, aides disponibles
- **Findings sources** : IDs des findings qui ont genere cette carte
- **Date d'expiration** : quand l'opportunite se ferme

## Cycle de vie

```
detected -> validated -> activated -> (completed ou expired)
                    \-> expired
```

- **detected** : generee automatiquement par /intel-analyze
- **validated** : Mike confirme que c'est pertinent
- **activated** : action en cours (prospect contacte, pitch envoye)
- **expired** : opportunite passee ou non pertinente

## Exemples

```
/intel-opportunities
/intel-opportunities create
/intel-opportunities validate 7
/intel-opportunities activate 7
/intel-opportunities expire 5
```
