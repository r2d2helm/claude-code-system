# Wizard: Press Review Setup

Assistant de configuration initiale de la revue de presse.

## Questions

1. **Categories** : Quelles categories activer ?
   - [ ] IT / Tech (IA, securite, open source)
   - [ ] Business / Reglementaire (subsides, reglementation)
   - [ ] Concurrence (ESN, MSP, integrateurs)
   - [ ] Strategique (Big Tech, souverainete, geopolitique)
   - Default : toutes

2. **Frequence** : A quelle frequence faire la revue ?
   - Quotidien (`/press-review` chaque matin)
   - Hebdo (`/press-review --days=7` + `/press-digest weekly`)
   - A la demande
   - Default : a la demande

3. **Sources supplementaires** : Ajouter des sources specifiques ?
   - URL de sites a surveiller
   - Requetes de recherche personnalisees
   - Default : sources pre-configurees dans sources.json

4. **Scoring** : Personnaliser les mots-cles Seldon ?
   - Ajouter des mots-cles haute pertinence
   - Ajouter des boosters contextuels
   - Default : keywords pre-configures dans seldon-keywords.json

5. **Vault** : Confirmer le chemin de sortie
   - Default : `C:\Users\r2d2\Documents\Knowledge\References\`

## Processus de setup

### 1. Verifier les prerequis

- Confirmer acces au vault Obsidian
- Verifier que les fichiers data/ existent (sinon les creer)
- Tester un WebSearch simple pour confirmer la connectivite

### 2. Personnaliser les sources

Si l'utilisateur veut ajouter des sources :
- Ajouter dans `data/sources.json`
- Tester l'accessibilite de chaque URL

### 3. Personnaliser le scoring

Si l'utilisateur veut ajouter des mots-cles :
- Ajouter dans `data/seldon-keywords.json`
- Afficher un apercu du scoring modifie

### 4. Premier scan test

- Lancer un `/press-quick` pour valider la configuration
- Afficher les resultats
- Demander confirmation

### 5. Confirmer

```
=== Configuration Press Review ===

Categories actives : IT, Business, Concurrence, Strategique
Sources : 13 requetes + 7 sites
Mots-cles Seldon : 13 haute + 8 moyenne + 6 boosters
Sortie vault : Knowledge/References/

Configuration sauvegardee. Utilisez :
  /press-quick    pour un scan rapide
  /press-review   pour une revue complete
```
