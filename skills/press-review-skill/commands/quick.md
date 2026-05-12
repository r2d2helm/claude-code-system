# Commande: /press-quick

Scan rapide de la presse -- titres et liens uniquement, sans note vault.

## Syntaxe

```
/press-quick [--category=IT|Business|Concurrence|Strategique]
```

## Arguments

| Argument | Description | Defaut |
|----------|-------------|--------|
| `--category` | Filtrer sur une seule categorie | Toutes |

## Processus

### 1. Charger les requetes de recherche

- Lire `data/sources.json` pour les `search_queries` de chaque categorie
- Filtrer si `--category` specifie

### 2. Scanner (WebSearch uniquement)

- 1 seul WebSearch par categorie (la requete principale)
- Pas de WebFetch (pas d'approfondissement)
- Collecter : titre, URL, snippet, source
- Duree cible : < 30 secondes

### 3. Afficher le tableau console

```
=== Scan Rapide - 2026-03-25 ===

--- IT / Tech ---
  [1] Docker Engine 27.5 : nouvelles features securite
      https://www.docker.com/blog/...
  [2] Claude 4 : Anthropic annonce des agents autonomes
      https://www.anthropic.com/...

--- Business / Reglementaire ---
  [3] Cheque cybersecurite Wallonie : budget 2026 augmente
      https://www.digitalwallonia.be/...

--- Concurrence ---
  [4] Neurones IT ouvre un bureau a Bruxelles
      https://www.journaldunet.com/...

--- Strategique ---
  [5] CLOUD Act : l'Europe reagit avec un nouveau cadre
      https://www.politico.eu/...

Resultats : 12 articles | Duree : 18s
Tip: /press-review pour analyse complete avec scoring
```

### 4. Pas de persistance

- Pas de note vault
- Pas d'ecriture dans history.json
- Pas de scoring Seldon
- Mode consultation pure

## Exemples

### Scan rapide complet
```
/press-quick
```

### Scan rapide IT uniquement
```
/press-quick --category=IT
```
