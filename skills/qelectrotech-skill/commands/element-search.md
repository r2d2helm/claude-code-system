# Chercher un element dans la bibliotheque QET

Recherche dans la bibliotheque d'elements installee localement.

## Parametres

- **Terme** : Mot-cle de recherche (nom fichier ou contenu)
- **Categorie** : Filtrer par categorie (architectural, protection, etc.)
- **Langue** : Langue de recherche pour les noms (fr, en, de, etc.)

## Actions

1. **Scanner la bibliotheque** :
   - Chemin : `C:\Program Files\QElectroTech\qelectrotech-0.100.1+git8595-x86-win64-readytouse\elements\`
   - Rechercher dans les noms de fichiers .elmt
   - Rechercher dans le contenu XML (balises `<name>`)

2. **Afficher les resultats** :
   - Nom de l'element (multilangue)
   - Chemin complet dans la bibliotheque
   - Chemin embed:// pour reference dans un projet
   - Nombre de terminaux
   - Type (simple, master, slave)

## Categories principales

| Chemin | Description |
|--------|-------------|
| `10_electric/10_allpole/` | Schemas multipolaires |
| `10_electric/11_singlepole/` | Schemas unifilaires |
| `10_electric/11_singlepole/500_home_installation/30_architectural/` | **Symboles archi residentiels** |
| `10_electric/10_allpole/200_fuses_protective_gears/` | Protections |
| `10_electric/10_allpole/310_relays_contactors_contacts/` | Relais/Contacteurs |
| `10_electric/10_allpole/130_terminals_terminal_strips/` | Borniers |

## Exemple

```
/qet-element-search "prise"
/qet-element-search "disjoncteur" --category protection
/qet-element-search "lamp" --lang en
```

$ARGUMENTS
