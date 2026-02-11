# Catalogue des elements QET

Affiche le catalogue complet des elements disponibles dans la bibliotheque locale.

## Actions

1. Scanner recursivement `C:\Program Files\QElectroTech\...\elements\`
2. Pour chaque fichier .elmt :
   - Lire le XML pour extraire le nom (lang=fr prioritaire)
   - Compter les terminaux
   - Identifier le type (link_type)
3. Organiser par categorie hierarchique
4. Afficher le catalogue

## Filtres

- **--category** : Filtrer par categorie (architectural, protection, etc.)
- **--type** : Filtrer par link_type (simple, master, slave)
- **--count** : Afficher juste le nombre par categorie

## Sections principales du catalogue

### Residentiel (30_architectural)
78 elements : prises, lampes, interrupteurs, alarme, VDI...

### Protection (200_fuses_protective_gears)
~50 elements : disjoncteurs, differentiels, fusibles, parafoudres...

### Relais/Contacteurs (310_relays_contactors)
Bobines, contacts NO/NC, cross-referencing...

### Borniers (130_terminals)
~50 elements : bornes, barrettes, repartiteurs...

### VDI (25_V.D.I)
Prises RJ45, TV/FM...

## Exemple

```
/qet-element-catalog
/qet-element-catalog --category architectural
/qet-element-catalog --count
```

$ARGUMENTS
