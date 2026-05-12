# Wizard: Setup Initial Organisation

Configuration complete du systeme d'organisation de fichiers.

## Declenchement

```
/file-wizard setup
```

## Etapes du Wizard (6)

### Etape 1: Analyse Etat Actuel

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD ORGANISATION FICHIERS                       ║
║               Etape 1/6 : Analyse                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ANALYSE DE VOTRE SYSTEME...                                 ║
║                                                              ║
║  ETAT ACTUEL:                                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Documents   : 4,567 fichiers │ 45.6 GB │ Score: 45/100  │ ║
║  │ Pictures    : 12,345 fichiers│ 89.2 GB │ Score: 62/100  │ ║
║  │ Downloads   : 892 fichiers   │ 23.4 GB │ Score: 28/100  │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  PROBLEMES DETECTES:                                         ║
║  * 1,234 fichiers sans date ISO (27%)                        ║
║  * 567 fichiers avec espaces/caracteres speciaux             ║
║  * 234 doublons potentiels (4.5 GB)                          ║
║  * 89 dossiers vides                                         ║
║                                                              ║
║  Score global: 42/100 ████████░░░░░░░░░░░░░░                 ║
║                                                              ║
║  [1] Continuer avec configuration  [2] Rapport detaille      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Etape 2: Choix du Profil

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD ORGANISATION FICHIERS                       ║
║                Etape 2/6 : Profil                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Quel profil correspond le mieux a votre usage ?             ║
║                                                              ║
║  [1] PERSONNEL                                               ║
║      Documents administratifs, photos, medias                ║
║      Structure: Administratif, Projets, Personnel            ║
║                                                              ║
║  [2] PROFESSIONNEL                                           ║
║      Travail, clients, projets d'entreprise                  ║
║      Structure: Clients, Projets, Admin, Resources           ║
║                                                              ║
║  [3] DEVELOPPEUR                                             ║
║      Code, projets dev, documentation technique              ║
║      Structure: Projects, Code, Docs, Tools                  ║
║                                                              ║
║  [4] CREATIF                                                 ║
║      Design, medias, portfolio                               ║
║      Structure: Clients, Portfolio, Assets, Archive          ║
║                                                              ║
║  [5] PERSONNALISE                                            ║
║      Creer votre propre structure                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Etape 3: Structure des Dossiers

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD ORGANISATION FICHIERS                       ║
║              Etape 3/6 : Structure                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  STRUCTURE PROPOSEE (Profil: Personnel):                     ║
║                                                              ║
║  Documents/                                                  ║
║  ├── _INBOX/              # Fichiers a trier                 ║
║  ├── _ARCHIVE/            # Anciens fichiers par annee       ║
║  │   └── {YYYY}/                                             ║
║  ├── Administratif/                                          ║
║  │   ├── Banque/                                             ║
║  │   ├── Impots/                                             ║
║  │   ├── Assurances/                                         ║
║  │   └── Factures/                                           ║
║  ├── Projets/                                                ║
║  │   └── {NomProjet}/                                        ║
║  ├── Travail/                                                ║
║  └── Personnel/                                              ║
║                                                              ║
║  [1] Appliquer  [2] Modifier  [3] Previsualiser              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script creation structure:**
```bash
#!/usr/bin/env bash
base_path="$HOME/Documents"

structure=(
  "_INBOX"
  "_ARCHIVE/2024"
  "_ARCHIVE/2025"
  "_ARCHIVE/2026"
  "Administratif/Banque"
  "Administratif/Impots"
  "Administratif/Assurances"
  "Administratif/Factures"
  "Projets"
  "Travail"
  "Personnel"
)

for folder in "${structure[@]}"; do
  path="${base_path}/${folder}"
  if [ ! -d "$path" ]; then
    mkdir -p "$path"
    echo "Cree: $folder"
  fi
done
```

