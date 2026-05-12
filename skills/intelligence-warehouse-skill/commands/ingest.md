---
name: intel-ingest
description: Ingerer des trouvailles dans le warehouse
---

# /intel-ingest - Ingestion de trouvailles

## Cible : $ARGUMENTS

Ingere des trouvailles (findings) dans le warehouse SQLite. Trois modes d'ingestion disponibles.

## Modes

### Mode 1 : Depuis press-review (--from-press-review)

```
/intel-ingest --from-press-review
```

1. Chercher la derniere note Press-Review dans le vault :
   - Chemin : `C:\Users\r2d2\Documents\Knowledge\References\`
   - Pattern : `YYYY-MM-DD_Press-Review*.md`
   - Prendre la plus recente

2. Parser la note markdown :
   - Extraire chaque article (titre, URL, source, categorie, resume, points cles, score Seldon)
   - Les articles sont structures en sections par categorie

3. Pour chaque article extrait :
   - Verifier s'il existe deja (doublon par URL ou titre similaire)
   - Extraire les entites (entreprises, technologies) du texte
   - Extraire les tags du texte
   - Inserer dans la table `findings`

4. Lancer la detection de connexions (voir etape commune)

### Mode 2 : Manuel (sans argument)

```
/intel-ingest
```

1. Demander a Mike de coller un article ou du texte brut
2. Analyser le texte avec Claude :
   - Extraire : titre, source, URL (si presente), categorie
   - Generer : resume (3-5 phrases), points cles (liste), score Seldon
   - Extraire : entites, tags
3. Inserer dans la table `findings` avec `source_type = 'manual'`
4. Lancer la detection de connexions

### Mode 3 : Depuis vault (--from-vault <path>)

```
/intel-ingest --from-vault C:\Users\r2d2\Documents\Knowledge\References\ma-note.md
```

1. Lire la note vault specifiee
2. Extraire le frontmatter (title, date, tags, type)
3. Analyser le contenu pour generer resume, points cles, score Seldon
4. Inserer dans `findings` avec `source_type = 'vault'` et `vault_note_path`
5. Lancer la detection de connexions

## Etape commune : Detection de connexions

Apres chaque ingestion, pour chaque nouveau finding :

1. Charger `data/connection-rules.json`
2. Recuperer les 20 derniers findings de la DB
3. Appliquer chaque regle :
   - **shared_tags** : comparer les tags JSON (similarite Jaccard >= 0.3)
   - **same_entity** : comparer les entites extraites
   - **temporal_proximity** : meme semaine + meme categorie
   - **complementary_categories** : paires IT/Business, etc.
   - **opportunity_trigger** : score 4-5 + mots-cles financiers
4. Inserer les connexions detectees dans la table `connections`

## Etape optionnelle : Note vault

Si le finding a un score >= 3, proposer de creer une note vault :
- Chemin : `Knowledge/References/Intel/YYYY-MM-DD_Intel_{title-slug}.md`
- Utiliser le template `templates/finding-note.md`

## Format de sortie

```
## Finding ingere

- **ID** : #42
- **Titre** : Migration VMware : Broadcom pousse les PME vers la sortie
- **Categorie** : IT_Tech
- **Score Seldon** : 4/5
- **Tags** : VMware, migration, Proxmox, lock-in
- **Entites** : Broadcom, VMware, Proxmox

## Connexions detectees

| Connexion | Avec | Type | Force |
|-----------|------|------|-------|
| #42 <-> #38 | "Proxmox 9.0 release" | thematic | 0.6 |
| #42 <-> #35 | "Cheque cyber Wallonie" | causal | 0.9 |

Note vault creee : Knowledge/References/Intel/2026-03-25_Intel_Migration-VMware-Broadcom.md
```

## Exemples

```
/intel-ingest --from-press-review
/intel-ingest
/intel-ingest --from-vault C:\Users\r2d2\Documents\Knowledge\References\2026-03-25_Press-Review.md
```
