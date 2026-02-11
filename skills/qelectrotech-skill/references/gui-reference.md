# Reference GUI et Limitations QET

> Reference extraite du skill QElectroTech - raccourcis, limitations, exemples

## Raccourcis QElectroTech GUI

| Action | Raccourci |
|--------|-----------|
| Nouveau projet | Ctrl+N |
| Ouvrir | Ctrl+O |
| Sauvegarder | Ctrl+S |
| Annuler | Ctrl+Z |
| Refaire | Ctrl+Y |
| Copier | Ctrl+C |
| Coller | Ctrl+V |
| Supprimer | Suppr |
| Zoom + | Ctrl+Molette haut |
| Zoom - | Ctrl+Molette bas |
| Zoom fit | Ctrl+9 |
| Folio suivant | Ctrl+Tab |
| Folio precedent | Ctrl+Shift+Tab |
| Mode selection | Echap |
| Ajouter texte | T |
| Ajouter ligne | Espace (apres shape) |
| Proprietes element | Double-clic |
| Pivoter element | Espace |
| Imprimer | Ctrl+P |

## Limitations Connues

1. **Pas d'export CLI** : Export PDF/SVG/DXF uniquement via GUI
2. **Pas de layers** : Pas de systeme de calques (verrouiller elements comme workaround)
3. **Pas d'ERC** : Pas de verification de regles electriques automatique
4. **Performance** : Projets > 100 folios peuvent ralentir
5. **Terminal strips** : Fonctionnalite en evolution, pas encore mature
6. **DXF import** : Import basique, convertir en SVG d'abord pour meilleur resultat

## Exemples Inclus

| Fichier | Description |
|---------|-------------|
| `Habitat-Unifilaire.qet` | Plan unifilaire domestique (reference) |
| `Habitat-Schemas_developpes.qet` | Schemas developpes domestique |
| `tableau_domestique.qet` | Tableau electrique maison |
| `industrial.qet` | Schema industriel |
| `photovoltaique.qet` | Installation solaire |
| `Projet_vierge.qet` | Projet vide (template) |
