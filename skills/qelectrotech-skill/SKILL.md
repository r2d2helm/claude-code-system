# Agent QElectroTech - Plans Electriques Professionnels

Agent specialise dans la creation, administration et manipulation de plans electriques avec QElectroTech (QET) 0.100.x. Competences en schemas unifilaires residentiels, tableaux electriques, normes IEC 60617 et NF C 15-100.

## Environnement

| Composant | Valeur |
|-----------|--------|
| QElectroTech | 0.100.1 (git8595) |
| Chemin | `C:\Program Files\QElectroTech\qelectrotech-0.100.1+git8595-x86-win64-readytouse\` |
| Executable | `bin\qelectrotech.exe` |
| Elements | `elements\` (bibliotheque systeme) |
| Titleblocks | `titleblocks\` (cartouches) |
| Exemples | `examples\` (projets de reference) |
| Format | `.qet` (XML, UTF-8) |
| Elements | `.elmt` (XML, definitions graphiques) |
| Cartouches | `.titleblock` (XML, templates) |

## Chemins et Collections

### Types de collections

| Prefixe | Description | Emplacement |
|---------|-------------|-------------|
| `common://` | Collection systeme (lecture seule) | `<install>/elements/` |
| `custom://` | Collection utilisateur | `C:\Users\<user>\Application Data\qet\elements\` |
| `embed://` | Collection embarquee dans le projet | `<project>/collection/` |

### Flags CLI

| Flag | Description |
|------|-------------|
| `--common-elements-dir` | Chemin vers la collection systeme |
| `--config-dir` | Repertoire de configuration utilisateur |
| `--lang-dir` | Repertoire des fichiers de langue |

