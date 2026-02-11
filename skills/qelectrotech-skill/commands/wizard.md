# Assistant QElectroTech

Lance un wizard interactif pour un projet electrique.

## Wizards disponibles

| Wizard | Commande | Etapes | Description |
|--------|----------|--------|-------------|
| Residential | `/qet-wizard residential` | 8 | Projet maison complete |
| Panel | `/qet-wizard panel` | 6 | Tableau electrique |
| Renovation | `/qet-wizard renovation` | 5 | Mise aux normes |
| Extension | `/qet-wizard extension` | 4 | Ajout circuit |
| Tertiaire | `/qet-wizard tertiaire` | 7 | Bureau/Commerce |
| Outdoor | `/qet-wizard outdoor` | 4 | Exterieur/Jardin |
| Industrial | `/qet-wizard industrial` | 7 | Installation industrielle (moteurs, VFD, automate) |
| Photovoltaic | `/qet-wizard photovoltaic` | 6 | Installation solaire (autoconso/revente/hybride) |
| EV Charger | `/qet-wizard ev-charger` | 5 | Borne de recharge IRVE (domestique/copro/pro) |

## Fonctionnement

Chaque wizard charge le fichier correspondant dans `wizards/` :
- `wizard-residential.md`
- `wizard-panel.md`
- `wizard-renovation.md`
- `wizard-extension.md`
- `wizard-tertiaire.md`
- `wizard-outdoor.md`
- `wizard-industrial.md`
- `wizard-photovoltaic.md`
- `wizard-ev-charger.md`

## Exemple

```
/qet-wizard residential
/qet-wizard panel
/qet-wizard industrial
/qet-wizard photovoltaic
/qet-wizard ev-charger
```

$ARGUMENTS
