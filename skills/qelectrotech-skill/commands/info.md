# Analyser un fichier QET

Affiche un rapport detaille sur un projet QElectroTech.

## Actions

1. **Charger** le fichier XML
2. **Extraire et afficher** :

### Informations generales
- Titre du projet
- Version QET
- Date de sauvegarde
- Taille du fichier

### Folios
Pour chaque folio :
- Numero d'ordre et titre
- Dimensions (cols x rows)
- Nombre d'elements places
- Nombre de conducteurs
- Nombre de textes libres
- Nombre de formes (lignes, rectangles...)

### Elements
- Total d'elements places dans tous les folios
- Repartition par type (prises, lampes, interrupteurs...)
- Elements uniques vs repetes
- References `embed://` utilisees

### Collection embarquee
- Nombre de definitions d'elements dans la collection
- Arborescence des categories
- Elements non references (presents dans collection mais non places)
- Elements manquants (references mais absents de la collection)

### Validation UUID
- Verification du format UUID (`{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}`)
- Detection des UUIDs dupliques (elements et terminaux)
- Verification de l'unicite dans tout le projet

### Detection d'anomalies
- **Elements orphelins** : presents dans la collection mais non references par aucun `<element>`
- **Elements manquants** : references par `embed://` mais absents de `<collection>`
- **Coherence cross-references** : verification que chaque slave pointe vers un master existant
- **Conducteurs deconnectes** : conducteurs dont un terminal n'est relie a aucun element

### Resume
```
Projet: Nom
Folios: X | Elements: Y | Conducteurs: Z
Collection: N definitions | Couverture: 100%
UUIDs: N valides | Orphelins: X | Manquants: Y
Cross-refs: N master/slave | Coherence: OK/NOK
```

## Exemple

```
/qet-info "C:\Users\r2d2\Desktop\NELU_ELEC_COMPLET.qet"
/qet-info projet.qet --detailed
```

$ARGUMENTS
