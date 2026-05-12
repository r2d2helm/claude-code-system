---
name: wizard-cross-ref
description: Assistant interactif de cross-referencing
---

# Wizard : Cross-Referencing Interactif

## Declencheur

```
/intel-wizard cross-ref
```

## Description

Assistant interactif pour explorer les connexions entre findings et decouvrir des patterns caches. Ideal quand Mike veut creuser un sujet specifique.

## Etapes

### Etape 1 : Choisir le point de depart

Proposer 3 options :
1. **Par finding** : entrer un ID ou chercher par titre
2. **Par tag** : choisir parmi les top 10 tags
3. **Par entite** : choisir parmi les entites les plus frequentes

### Etape 2 : Afficher le contexte

Pour le point de depart choisi, afficher :
- Le finding (ou les findings lies au tag/entite)
- Ses connexions existantes
- Son score Seldon
- Les opportunities/threats liees

### Etape 3 : Explorer les connexions

Pour chaque connexion :
- Afficher le finding lie
- Afficher le type et la force de connexion
- Demander si Mike veut creuser cette branche

Mode interactif :
```
## Finding #42 : Migration VMware Broadcom (4/5)

Connexions :
  1. -> #38 "Proxmox 9.0 release" [thematic, 0.6]
  2. -> #35 "Cheque cyber Wallonie" [causal, 0.9]
  3. -> #44 "ESN belges en difficulte" [complementary, 0.7]

Quel lien explorer ? (1-3, 'n' pour nouvelle recherche, 'a' pour analyser le cluster)
```

### Etape 4 : Analyse du cluster

Quand Mike choisit 'a' ou apres avoir explore :
1. Identifier le cluster complet (tous les findings connectes)
2. Calculer le score moyen
3. Identifier les themes dominants
4. Verifier skill-registry.json : quels skills R2D2 sont pertinents
5. Verifier les leviers financiers

### Etape 5 : Decision

Proposer les actions possibles :
1. **Creer une Opportunity Card** si le cluster montre une convergence
2. **Creer un Threat Alert** si le cluster montre une menace
3. **Ajouter des connexions manuelles** si Claude detecte des liens non captures
4. **Exporter** le cluster pour le R2D2 Agent
5. **Continuer l'exploration** avec un autre point de depart

### Etape 6 : Boucle

Revenir a l'etape 1 tant que Mike veut continuer.

## Exemples d'utilisation

```
/intel-wizard cross-ref

> Point de depart ? (1) Finding (2) Tag (3) Entite
> 2
> Choisir un tag :
> 1. cybersecurite (12)
> 2. VMware (8)
> 3. souverainete (7)
> ...
> 2

> 3 findings avec le tag "VMware" :
> #38 "Proxmox 9.0 release" (4/5)
> #42 "Migration VMware Broadcom" (4/5)
> #44 "ESN belges en difficulte VMware" (4/5)
>
> Connexions entre eux :
> #38 <-> #42 (thematic, 0.6)
> #42 <-> #44 (complementary, 0.7)
>
> Et aussi connecte a :
> #35 "Cheque cyber Wallonie" (causal, 0.9)
>
> Explorer (1-4), analyser cluster (a), nouvelle recherche (n) ?
> a
>
> ## Analyse du cluster "VMware"
> - 4 findings, score moyen 4.2
> - Skills pertinents : proxmox-skill, backup-skill, security-skill
> - Levier : Cheque Cybersecurite 75% (60k EUR)
> - CONVERGENCE DETECTEE
>
> Creer une Opportunity Card ? (o/n)
```
