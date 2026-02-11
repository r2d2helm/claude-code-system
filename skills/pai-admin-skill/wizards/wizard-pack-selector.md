# Wizard : Selection Guidee de Packs

Assistant interactif pour choisir les packs PAI adaptes aux besoins de l'utilisateur.

## Etape 1 : Etat actuel

1. Verifier quels packs sont deja installes (via `/pai-packs --installed`)
2. Afficher l'etat actuel

## Etape 2 : Profil d'usage

Demander via AskUserQuestion :
- "Comment utilisez-vous principalement votre DA ?"
  - Developpement logiciel
  - Recherche et analyse
  - Securite et audit
  - Creativite et contenu
  - Gestion de projets et vie personnelle
  - Un peu de tout

## Etape 3 : Recommandations

Selon le profil, recommander :

### Developpement
- pai-createcli-skill (generation CLI)
- pai-createskill-skill (creation skills)
- pai-browser-skill (test automation)
- pai-prompting-skill (meta-prompting)

### Recherche et analyse
- pai-research-skill (recherche multi-sources)
- pai-firstprinciples-skill (analyse fondamentale)
- pai-council-skill (debat multi-agents)
- pai-osint-skill (intelligence open source)

### Securite
- pai-recon-skill (reconnaissance)
- pai-redteam-skill (analyse adversariale)
- pai-annualreports-skill (rapports securite)
- pai-osint-skill (OSINT)

### Creativite
- pai-art-skill (contenu visuel)
- pai-prompting-skill (meta-prompting)
- pai-agents-skill (agents personnalises)

### Gestion projets / vie
- pai-telos-skill (objectifs de vie)
- pai-algorithm-skill (methodologie)
- pai-agents-skill (delegation)

### Tout
- Recommander le Bundle complet

## Etape 4 : Installation

1. Afficher les packs recommandes avec descriptions
2. Demander lesquels installer via AskUserQuestion (multiSelect)
3. Verifier les dependances
4. Installer dans l'ordre correct (infrastructure d'abord)
5. Pour chaque pack : `/pai-pack-install <nom>`
6. Verification finale
