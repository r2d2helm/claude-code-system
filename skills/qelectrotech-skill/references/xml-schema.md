# Structure XML QET

> Reference extraite du skill QElectroTech - schemas XML pour projets, elements et cartouches

## Fichier Projet (.qet)

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

## Fichier Element (.elmt)

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

## Styles graphiques

```
style="line-style:<style>;line-weight:<weight>;filling:<fill>;color:<color>"
```

| Propriete | Valeurs |
|-----------|---------|
| line-style | `normal`, `dashed`, `dotted`, `dashdotted` |
| line-weight | `thin`, `normal`, `hight`, `eleve` |
| filling | `none`, `black`, `white`, `red`, `green`, `blue`, `orange`, `yellow`, `cyan`, `magenta`, `lightgray`, `darkgray`, `hor`, `ver`, `bdiag`, `fdiag` |
| color | Nom CSS ou hex (`black`, `#FF0000`) |

## Types d'elements

| link_type | Description | Usage |
|-----------|-------------|-------|
| `simple` | Element standard | Prises, lampes, interrupteurs |
| `master` | Element maitre | Bobine relais (K1), contacteur |
| `slave` | Element esclave | Contact NO/NC du meme relais |
| `terminale` | Borne | Bornier, terminal strip |
| `thumbnail` | Vignette | Reference de folio |
| `previous_report` | Report amont | Renvoi vers folio precedent |
| `next_report` | Report aval | Renvoi vers folio suivant |

## Fichier Cartouche (.titleblock)

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
