# Bibliotheque d'Elements QET

> Reference extraite du skill QElectroTech - catalogue complet des elements et structure de la bibliotheque

## Structure (installation locale)

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

## Elements Architecturaux Residentiels (30_architectural)

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

## Elements VDI (25_V.D.I)

| Element | Fichier | Description |
|---------|---------|-------------|
| Prise RJ45 | `prise_rj45_6e_leds.elmt` | Prise reseau Cat6 |
| Prise TV/FM | `prise_tv_fm.elmt` | Prise antenne |

## Elements Protection (200_fuses_protective_gears)

| Element | Fichier | Description |
|---------|---------|-------------|
| Disjoncteur 1P | `disjonct-m_1f.elmt` | Disj. unipol. |
| Disjoncteur 1P+N | `disjonct-m_1fn.elmt` | Disj. phase+neutre |
| Disjoncteur 2P | `disjonct-m_2f.elmt` | Disj. bipolaire |
| Disjoncteur 3P | `disjonct-m_3f.elmt` | Disj. triphase |
| Disjoncteur 3P+N | `disjonct-m_3fn.elmt` | Disj. tri+neutre |
| Interrupteur diff. | `interrupteur_differentiel.elmt` | ID 30mA |
| Disj. differentiel | `disjoncteur_differentiel_ph_n.elmt` | DDR |

## Elements Compteurs (40_meters)

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