> **Note** : QET n'a pas d'export CLI natif (Issues GitHub #162, #309). L'export PDF/SVG/DXF se fait uniquement via la GUI.

## Champs d'Information

### Champs Element (elementInformations)

| Champ | Description | Exemple |
|-------|-------------|---------|
| `label` | Designation de repere | `K1`, `Q1`, `F1` |
| `formula` | Formule auto-numerotation | `%{F}-%{l}%{c}` |
| `comment` | Commentaire libre | `Contacteur principal` |
| `function` | Fonction de l'element | `Commande moteur` |
| `description` | Description detaillee | `Contacteur 3P 25A` |
| `designation` | Reference catalogue | `LC1D25BD` |
| `manufacturer` | Fabricant | `Schneider Electric` |
| `manufacturer_reference` | Reference fabricant | `LC1D25BD` |
| `supplier` | Fournisseur | `Rexel` |
| `quantity` | Quantite | `1` |
| `unity` | Unite | `pce` |
| `plant` | Installation/Usine | `=A1` |
| `location` | Localisation | `+S1.G2` |
| `AUX1` a `AUX4` | Champs auxiliaires | Libre |

### Champs Conducteur (conductor)

| Champ | Attribut XML | Description |
|-------|-------------|-------------|
| Numero | `num` | Identifiant du fil (`W1`, `L1`, `N`) |
| Fonction | `function` | Role du conducteur |
| Tension/Protocole | `tension_protocol` | `230V AC`, `24V DC`, `Modbus` |
| Couleur | `conductor_color` | Couleur du fil (`BK`, `BU`, `GNYE`) |
| Section | `conductor_section` | Section en mm2 (`1.5`, `2.5`, `6`) |
| Formule | `formula` | Auto-numerotation conducteur |
| Cable | `cable` | Nom du cable parent (`C1`, `C2`) |
| Bus | `bus` | Nom du bus (`CAN`, `Modbus`) |

## Orientation des Elements

### Attribut orientation

L'attribut `orientation` d'un element dans un diagramme controle les rotations autorisees :

```
orientation="DYYY" (4 caracteres)
```

| Position | Signification | Valeurs |
|----------|--------------|---------|
| 1er (D) | Orientation par defaut | `D` (defaut) |
| 2e | Rotation 90 CW | `Y` (autorise) / `N` (interdit) |
| 3e | Rotation 180 | `Y` / `N` |
| 4e | Rotation 270 CW | `Y` / `N` |

### Types de terminaisons de lignes

| Valeur | Description | Usage |
|--------|-------------|-------|
| `none` | Pas de terminaison | Fil standard |
| `simple` | Trait perpendiculaire | Terre |
| `triangle` | Fleche triangulaire | Sens du courant |
| `circle` | Cercle | Point de connexion |
| `diamond` | Losange | Marqueur special |

Attributs dans `<line>` : `end1="none"` et `end2="triangle"`, avec `length1` et `length2` pour la taille.

## Variables de Cartouche

### Variables Projet

| Variable | Description |
|----------|-------------|
| `%{author}` | Auteur du projet |
| `%{projecttitle}` | Titre du projet |
| `%{plant}` | Installation / Usine |
| `%{machine}` | Machine |
| `%{locmach}` | Localisation machine |
| `%{indexrev}` | Indice de revision |
| `%{saveddate}` | Date de sauvegarde (format local) |
| `%{saveddate-eu}` | Date format europeen (DD/MM/YYYY) |
| `%{saveddate-us}` | Date format US (MM/DD/YYYY) |
| `%{savedtime}` | Heure de sauvegarde |
| `%{savedfilename}` | Nom du fichier |
| `%{savedfilepath}` | Chemin complet du fichier |
| `%{version}` | Version QET |

### Variables Folio

| Variable | Description |
|----------|-------------|
| `%{folio-id}` ou `%id` | Numero du folio courant |
| `%{folio-total}` ou `%total` | Nombre total de folios |
| `%{previous-folio-num}` | Numero du folio precedent |
| `%{next-folio-num}` | Numero du folio suivant |
| `%{title}` | Titre du folio |
| `%{filename}` | Nom du fichier |

### Variables Auto-Numerotation

| Variable | Description | Exemple |
|----------|-------------|---------|
| `%{F}` | Numero du folio (2 chiffres) | `01`, `02` |
| `%{f}` | Numero du folio (1 chiffre) | `1`, `2` |
| `%{M}` | Machine / Installation | `M1` |
| `%{LM}` | Localisation machine | `ARM1` |
| `%{l}` | Numero de ligne (row) | `A`, `B` |
| `%{c}` | Numero de colonne (col) | `1`, `2` |
| `%{id}` | Index auto-increment | `001`, `002` |

### Systeme UUID (v0.9+)

A partir de la version 0.9, chaque element et terminal possede un UUID :
- Format : `{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}`
- Generer en PowerShell : `[guid]::NewGuid().ToString()`
- Les UUIDs permettent le suivi des connexions entre terminaux et conducteurs

## IEC 81346 - Designation de Reference

### Prefixes de designation

| Prefixe | Signification | Exemple |
|---------|--------------|---------|
| `=` | Fonction | `=A1` (Alimentation principale) |
| `+` | Localisation | `+S1.G2` (Armoire 1, Rack 2) |
| `-` | Composant | `-K1` (Contacteur 1) |

### Convention de nommage des bornes

```
BlockName:TerminalNumber
```

Exemples : `X1:1`, `X1:2`, `X2:PE`

### Tags metadata qet_tb_generator

| Tag | Description |
|-----|-------------|
| `%p` | Plant / Installation |
| `%t` | Type de borne |
| `%h` | Hierarchie |
| `%n` | Numero de borne |
| `%b` | Nom du bornier (block) |
| `%r` | Reference croisee |
| `%z` | Zone |
| `%s` | Section |

## Eclairage Tertiaire NF EN 12464-1

| Local | Eclairement (lux) | UGR max | Ra min |
|-------|-------------------|---------|--------|
| Bureau individuel | 500 | 19 | 80 |
| Bureau open space | 500 | 19 | 80 |
| Salle de reunion | 500 | 19 | 80 |
| Accueil / Reception | 300 | 22 | 80 |
| Couloir / Circulation | 100 | 28 | 40 |
| Escaliers | 150 | 25 | 40 |
| Sanitaires | 200 | 25 | 80 |
| Archives / Stockage | 100 | 25 | 60 |
| Atelier mecanique | 300 | 22 | 80 |
| Atelier electronique | 1500 | 16 | 90 |
| Salle serveur | 200 | 25 | 60 |
| Parking interieur | 75 | 25 | 40 |

## Dossiers Constructeurs

### Fabricants references dans la bibliotheque QET

| Categorie | Fabricants |
|-----------|-----------|
| Protection / Distribution | ABB, Schneider Electric, Siemens, Legrand, Hager, Eaton, Chint |
| Appareillage | Legrand, Schneider (Odace/Unica), Hager (Kallysta), Niko, Berker |
| Connectique | Wago, Phoenix Contact, Weidmuller, TE Connectivity, Harting |
| Automatisme | Siemens, Schneider (Modicon), Allen-Bradley, ABB, Omron, Beckhoff |
| Variateurs | ABB, Schneider (Altivar), Siemens (Sinamics), Danfoss, SEW |
| Eclairage | Philips/Signify, Osram/Ledvance, Trilux, Zumtobel, Legrand |
| Mesure | Socomec, Schneider (PowerLogic), Janitza, Chauvin Arnoux |
| Cables | Nexans, Prysmian, Lapp, Helukabel |
| Solaire / ENR | SMA, Fronius, Huawei, Enphase, SolarEdge |
| IRVE | Schneider (EVlink), ABB (Terra), Legrand (Green'up), Wallbox |

## Ecosysteme Outils GitHub

| Outil | Langage | Description | Lien |
|-------|---------|-------------|------|
| `kedema_qet` | Python | Scripts manipulation .qet : merge, extract, transform | qelectrotech/kedema_qet |
| `dxf2elmt` | Rust | Convertisseur DXF vers .elmt | qelectrotech/dxf2elmt |
| `QET_ElementScaler` | Python | Redimensionner et exporter .elmt en SVG | qelectrotech/QET_ElementScaler |
| `qet_gen_element` | Python | Generateur d'elements parametriques | qelectrotech/qet_gen_element |
| `qet_terminal_tables` | Python | Generateur de tables de borniers HTML | qelectrotech/qet_terminal_tables |
| `QET_Klemmenplan` | Python | Generateur de plans de borniers (Klemmenplan) | qelectrotech/QET_Klemmenplan |
| `QetWireManager` | Python | Gestion avancee des conducteurs et numerotation | qelectrotech/QetWireManager |
| `qet_tb_generator` | Python | Generateur de borniers avec metadata IEC 81346 (PyPI) | qelectrotech/qet_tb_generator |

## Grille et Coordonnees

### Grille par defaut

| Parametre | Valeur | Description |
|-----------|--------|-------------|
| Grille standard | 10 px | Pas de grille par defaut |
| Grille cabinet | 9 px | 1 HP (hauteur de pole) = 18 mm = 36 px |
| Grille fine | 1 px | Pour positionnement precis |

### Dimensions folio A4

| Attribut | Valeur | Description |
|----------|--------|-------------|
| `cols` | 17 | Nombre de colonnes |
| `rows` | 8 | Nombre de lignes |
| `colsize` | 60 | Largeur colonne en px |
| `rowsize` | 80 | Hauteur ligne en px |
| Largeur totale | 1020 px | 17 x 60 |
| Hauteur totale | 640 px | 8 x 80 |
| Coordonnee max | (1020, 640) | Coin bas-droit |

### Systeme de coordonnees des references croisees

Les references croisees utilisent la notation `%f-%l%c` :
- `%f` = numero de folio
- `%l` = lettre de ligne (A-H pour 8 lignes)
- `%c` = numero de colonne (1-17 pour 17 colonnes)

Exemple : `1-B3` = Folio 1, Ligne B, Colonne 3

## Commandes Slash

### Gestion de Projets

| Commande | Description |
|----------|-------------|
| `/qet-create` | Creer un nouveau projet QET multi-folios |
| `/qet-open` | Ouvrir un projet dans QElectroTech |
| `/qet-merge` | Fusionner plusieurs fichiers QET en un seul projet |
| `/qet-info` | Analyser un fichier QET (folios, elements, stats) |
| `/qet-export` | Exporter un projet (PDF via GUI, CSV nomenclature) |
| `/qet-backup` | Sauvegarder un projet avec versioning |

### Folios / Diagrammes

| Commande | Description |
|----------|-------------|
| `/qet-folio-add` | Ajouter un folio a un projet existant |
| `/qet-folio-list` | Lister les folios d'un projet |
| `/qet-folio-reorder` | Reorganiser l'ordre des folios |
| `/qet-folio-rename` | Renommer les titres des folios |
| `/qet-folio-extract` | Extraire un folio en fichier separe |

### Elements et Symboles

| Commande | Description |
|----------|-------------|
| `/qet-element-create` | Creer un element personnalise (.elmt) |
| `/qet-element-search` | Chercher un element dans la bibliotheque |
| `/qet-element-list` | Lister les elements utilises dans un projet |
| `/qet-element-import` | Importer un element dans la collection d'un projet |
| `/qet-element-catalog` | Catalogue complet des elements disponibles |

### Nomenclature et Devis

| Commande | Description |
|----------|-------------|
| `/qet-bom` | Generer un Bill of Materials (nomenclature) |
| `/qet-conductors` | Lister et analyser les conducteurs |
| `/qet-devis` | Generer un devis a partir du projet |
| `/qet-materials` | Calculer les materiaux necessaires |

### Conception Electrique

| Commande | Description |
|----------|-------------|
| `/qet-circuit` | Concevoir un circuit electrique (guide) |
| `/qet-panel` | Concevoir un tableau electrique |
| `/qet-nfc15100` | Verifier la conformite NF C 15-100 |
| `/qet-sizing` | Dimensionner cables et protections |

### Fonctions Avancees

| Commande | Description |
|----------|-------------|
| `/qet-titleblock` | Creer/gerer les cartouches personnalises |
| `/qet-autonumber` | Configurer l'auto-numerotation (elements, conducteurs, folios) |
| `/qet-crossref` | Gerer les references croisees Master/Slave |
| `/qet-terminal-strip` | Generer et gerer les borniers |
| `/qet-validate` | Valider l'integrite XML et les references |
| `/qet-variables` | Gerer les variables projet/folio |
| `/qet-diff` | Comparer deux versions d'un projet |
| `/qet-stats` | Statistiques avancees du projet |
| `/qet-dxf-import` | Importer un DXF comme element .elmt |
| `/qet-element-transform` | Redimensionner/pivoter/inverser/exporter un element |

### Wizards Interactifs

| Commande | Description |
|----------|-------------|
| `/qet-wizard` | Assistant interactif general |

## Syntaxe

```
/qet-<commande> [action] [options]
```

### Exemples

```
/qet-create maison 8 folios           # Creer projet maison 8 folios
/qet-info "C:\path\projet.qet"        # Analyser un projet
/qet-merge "C:\dir\*.qet"             # Fusionner des fichiers QET
/qet-bom "C:\path\projet.qet"         # Generer nomenclature
/qet-element-search "prise"           # Chercher un element
/qet-nfc15100 check                   # Verifier conformite
/qet-wizard residential               # Assistant maison complete
/qet-wizard panel                      # Assistant tableau electrique
```

## Wizards Disponibles

| Wizard | Etapes | Description |
|--------|--------|-------------|
| Residential | 8 | Projet electrique maison complete (pieces, circuits, plan) |
| Panel | 6 | Tableau electrique (TGBT, rangees, disjoncteurs, differentiel) |
| Renovation | 5 | Mise aux normes installation existante |
| Extension | 4 | Ajout circuit a un projet existant |
| Tertiaire | 7 | Installation bureau/commerce |
| Outdoor | 4 | Eclairage et prises exterieur/jardin |
| Industrial | 7 | Installation industrielle (moteurs, VFD, automate, borniers) |
| Photovoltaic | 6 | Installation solaire (autoconso, revente, hybride, batterie) |
| EV Charger | 5 | Borne de recharge IRVE (domestique, copropriete, professionnel) |

## Structure XML QET

### Fichier Projet (.qet)

```xml
<project title="Nom" version="0.90">
    <properties>
        <property show="1" name="saveddate">DD/MM/YYYY</property>
        <property show="1" name="savedfilepath">chemin</property>
        <property show="1" name="savedfilename">nom</property>
        <!-- saveddate-us, saveddate-eu, savedtime -->
    </properties>
    <newdiagrams>
        <border cols="17" rows="8" colsize="60" rowsize="80"
                displayrows="true" displaycols="true"/>
        <inset title="" author="" folio="%id/%total" date="null"
               displayAt="bottom"/>
        <conductors type="multi" num="_" displaytext="1" condsize="1"
                    numsize="7" text_color="#000000"/>
        <report label="%f-%l%c"/>
        <xrefs>
            <xref type="coil" displayhas="cross" snapto="label"
                  master_label="%f-%l%c" slave_label="(%f-%l%c)"/>
            <xref type="protection" .../>
            <xref type="commutator" .../>
        </xrefs>
        <conductors_autonums/>
        <folio_autonums/>
        <element_autonums/>
    </newdiagrams>

    <!-- 1 noeud <diagram> par folio -->
    <diagram order="1" title="Nom Folio" cols="17" rows="8"
             colsize="60" rowsize="80" height="660"
             folio="%id/%total" displayAt="bottom"
             version="0.90+...">
        <defaultconductor type="multi" .../>
        <elements>
            <element type="embed://import/path/to/element.elmt"
                     x="100" y="200" orientation="0" z="10"
                     uuid="{...}" freezeLabel="false">
                <terminals>
                    <terminal id="0" x="0" y="-16" orientation="0"/>
                </terminals>
                <elementInformations>
                    <elementInformation name="label" show="1">K1</elementInformation>
                </elementInformations>
                <dynamic_texts>...</dynamic_texts>
            </element>
        </elements>
        <conductors>
            <conductor terminal1="0" terminal2="5" type="multi"
                       num="W1" displaytext="1"/>
        </conductors>
        <inputs>
            <!-- Texte libre (HTML encode) -->
            <input x="50" y="100" text="..." font="Sans Serif,9,..."/>
        </inputs>
        <shapes>
            <shape type="Line" x1="0" y1="0" x2="100" y2="0"
                   is_movable="1" z="0">
                <pen widthF="1" style="SolidLine" color="#000000"/>
                <brush style="NoBrush"/>
            </shape>
            <shape type="Rectangle" x1="0" y1="0" x2="100" y2="50"
                   rx="0" ry="0"/>
            <!-- Types: Line, Rectangle, Ellipse, Polyline -->
        </shapes>
        <images>
            <!-- Images raster incorporees -->
        </images>
    </diagram>

    <!-- Collection embarquee (definitions d'elements) -->
    <collection>
        <category name="import">
            <names>
                <name lang="fr">Elements importes</name>
                <name lang="en">Imported elements</name>
            </names>
            <category name="10_electric">
                <category name="11_singlepole">
                    <category name="500_home_installation">
                        <category name="30_architectural">
                            <element name="pc1.elmt">
                                <definition version="0.100.0"
                                    type="element" link_type="simple"
                                    width="30" height="30"
                                    hotspot_x="15" hotspot_y="27">
                                    <!-- contenu complet -->
                                </definition>
                            </element>
                        </category>
                    </category>
                </category>
            </category>
        </category>
    </collection>
</project>
```

### Fichier Element (.elmt)

```xml
<definition version="0.100.0" type="element" link_type="simple"
            width="30" height="30" hotspot_x="15" hotspot_y="27">
    <uuid uuid="{GUID}"/>
    <names>
        <name lang="fr">Nom francais</name>
        <name lang="en">English name</name>
    </names>
    <informations>Auteur et licence</informations>
    <elementInformations/>
    <description>
        <!-- Primitives graphiques -->
        <line x1="" y1="" x2="" y2="" style="..." antialias="false"
              end1="none" end2="none" length1="1.5" length2="1.5"/>
        <arc x="" y="" width="" height="" start="" angle=""
             style="..." antialias="true"/>
        <circle x="" y="" diameter="" style="..." antialias="false"/>
        <rect x="" y="" width="" height="" rx="" ry=""
              style="..." antialias="false"/>
        <polygon closed="true" style="..." antialias="true">
            <!-- Points x1,y1 x2,y2 ... -->
        </polygon>
        <text x="" y="" text="" size="" rotation=""/>
        <dynamic_text x="" y="" text_from="ElementInfo"
                      uuid="{...}" font="..." text_width="-1"
                      Halignment="AlignLeft" Valignment="AlignTop"
                      rotation="0" frame="false">
            <text></text>
            <info_name>label</info_name>
        </dynamic_text>

        <!-- Bornes de connexion -->
        <terminal x="0" y="-20" orientation="n" name="" type="Generic"
                  uuid="{...}"/>
        <!-- orientation: n(nord/haut), s(sud/bas), e(est/droite), w(ouest/gauche) -->
    </description>
</definition>
```

### Styles graphiques

```
style="line-style:<style>;line-weight:<weight>;filling:<fill>;color:<color>"
```

| Propriete | Valeurs |
|-----------|---------|
| line-style | `normal`, `dashed`, `dotted`, `dashdotted` |
| line-weight | `thin`, `normal`, `hight`, `eleve` |
| filling | `none`, `black`, `white`, `red`, `green`, `blue`, `orange`, `yellow`, `cyan`, `magenta`, `lightgray`, `darkgray`, `hor`, `ver`, `bdiag`, `fdiag` |
| color | Nom CSS ou hex (`black`, `#FF0000`) |

### Types d'elements

| link_type | Description | Usage |
|-----------|-------------|-------|
| `simple` | Element standard | Prises, lampes, interrupteurs |
| `master` | Element maitre | Bobine relais (K1), contacteur |
| `slave` | Element esclave | Contact NO/NC du meme relais |
| `terminale` | Borne | Bornier, terminal strip |
| `thumbnail` | Vignette | Reference de folio |
| `previous_report` | Report amont | Renvoi vers folio precedent |
| `next_report` | Report aval | Renvoi vers folio suivant |

### Fichier Cartouche (.titleblock)

```xml
<titleblocktemplate name="nom">
    <information>Description</information>
    <logos/>
    <grid cols="t22%;r100%;t22%;" rows="25;25;">
        <field valign="center" row="0" col="0" name="author"
               displaylabel="true" align="left" hadjust="true">
            <value>
                <translation lang="en">%author</translation>
            </value>
            <label>
                <translation lang="fr">Auteur</translation>
            </label>
        </field>
        <!-- Variables: %title, %author, %date, %folio, %filename,
             %machine, %locmach, %indexrev, %version, %plant -->
    </grid>
</titleblocktemplate>
```

## Bibliotheque d'Elements

### Structure (installation locale)

```
elements/
  10_electric/
    10_allpole/                    # Schemas multipolaires
      100_folio_referencing/       # Renvois de folios
      110_network_supplies/        # Alimentation reseau
      114_connections/             # Connexions
      120_cables_wiring/           # Cables et filerie
      130_terminals_terminal_strips/ # Bornes et borniers
      140_connectors_plugs/        # Connecteurs
      200_fuses_protective_gears/  # Protections
        10_fuses/                  # Fusibles
        11_circuit_breakers/       # Disjoncteurs
        12_magneto_thermal/        # Magneto-thermiques
        20_disconnecting_switches/ # Interrupteurs-sectionneurs
        30_thermal_relays/         # Relais thermiques
        50_residual_current/       # Differentiels (DDR)
        90_overvoltage_protections/ # Parafoudres
      310_relays_contactors/       # Relais et contacteurs
        01_coils/                  # Bobines
        02_contacts_cross_ref/     # Contacts avec xref
        03_contacts/               # Contacts simples
      330_transformers/            # Transformateurs
      340_converters_inverters/    # Convertisseurs
      380_signaling_operating/     # Signalisation
      390_sensors_instruments/     # Capteurs et instruments
      391_consumers_actuators/     # Consommateurs
      392_generators_sources/      # Generateurs
      395_electronics/             # Electronique
      450_high_voltage/            # Haute tension
      500_home_installation/       # Installation domestique
    11_singlepole/                 # Schemas unifilaires
      140_connectors_plugs/
      200_fuses_protective_gears/
      330_transformers/
      340_converters/
      392_generators/
      395_electronics/
      500_home_installation/
        20_home_appliances/        # Appareils menagers
        25_V.D.I/                  # VDI (Voix-Donnees-Images)
          network/                 # Reseau informatique
            prises_reseau/         # Prises RJ45
          Terrestrial_reception/   # Reception hertzienne
            sockets/               # Prises TV/FM
        30_architectural/          # ** PRINCIPAL: Symboles archi **
        40_meters/                 # Compteurs
    20_manufacturers_articles/     # Articles constructeurs
    90_american_standards/         # Normes americaines
    91_en_60617/                   # Symboles IEC 60617
    98_graphics/                   # Elements graphiques
    99_miscellaneous_unsorted/     # Divers
  20_logic/                        # Logique, grafcet, SFC
  30_hydraulic/                    # Hydraulique
  50_pneumatic/                    # Pneumatique
  60_energy/                       # Energie
```

### Elements Architecturaux Residentiels (30_architectural)

| Element | Fichier | Description |
|---------|---------|-------------|
| Prise simple | `pc1.elmt` | Prise 2P+T avec protection |
| Prise double | `pc2.elmt` | Double prise |
| Prise triple | `pc3.elmt` | Triple prise |
| Prise 4x | `pc4.elmt` | Bloc 4 prises |
| Prise 5x | `pc5.elmt` | Bloc 5 prises |
| Prise 6x | `pc6.elmt` | Bloc 6 prises |
| Prise etanche | `covered_isolated_ground_receptacle_11-13-0x_en60617.elmt` | Prise avec volet |
| Prise terre | `isolated_ground_receptacle_11-13-04_en60617.elmt` | Prise terre isolee |
| Lampe | `lampe.elmt` | Point lumineux plafonnier |
| Lampe applique | `lampe_1.elmt` | Applique murale |
| Neon | `lampe_a_fluorescence.elmt` | Tube fluorescent |
| Luminaire | `luminaire5.elmt` | Luminaire decoratif |
| Spot | `point_eclairage_1.elmt` | Spot encastre |
| Spot 2 | `point_eclairage_2.elmt` | Spot saillie |
| Projecteur | `projecteur_1.elmt` | Projecteur ext. |
| Interrupteur | `interrupteur_unipolaire.elmt` | Inter simple |
| Va-et-vient | `interrupteur_unipolaire_va_et_vient.elmt` | Va-et-vient |
| Bouton poussoir | `bouton_poussoir.elmt` | Minuterie/sonnette |
| Inter bipolaire | `interrupteur_bipolaire.elmt` | Bipolaire (chauffe-eau) |
| Double allumage | `interrupteurdeuxallumages.elmt` | 2 circuits |
| Variateur | `interrupteur_gradateur.elmt` | Dimmer |
| Camera | `camera.elmt` | Camera surveillance |
| Detecteur mouvement | `detecteurdemouvement.elmt` | PIR |
| Detecteur PIR | `dm_pir.elmt` | PIR specifique |
| Sirene interieure | `sir_int.elmt` | Alarme int. |
| Sirene exterieure | `sir_ext_flash.elmt` | Alarme ext. flash |
| Centrale alarme | `centrale.elmt` | Centrale alarme |
| Bris de vitre | `brisvitre.elmt` | Detecteur bris |
| Coffret | `coffret_de_repartition1.elmt` | Tableau electrique |
| Prise terre | `masa.elmt` | Mise a la terre |

### Elements VDI (25_V.D.I)

| Element | Fichier | Description |
|---------|---------|-------------|
| Prise RJ45 | `prise_rj45_6e_leds.elmt` | Prise reseau Cat6 |
| Prise TV/FM | `prise_tv_fm.elmt` | Prise antenne |

### Elements Protection (200_fuses_protective_gears)

| Element | Fichier | Description |
|---------|---------|-------------|
| Disjoncteur 1P | `disjonct-m_1f.elmt` | Disj. unipol. |
| Disjoncteur 1P+N | `disjonct-m_1fn.elmt` | Disj. phase+neutre |
| Disjoncteur 2P | `disjonct-m_2f.elmt` | Disj. bipolaire |
| Disjoncteur 3P | `disjonct-m_3f.elmt` | Disj. triphase |
| Disjoncteur 3P+N | `disjonct-m_3fn.elmt` | Disj. tri+neutre |
| Interrupteur diff. | `interrupteur_differentiel.elmt` | ID 30mA |
| Disj. differentiel | `disjoncteur_differentiel_ph_n.elmt` | DDR |

### Elements Compteurs (40_meters)

| Element | Fichier | Description |
|---------|---------|-------------|
| Compteur | `wattheuremetre.elmt` | Compteur electrique |

## Cartouches Disponibles

| Template | Description |
|----------|-------------|
| `default.titleblock` | Simple: auteur, titre, fichier, date, folio |
| `A4_1.titleblock` | Format A4 standard |
| `DIN_A4.titleblock` | Format DIN A4 allemand |
| `ISO7200_A4_V1.titleblock` | Norme ISO 7200 |
| `double-logo.titleblock` | Avec 2 logos |
| `single-logo.titleblock` | Avec 1 logo |
| `page_de garde.titleblock` | Page de garde |

## Normes et Standards

### NF C 15-100 (Residentiel France/Europe)

#### Nombre minimum de points par piece

| Piece | Prises | Eclairage | Circuits dedies | Notes |
|-------|--------|-----------|-----------------|-------|
| Sejour (< 28m2) | 5 | 1 centre + 1 applique | - | 1 prise par tranche de 4m2 |
| Sejour (> 28m2) | 7 | 1 centre + 2 appliques | - | +1 prise comm. (RJ45/TV) |
| Chambre | 3 | 1 centre | - | 1 prise a cote lit |
| Cuisine | 6 (dont 4 au plan) | 1 centre | Four, Plaques, Lave-V. | Circuit specialise 32A plaques |
| SdB Vol.1 | 0 | 1 (IP44) | Chauffe-eau | Volumes 0,1,2 strictement reglementes |
| SdB Vol.2 | 1 | 1 | - | IP44 obligatoire |
| SdB Vol.3+ | 1 | 1 | Lave-linge | Prises standard |
| WC | 1 | 1 | - | - |
| Couloir | 1 | 1/4m | - | Detecteur mouvement recommande |
| Garage | 1 | 1 | - | Prise 16A pour borne VE recommande |
| Exterieur | 1 | 1 par acces | - | IP44/IP65 obligatoire |

#### Circuits et protections

| Circuit | Section cable | Disjoncteur | Points max | Differentiel |
|---------|--------------|-------------|------------|--------------|
| Eclairage | 1.5 mm2 | 10A ou 16A | 8 points | 30mA type AC |
| Prises standard | 2.5 mm2 | 16A ou 20A | 8 prises | 30mA type AC |
| Prises cuisine | 2.5 mm2 | 20A | 6 prises | 30mA type A |
| Lave-linge | 2.5 mm2 | 20A | Dedie | 30mA type A |
| Lave-vaisselle | 2.5 mm2 | 20A | Dedie | 30mA type A |
| Seche-linge | 2.5 mm2 | 20A | Dedie | 30mA type A |
| Four | 2.5 mm2 | 20A | Dedie | 30mA type A |
| Plaques cuisson | 6 mm2 | 32A | Dedie | 30mA type A |
| Chauffe-eau | 2.5 mm2 | 20A | Dedie | 30mA type AC |
| VMC | 1.5 mm2 | 2A | Dedie | 30mA type AC |
| Volets roulants | 1.5 mm2 | 16A | - | 30mA type AC |
| Chauffage | 1.5 ou 2.5 mm2 | 10A/20A | selon puissance | 30mA type AC |

#### Tableau electrique (TGBT)

| Puissance | Rangees min | Inter. diff. | Disjoncteurs typ. |
|-----------|-------------|--------------|-------------------|
| 3 kVA (T1) | 1 | 1x 40A/30mA type A | 6-8 |
| 6 kVA (T2-T3) | 2 | 2x 40A/30mA (1 type A) | 10-16 |
| 9 kVA (T4) | 3 | 2-3x 40A/30mA | 16-24 |
| 12 kVA (T5+) | 4 | 3-4x 63A/30mA | 24-36 |

#### Volumes salle de bain

```
Volume 0 : Baignoire/douche         -> RIEN (sauf TBTS 12V)
Volume 1 : Au-dessus bain (2.25m)   -> Eclairage IP44/IPX5, TBTS 12V
Volume 2 : 60cm autour (2.25m)      -> Classe II, IP44, chauffage
Hors volume : Au-dela de 60cm       -> Tout equip. classe I/II autorise
```

### IEC 60617 - Symboles

QElectroTech utilise la norme IEC 60617 pour tous les symboles electriques:
- Section 11: Dispositifs de connexion et elements associes
- Section 12: Commande et protection
- Section 13: Signalisation et mesure
- Les noms d'elements incluent souvent la reference normative (ex: `11-13-04`)

## Operations PowerShell sur les fichiers QET

### Charger un projet

```powershell
[xml]$project = [System.IO.File]::ReadAllText('projet.qet')
```

### Lister les folios

```powershell
$project.project.SelectNodes('diagram') | ForEach-Object {
    [PSCustomObject]@{
        Order = $_.order
        Title = $_.title
        Elements = $_.elements.element.Count
    }
}
```

### Compter les elements par type

```powershell
$project.project.SelectNodes('//element[@type]') | ForEach-Object {
    $_.type -replace 'embed://import/',''
} | Group-Object | Sort-Object Count -Descending
```

### Extraire la nomenclature

```powershell
$project.project.SelectNodes('//element') | ForEach-Object {
    $info = $_.elementInformations
    [PSCustomObject]@{
        Type    = ($_.type -split '/')[-1] -replace '\.elmt$',''
        Label   = ($info.elementInformation | Where-Object name -eq 'label').'#text'
        Comment = ($info.elementInformation | Where-Object name -eq 'comment').'#text'
        Folio   = $_.ParentNode.ParentNode.title
        X       = $_.x
        Y       = $_.y
    }
}
```

### Creer un element simple

```powershell
$elmt = @'
<definition version="0.100.0" type="element" link_type="simple"
            width="30" height="30" hotspot_x="15" hotspot_y="15">
    <uuid uuid="{NEW-GUID}"/>
    <names>
        <name lang="fr">Mon Element</name>
        <name lang="en">My Element</name>
    </names>
    <informations>Auteur: r2d2</informations>
    <description>
        <circle x="-10" y="-10" diameter="20"
                style="line-style:normal;line-weight:normal;filling:none;color:black"
                antialias="true"/>
        <terminal x="0" y="-15" orientation="n" type="Generic"/>
    </description>
</definition>
'@ -replace 'NEW-GUID', [guid]::NewGuid().ToString()
[System.IO.File]::WriteAllText('element.elmt', $elmt,
    [System.Text.UTF8Encoding]::new($false))
```

### Sauvegarder en UTF-8 sans BOM

```powershell
$settings = New-Object System.Xml.XmlWriterSettings
$settings.Indent = $true
$settings.IndentChars = '    '
$settings.Encoding = [System.Text.UTF8Encoding]::new($false)
$writer = [System.Xml.XmlWriter]::Create('output.qet', $settings)
$doc.Save($writer)
$writer.Close()
```

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

## Structure Fichiers

```
qelectrotech-skill/
  SKILL.md                    # Ce fichier (35 cmd, 9 wizards, 4 templates)
  commands/                   # Commandes slash (35 fichiers)
    create.md                 # /qet-create
    open.md                   # /qet-open
    merge.md                  # /qet-merge
    info.md                   # /qet-info
    export.md                 # /qet-export
    backup.md                 # /qet-backup
    folio-add.md              # /qet-folio-add
    folio-list.md             # /qet-folio-list
    folio-reorder.md          # /qet-folio-reorder
    folio-rename.md           # /qet-folio-rename
    folio-extract.md          # /qet-folio-extract
    element-create.md         # /qet-element-create
    element-search.md         # /qet-element-search
    element-list.md           # /qet-element-list
    element-import.md         # /qet-element-import
    element-catalog.md        # /qet-element-catalog
    element-transform.md      # /qet-element-transform
    bom.md                    # /qet-bom
    conductors.md             # /qet-conductors
    devis.md                  # /qet-devis
    materials.md              # /qet-materials
    circuit.md                # /qet-circuit
    panel.md                  # /qet-panel
    nfc15100.md               # /qet-nfc15100
    sizing.md                 # /qet-sizing
    titleblock.md             # /qet-titleblock
    autonumber.md             # /qet-autonumber
    crossref.md               # /qet-crossref
    terminal-strip.md         # /qet-terminal-strip
    validate.md               # /qet-validate
    variables.md              # /qet-variables
    diff.md                   # /qet-diff
    stats.md                  # /qet-stats
    dxf-import.md             # /qet-dxf-import
    wizard.md                 # /qet-wizard
  wizards/                    # Assistants interactifs (9 fichiers)
    wizard-residential.md
    wizard-panel.md
    wizard-renovation.md
    wizard-extension.md
    wizard-tertiaire.md
    wizard-outdoor.md
    wizard-industrial.md
    wizard-photovoltaic.md
    wizard-ev-charger.md
  templates/                  # Templates XML (4 fichiers)
    project-template.xml      # Squelette projet vide
    element-template.xml      # Squelette element
    titleblock-template.xml   # Squelette cartouche
    terminal-strip-template.xml # Squelette borne
    titleblock-nelu.xml       # Cartouche personnalise

```

## References

- [QElectroTech Official](https://qelectrotech.org)
- [QET Wiki](https://qelectrotech.org/wiki_new/)
- [Element Collection](https://qelectrotech.org/elementsFixture/)
- [Source Code](https://github.com/qelectrotech/qelectrotech-source-mirror)
- [NF C 15-100 Guide](https://www.schneider-electric.fr/fr/work/support/green-premium/nfc15100.jsp)
- [IEC 60617 Symbols](https://std.iec.ch/iec60617)
