# Generer un Bill of Materials (BOM)

Extrait la nomenclature complete d'un projet QET.

## Actions

1. Charger le fichier .qet
2. Parcourir tous les elements de tous les folios
3. Pour chaque element, extraire les champs elementInformations :
   - Type (depuis embed:// path)
   - Nom lisible (mapping type -> nom francais)
   - `label` : Designation de repere (K1, Q1...)
   - `description` : Description detaillee
   - `designation` : Reference catalogue
   - `manufacturer` : Fabricant
   - `manufacturer_reference` : Reference fabricant
   - `supplier` : Fournisseur
   - `quantity` : Quantite
   - `comment` : Commentaire
   - `function` : Fonction
   - Folio d'appartenance
4. Grouper par type et compter
5. Options de groupement :
   - **Par folio** : Nomenclature par page/schema
   - **Par fabricant** : Regrouper par constructeur
   - **Par localisation** : Regrouper par `plant` / `location`
6. Generer le rapport

## Sources de donnees

- **XML parsing** : Extraction directe des `elementInformations`
- **Export CSV natif** : QET peut exporter une nomenclature via GUI (Projet > Exporter la nomenclature)
- **SQLite interne** : QET utilise une base SQLite pour le cache des elements, consultable pour enrichir les donnees

## Mapping des types courants

| Type fichier | Nom FR | Categorie |
|-------------|--------|-----------|
| pc1.elmt | Prise 2P+T | Appareillage |
| pc2.elmt | Double prise 2P+T | Appareillage |
| pc6.elmt | Bloc 6 prises | Appareillage |
| lampe.elmt | Point lumineux | Eclairage |
| lampe_1.elmt | Applique murale | Eclairage |
| luminaire5.elmt | Luminaire | Eclairage |
| interrupteur_unipolaire.elmt | Interrupteur simple | Commande |
| interrupteur_unipolaire_va_et_vient.elmt | Va-et-vient | Commande |
| bouton_poussoir.elmt | Bouton poussoir | Commande |
| detecteurdemouvement.elmt | Detecteur mouvement | Securite |
| camera.elmt | Camera | Securite |
| sir_int.elmt | Sirene interieure | Securite |
| sir_ext_flash.elmt | Sirene exterieure | Securite |
| prise_rj45_6e_leds.elmt | Prise RJ45 Cat6 | VDI |
| prise_tv_fm.elmt | Prise TV/FM | VDI |
| disjonct-m_1fn.elmt | Disjoncteur 1P+N | Protection |
| interrupteur_differentiel.elmt | Interrupteur diff. 30mA | Protection |
| wattheuremetre.elmt | Compteur electrique | Comptage |
| coffret_de_repartition1.elmt | Tableau electrique | Distribution |

## Format de sortie

```
# Nomenclature - Projet "Nom"
Date: DD/MM/YYYY

## Appareillage
| Ref | Description | Quantite | Folios |
|-----|-------------|----------|--------|
| PC1 | Prise 2P+T simple | 24 | 1,2,3,4,5 |
| PC2 | Double prise 2P+T | 8 | 1,2,4 |
...

## Eclairage
...

## TOTAL
- Appareillage: 45 pieces
- Eclairage: 22 pieces
- Commande: 18 pieces
- Securite: 8 pieces
- VDI: 12 pieces
- Protection: 16 pieces
= TOTAL: 121 elements
```

## Export

- **--csv** : Exporter en CSV (pour Excel/LibreOffice)
- **--clipboard** : Copier dans le presse-papiers

## Exemple

```
/qet-bom "projet.qet"
/qet-bom "projet.qet" --csv "nomenclature.csv"
```

$ARGUMENTS
