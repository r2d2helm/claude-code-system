# Wizard Photovoltaique - Installation Solaire

Assistant interactif pour creer un projet d'installation photovoltaique.

## Etapes

### Etape 1 : Type d'installation

Demander a l'utilisateur :

| Option | Description |
|--------|-------------|
| Autoconsommation | Production pour usage propre, surplus injecte |
| Revente totale | Toute la production est vendue (raccordement dedie) |
| Hybride (avec batterie) | Stockage + autoconsommation + injection |
| Site isole | Pas de raccordement reseau (off-grid) |

- **Puissance crete** : kWc (ex: 3, 6, 9, 36 kWc)
- **Monophase ou triphase** : selon puissance et raccordement

### Etape 2 : Composants

#### Panneaux solaires
- Nombre et puissance unitaire (ex: 10 x 400Wc)
- Configuration : serie (string) et parallele
- Tension Voc et courant Isc du string

#### Onduleur(s)
- Type : string, micro-onduleur, hybride
- Puissance nominale (kVA)
- Nombre de MPPT
- Fabricant (SMA, Fronius, Huawei, Enphase, SolarEdge...)

#### Batterie (si hybride)
- Capacite (kWh)
- Technologie (Li-ion, LFP)
- Onduleur/chargeur integre ou separe

### Etape 3 : Protection DC (cote panneaux)

Generer le schema DC :
- Connecteurs MC4
- Sectionneur DC (par string)
- Parafoudre DC (type 2)
- Fusibles string (si parallele > 2 strings)
- Cable solaire (section selon courant et longueur)

### Etape 4 : Protection AC (cote reseau)

Generer le schema AC :
- Disjoncteur AC dedie (calibre selon puissance onduleur)
- Differentiel 30mA type A (ou type B si onduleur sans transformateur)
- Parafoudre AC type 2
- Compteur de production (si revente)
- Raccordement au TGBT ou coffret dedie

### Etape 5 : Schema unifilaire

Generer le schema unifilaire complet :

```
Panneaux [Voc x Isc] → Sectionneur DC → Parafoudre DC → Onduleur
                                                              ↓
Reseau ← Compteur ← Disj. AC ← Diff 30mA ← Parafoudre AC ←┘
                                                              ↓
                                                         Batterie (si hybride)
```

### Etape 6 : Generation du projet

1. Creer le fichier .qet avec folios :
   - Page de garde
   - Schema unifilaire general
   - Schema DC detaille (strings, protections)
   - Schema AC detaille (onduleur, protections, raccordement)
   - Schema batterie (si hybride)
   - Integration TGBT
   - Nomenclature
2. Sauvegarder et proposer d'ouvrir

## Reference QET

Le projet QET inclut un exemple de reference : `photovoltaique.qet` dans le dossier `examples/`.

## Normes applicables

- NF C 15-100 : Installation BT
- UTE C 15-712-1 : Installations photovoltaiques raccordees au reseau
- UTE C 15-712-2 : Installations PV en site isole
- Guide ENEDIS IRVE/PV pour le raccordement

## Exemple

```
/qet-wizard photovoltaic
/qet-wizard photovoltaic --power 6kWc --type autoconso
/qet-wizard photovoltaic --power 9kWc --type hybride --battery 10kWh
```

$ARGUMENTS
