# Commande: /press-sources

Gerer les sources de veille (lister, ajouter, supprimer, activer/desactiver).

## Syntaxe

```
/press-sources <action> [arguments]
```

## Actions

### list -- Lister les sources

```
/press-sources list
/press-sources list --category=IT
```

Affiche un tableau des sources par categorie :

```
=== Sources de veille ===

--- IT / Tech (5 requetes, 3 sites) ---
  Requetes :
    1. "actualites IA LLM agents 2026"
    2. "CVE critiques vulnerabilites"
    3. "Docker Proxmox open source updates"
    4. "souverainete numerique Europe local-first"
    5. "Claude Anthropic Mistral actualites"
  Sites :
    [cert-be]        CERT-BE           https://cert.be/fr/advisories        ACTIF
    [lemagit]        LeMagIT           https://www.lemagit.fr               ACTIF
    [usine-digitale] L'Usine Digitale  https://www.usine-digitale.fr        ACTIF

--- Business / Reglementaire (5 requetes, 2 sites) ---
  ...
```

### add -- Ajouter une source

```
/press-sources add <url> --category=<categorie> --name=<nom> [--id=<id>]
```

| Argument | Description | Requis |
|----------|-------------|--------|
| `<url>` | URL du site source | Oui |
| `--category` | IT, Business, Concurrence, Strategique | Oui |
| `--name` | Nom affiche de la source | Oui |
| `--id` | Identifiant unique (auto-genere si absent) | Non |

Processus :
1. Valider que l'URL est accessible (WebFetch rapide)
2. Generer un ID si non fourni (slugify du nom)
3. Ajouter dans `data/sources.json` sous la categorie
4. Source activee par defaut

### remove -- Supprimer une source

```
/press-sources remove <id>
```

Processus :
1. Chercher la source par ID dans toutes les categories
2. Confirmer la suppression
3. Retirer de `data/sources.json`

### enable / disable -- Activer/desactiver

```
/press-sources enable <id>
/press-sources disable <id>
```

Processus :
1. Chercher la source par ID
2. Basculer le champ `enabled` dans `data/sources.json`
3. Confirmer le changement

### add-query -- Ajouter une requete de recherche

```
/press-sources add-query "<requete>" --category=<categorie>
```

Ajoute une requete WebSearch dans les `search_queries` de la categorie.

### remove-query -- Supprimer une requete

```
/press-sources remove-query <index> --category=<categorie>
```

Supprime la requete a l'index donne (base 1).

## Exemples

### Ajouter Ars Technica en source IT
```
/press-sources add https://arstechnica.com --category=IT --name="Ars Technica"
```

### Desactiver temporairement Sortlist
```
/press-sources disable sortlist
```

### Ajouter une requete business
```
/press-sources add-query "aides digitalisation PME Flandre 2026" --category=Business
```