### Etape 4: Convention de Nommage

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD ORGANISATION FICHIERS                       ║
║              Etape 4/6 : Nommage                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  CONVENTION DE NOMMAGE:                                      ║
║                                                              ║
║  Format standard:                                            ║
║  {DATE}_{CATEGORIE}_{DESCRIPTION}_{VERSION}.{EXT}            ║
║                                                              ║
║  Exemples:                                                   ║
║  2026-02-03_Facture_EDF-Janvier_v01.pdf                      ║
║  2026-02-03_Photo_Vacances-Bretagne_001.jpg                  ║
║                                                              ║
║  Regles:                                                     ║
║  [x] Date ISO en prefixe (YYYY-MM-DD)                        ║
║  [x] Underscores entre elements                              ║
║  [x] Tirets entre mots                                       ║
║  [x] Pas d'espaces ni accents                                ║
║  [x] Versions avec zeros (v01, v02)                          ║
║  [x] Maximum 50 caracteres                                   ║
║                                                              ║
║  Appliquer aux fichiers existants ?                          ║
║  [1] Oui, renommer maintenant                                ║
║  [2] Non, appliquer seulement aux nouveaux                   ║
║  [3] Previsualiser les changements                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Etape 5: Nettoyage Initial

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD ORGANISATION FICHIERS                       ║
║              Etape 5/6 : Nettoyage                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  NETTOYAGE INITIAL:                                          ║
║                                                              ║
║  Actions recommandees:                                       ║
║                                                              ║
║  [x] Supprimer 89 dossiers vides                             ║
║  [x] Nettoyer fichiers temporaires (2.3 GB)                  ║
║  [x] Organiser Downloads par type                            ║
║  [x] Deplacer fichiers Desktop vers _INBOX                   ║
║                                                              ║
║  Actions optionnelles:                                       ║
║  [ ] Supprimer doublons (234 fichiers, 4.5 GB)               ║
║      Verification manuelle recommandee                       ║
║  [ ] Archiver fichiers > 1 an                                ║
║  [ ] Vider corbeille (1.2 GB)                                ║
║                                                              ║
║  Espace a liberer: ~8 GB                                     ║
║                                                              ║
║  [1] Executer nettoyage  [2] Passer  [3] Details             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Etape 6: Automatisation

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD ORGANISATION FICHIERS                       ║
║             Etape 6/6 : Automatisation                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  CONFIGURATION AUTOMATISATION:                               ║
║                                                              ║
║  Taches cron:                                                ║
║                                                              ║
║  [x] Organiser Downloads automatiquement                     ║
║      Frequence: Quotidien a 20:00                            ║
║                                                              ║
║  [x] Nettoyer fichiers temporaires                           ║
║      Frequence: Hebdomadaire (Dimanche 03:00)                ║
║                                                              ║
║  [ ] Scanner doublons                                        ║
║      Frequence: Mensuel (1er du mois)                        ║
║                                                              ║
║  [ ] Archiver fichiers anciens                               ║
║      Frequence: Mensuel (fichiers > 1 an)                    ║
║                                                              ║
║  [1] Configurer  [2] Passer  [3] Manuel uniquement           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Finalisation

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD ORGANISATION FICHIERS                       ║
║                   TERMINE                                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  CONFIGURATION TERMINEE!                                     ║
║                                                              ║
║  Resume des actions:                                         ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Structure creee (15 dossiers)                           │ ║
║  │ Convention de nommage definie                           │ ║
║  │ 89 dossiers vides supprimes                             │ ║
║  │ 2.3 GB de fichiers temp nettoyes                        │ ║
║  │ Downloads organise par type                             │ ║
║  │ 2 taches cron creees                                    │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  NOUVEAU SCORE: 78/100 (+36 pts!)                            ║
║  ████████████████████████████████░░░░░░░░                    ║
║                                                              ║
║  README cree: Documents/README-Organisation.md               ║
║                                                              ║
║  Prochaines etapes suggerees:                                ║
║  * Trier les fichiers dans _INBOX                            ║
║  * Revoir les doublons detectes                              ║
║  * Renommer photos avec /file-rename iso-date                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script README genere:**
```bash
#!/usr/bin/env bash
cat > "$HOME/Documents/README-Organisation.md" <<EOF
# Organisation des Fichiers

## Structure
- **_INBOX**: Fichiers a trier
- **_ARCHIVE**: Anciens fichiers par annee
- **Administratif**: Documents officiels
- **Projets**: Projets en cours
- **Travail**: Documents professionnels
- **Personnel**: Documents prives

## Convention de Nommage
Format: \`{DATE}_{CATEGORIE}_{DESCRIPTION}_{VERSION}.{EXT}\`
Exemple: \`2026-02-03_Facture_EDF-Janvier_v01.pdf\`

### Regles
- Date ISO: YYYY-MM-DD
- Pas d'espaces (utiliser - ou _)
- Pas d'accents ni caracteres speciaux
- Versions: v01, v02, v03...

## Automatisation (cron)
- Downloads organise: Quotidien 20:00
- Nettoyage temp: Dimanche 03:00

## Commandes Utiles
- \`/file-organize downloads\` - Organiser telechargements
- \`/file-rename iso-date .\` - Ajouter dates ISO
- \`/file-clean temp\` - Nettoyer fichiers temporaires
- \`/file-analyze audit .\` - Verifier organisation

Configure le: $(date +%Y-%m-%d)
EOF
echo "README cree: $HOME/Documents/README-Organisation.md"
```
