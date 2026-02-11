# PRP : Amélioration globale des skills r2d2 — Audit Fix

## Goal
Corriger les 10 issues critiques et 8 warnings identifiés lors de l'audit global des 13 skills du système r2d2. Implémenter les 43 commandes [PREVU] manquantes, refactorer les SKILL.md surdimensionnés, et standardiser la qualité de documentation.

## Why
- Le meta-router ne route pas les commandes non déclarées (pai-admin fantôme)
- 2 SKILL.md dépassent la limite de 500 lignes (QET: 944, meta-router: 528)
- 43 commandes promises dans les SKILL.md mais sans fichiers d'implémentation
- Counts périmés dans CLAUDE.md créent de la confusion
- Absence de frontmatter YAML empêche le routage de certains skills

## What

### Success Criteria
- [ ] pai-admin-skill supprimé du filesystem
- [ ] Dossier parasite `{commands,wizards,templates}` supprimé de fileorg-skill
- [ ] QET SKILL.md < 500 lignes avec references/ créé
- [ ] Meta-router SKILL.md < 500 lignes
- [ ] Frontmatter YAML ajouté aux skills manquants (vault-guardian, qelectrotech)
- [ ] Tous les counts dans CLAUDE.md correspondent au filesystem
- [ ] 43 commandes [PREVU] implémentées avec fichiers .md
- [ ] Docker et Linux SKILL.md enrichis (Best Practices, liens doc)
- [ ] Validation 3 niveaux : 10/10

## Contexte nécessaire

### Documentation & Références
```yaml
- file: ~/.claude/skills/SKILL.md
  why: Meta-router à refactorer (528 lignes → <500)

- file: ~/.claude/skills/qelectrotech-skill/SKILL.md
  why: 944 lignes → refactorer dans references/ (<300 lignes core)

- file: ~/.claude/skills/proxmox-skill/commands/status.md
  why: Gold standard command file (281 lignes, multi-mode, scripts)

- file: ~/.claude/skills/windows-skill/commands/firewall.md
  why: Gold standard command file (371 lignes, complex)

- file: ~/.claude/skills/docker-skill/commands/ps.md
  why: Exemple commande simple (69 lignes)

- file: ~/.claude/CLAUDE.md
  why: Counts à corriger, sections Skills et Hooks
```

### Gotchas connus du système
```
# CRITICAL: Encodage UTF-8 sans BOM pour .md/.json
# CRITICAL: UTF-8 avec BOM pour .ps1/.psm1 (PS 5.1)
# CRITICAL: Wikilinks [[Nom]] dans les notes Obsidian
# CRITICAL: Frontmatter YAML obligatoire dans les notes vault
# CRITICAL: Pas de `??` ni `UTF8BOM` dans les scripts PowerShell (PS 5.1)
# CRITICAL: SKILL.md max 500 lignes, overflow dans references/
```

### Gold Standard Command Template
```markdown
# /<prefix>-<name> - Description Courte

Description en une phrase.

## Syntaxe

\`\`\`
/<prefix>-<name> [action] [options]
\`\`\`

## Actions

### /<prefix>-<name> action1

[Exemple de sortie visuelle en box-drawing, 10-30 lignes]

**Script PowerShell/Bash :**
\`\`\`powershell
# Implémentation avec commentaires
\`\`\`

## Options

| Option | Description |
|--------|-------------|
| `--flag` | Ce que ça fait |

## Exemples

\`\`\`bash
# Cas d'usage simple
/<prefix>-<name> action1

# Cas avancé
/<prefix>-<name> action2 --flag value
\`\`\`

## Voir Aussi
- `/<prefix>-related` - Description
```

**Sizing guide :**
- Commande simple (référence) : 50-100 lignes
- Commande medium (1-2 modes) : 100-200 lignes
- Commande complexe (3+ modes + script) : 200-350 lignes

## Implementation Blueprint

### Phase 1 : Cleanup (5 tâches)

```yaml
Task 1:
  action: DELETE
  path: ~/.claude/skills/pai-admin-skill/
  description: Supprimer le skill fantôme (27 commandes, non routé)
  validation: "! Test-Path ~/.claude/skills/pai-admin-skill"

Task 2:
  action: DELETE
  path: ~/.claude/skills/fileorg-skill/{commands,wizards,templates}/
  description: Supprimer le dossier parasite (glob expansion ratée)
  validation: Vérifier que commands/ et wizards/ normaux existent toujours

Task 3:
  action: MODIFY
  path: ~/.claude/skills/vault-guardian-skill/SKILL.md
  description: Ajouter frontmatter YAML en tête de fichier
  content: |
    ---
    name: vault-guardian-skill
    description: "Maintenance proactive du vault : health checks, auto-fix, rapports. Utiliser pour diagnostiquer, corriger automatiquement, ou auditer le vault Obsidian."
    ---

Task 4:
  action: MODIFY
  path: ~/.claude/skills/qelectrotech-skill/SKILL.md
  description: Ajouter frontmatter YAML en tête (sera refactoré en Phase 2)
  content: |
    ---
    name: qelectrotech-skill
    description: "Plans électriques QElectroTech : schémas unifilaires, multifilaires, nomenclatures, éléments, folios. Normes NF C 15-100 et IEC 60617."
    ---

Task 5:
  action: MODIFY
  path: ~/.claude/skills/docker-skill/SKILL.md
  description: Ajouter frontmatter YAML
  content: |
    ---
    name: docker-skill
    description: "Administration Docker et conteneurs : images, containers, compose, volumes, networks, registries, sécurité."
    ---
  ALSO: Même chose pour linux-skill/SKILL.md
```

### Phase 2 : Refactoring SKILL.md surdimensionnés (2 tâches)

```yaml
Task 6:
  action: REFACTOR
  path: ~/.claude/skills/qelectrotech-skill/
  description: |
    Extraire le contenu de SKILL.md (944 lignes) dans references/.
    Créer les fichiers suivants :

    references/field-definitions.md    ← lignes ~39-182 (champs éléments, UUID, IEC 81346)
    references/collections-paths.md    ← lignes ~19-37 (chemins, collections, flags CLI)
    references/variables-autonumber.md ← lignes ~102-144 (variables cartouche, autonumérotation)
    references/electrical-standards.md ← lignes ~183-199 + ~689-743 (NF C 15-100, IEC 60617, éclairage)
    references/elements-catalog.md     ← lignes ~555-676 (bibliothèque éléments résidentiel, VDI, protection)
    references/xml-schema.md           ← lignes ~366-553 (structure XML projet, élément, cartouche)
    references/manufacturers.md        ← lignes ~200-228 (fournisseurs, outils GitHub)
    references/grid-coordinates.md     ← lignes ~230-260 (grille, dimensions, coordonnées)
    references/powershell-snippets.md  ← lignes ~752-830 (scripts PS manipulation QET)
    references/titleblocks.md          ← lignes ~677-687 (templates cartouche)
    references/gui-reference.md        ← lignes ~832-863 (raccourcis, limitations)

    SKILL.md final (~300 lignes) conserve :
    - Frontmatter YAML
    - Header & environment (lignes 1-37)
    - Table des 35 commandes slash (lignes 261-350)
    - Index des références (nouveau, 20 lignes)
    - Raccourcis GUI résumés (5 lignes)
    - Exemples overview (5 lignes)

  pattern: Lire le SKILL.md actuel, identifier les sections exactes, extraire

Task 7:
  action: REFACTOR
  path: ~/.claude/skills/
  description: |
    Réduire SKILL.md meta-router de 528 à <500 lignes.

    Option A (recommandée) : Supprimer la section pai-admin si présente,
    compresser les pattern details (chaque skill en 5 lignes max au lieu de 15),
    déplacer les exemples de routing dans references/routing-examples.md.

    Option B : Extraire les diagrammes de flux ASCII dans references/detection-flows.md.

    Cible : ~400 lignes.

    IMPORTANT : Ne PAS ajouter pai-admin-skill (il est supprimé).
    Vérifier que les 12 skills restants sont tous listés avec les bons counts.
```

### Phase 3 : Docker + Linux (8 commandes)

```yaml
Task 8:
  action: CREATE (3 fichiers)
  path: ~/.claude/skills/docker-skill/commands/
  description: |
    Implémenter les 3 commandes [PREVU] du docker-skill.
    Pattern : suivre dk-ps.md (simple, 70-100 lignes chacune)

    1. registry.md — /dk-registry
       - Modes : login, push, pull, tag, search, catalog
       - Script : docker login, docker push, docker pull
       - Voir aussi : /dk-images

    2. swarm.md — /dk-swarm
       - Modes : init, join, leave, status, services, scale
       - Script : docker swarm init, docker node ls, docker service ls
       - Voir aussi : /dk-ps, /dk-network

    3. security.md — /dk-security
       - Modes : scan (image vuln), audit (runtime), secrets, trust
       - Script : docker scout cve, docker inspect --format security
       - Voir aussi : /dk-images

  ALSO: Enrichir docker-skill/SKILL.md :
    - Ajouter section "## Best Practices 2025-2026"
    - Ajouter section "## Références" avec liens Docker docs
    - Retirer les [PREVU] des 3 commandes maintenant implémentées
    - Mettre à jour le count (10 → 13 cmd)

Task 9:
  action: CREATE (5 fichiers)
  path: ~/.claude/skills/linux-skill/commands/
  description: |
    Implémenter les 5 commandes [PREVU] du linux-skill.
    Pattern : suivre le style existant (lx-status.md, 64 lignes, simple)

    1. backup.md — /lx-backup
       - Modes : rsync (incremental), tar (archive), snapshot, schedule
       - Script : rsync -avz, tar czf, crontab
       - Voir aussi : /lx-disk

    2. ssh.md — /lx-ssh
       - Modes : config, keys (generate/deploy), tunnel, harden
       - Script : ssh-keygen, ssh-copy-id, sshd_config
       - Voir aussi : /lx-firewall, /lx-users

    3. dns.md — /lx-dns
       - Modes : resolve, config, zones, flush, test
       - Script : dig, nslookup, systemd-resolved, named
       - Voir aussi : /lx-network

    4. nginx.md — /lx-nginx
       - Modes : status, sites (list/enable/disable), config (test/reload), ssl, proxy
       - Script : nginx -t, systemctl, sites-available/enabled
       - Voir aussi : /lx-certbot, /lx-firewall

    5. certbot.md — /lx-certbot
       - Modes : obtain, renew, revoke, list, auto
       - Script : certbot certonly, certbot renew, crontab
       - Voir aussi : /lx-nginx

  ALSO: Enrichir linux-skill/SKILL.md :
    - Ajouter section "## Best Practices 2025-2026"
    - Ajouter section "## Références" avec liens (Ubuntu docs, RHEL, Arch Wiki)
    - Retirer les [PREVU]
    - Mettre à jour le count (12 → 17 cmd)
```

### Phase 4 : Obsidian PREVU (23 commandes)

```yaml
Task 10:
  action: CREATE (23 fichiers)
  path: ~/.claude/skills/obsidian-skill/commands/
  description: |
    Implémenter les 23 commandes [PREVU] de l'obsidian-skill.
    Pattern : suivre health.md (complex, 356 lignes) pour les commandes riches,
    et un format plus simple (80-120 lignes) pour les commandes utilitaires.

    === GRAPHE & LIENS (4 commandes) ===

    1. graph.md — /obs-graph
       - Modes : show (stats graphe), clusters (groupes), islands (isolés), density
       - Script PS : Get-ChildItem *.md | analyse wikilinks, calcul centralité
       - ~150 lignes

    2. links-unlinked.md — /obs-links unlinked
       - Trouve les notes sans aucun lien entrant ni sortant
       - Script PS : comparer tous les wikilinks vs fichiers existants
       - ~80 lignes

    3. links-suggest.md — /obs-links suggest
       - Suggère des connexions basées sur tags, mots-clés, proximité sémantique
       - Script PS : analyser tags communs, termes fréquents
       - ~100 lignes

    4. links-fix.md — /obs-links fix
       - Répare les liens cassés (rename, target disparu, typo)
       - Script PS : Find-BrokenLinks puis proposition de fix interactif
       - ~120 lignes

    === TAGS (4 commandes) ===

    5. tags-unused.md — /obs-tags unused
       - Liste les tags définis mais non utilisés
       - Script PS : collecter tous les tags, compter occurrences
       - ~80 lignes

    6. tags-rename.md — /obs-tags rename <old> <new>
       - Renomme un tag dans tout le vault (frontmatter + inline)
       - Script PS : regex replace dans tous les .md
       - ~100 lignes

    7. tags-merge.md — /obs-tags merge <tag1> <tag2> → <target>
       - Fusionne deux tags en un seul
       - Script PS : rename tag1 → target, rename tag2 → target
       - ~80 lignes

    8. tags-hierarchy.md — /obs-tags hierarchy
       - Affiche l'arbre hiérarchique des tags (dev/python, ai/claude...)
       - Script PS : parser tags, construire arbre, afficher ASCII
       - ~100 lignes

    === STRUCTURE (3 commandes) ===

    9. structure.md — /obs-structure
       - Analyse la structure des dossiers (profondeur, distribution, tailles)
       - Script PS : Get-ChildItem -Recurse, stats par dossier
       - ~120 lignes

    10. move.md — /obs-move <note> <destination>
        - Déplace une note et met à jour tous les wikilinks pointant vers elle
        - Script PS : Move-Item + regex replace [[old-path]] → [[new-path]]
        - ~120 lignes

    11. rename.md — /obs-rename <note> <new-name>
        - Renomme une note selon les conventions (C_, YYYY-MM-DD_Conv_, etc.)
        - Met à jour tous les backlinks
        - ~100 lignes

    === CONTENU (4 commandes) ===

    12. templates.md — /obs-templates
        - Modes : list, validate, create, apply
        - Gère les templates du vault (_Templates/)
        - ~100 lignes

    13. duplicates.md — /obs-duplicates
        - Détecte les notes avec contenu similaire (hash, titre, tags)
        - Script PS : Get-FileHash + comparaison frontmatter
        - ~120 lignes

    14. attachments.md — /obs-attachments
        - Modes : list, orphans (non référencées), clean, move
        - Gère les pièces jointes (images, PDF)
        - ~120 lignes

    15. empty.md — /obs-empty
        - Trouve et supprime les notes vides ou quasi-vides
        - Script PS : Get-Content, mesurer contenu hors frontmatter
        - ~80 lignes

    === EXPORT & SYNC (2 commandes) ===

    16. export.md — /obs-export
        - Modes : pdf, html, json, csv
        - Exporte des notes ou le vault entier
        - ~120 lignes

    17. sync.md — /obs-sync
        - Modes : git (commit/push), backup (zip), compare
        - Synchronise le vault avec un backup ou repo
        - ~100 lignes

    === CONFIG (3 commandes) ===

    18. config.md — /obs-config
        - Modes : show, edit, reset
        - Gère la configuration Obsidian (.obsidian/)
        - ~100 lignes

    19. plugins.md — /obs-plugins
        - Modes : list, enable, disable, update, info
        - Gère les plugins community
        - ~120 lignes

    20. hotkeys.md — /obs-hotkeys
        - Modes : list, search, conflicts, export
        - Gère les raccourcis clavier Obsidian
        - ~80 lignes

    === WIZARDS (3 commandes) ===

    21. wizard-audit.md — /obs-wizard audit
        - Wizard complet d'audit vault (6 étapes guidées)
        - ~150 lignes

    22. wizard-cleanup.md — /obs-wizard cleanup
        - Nettoyage guidé (orphelins, vides, doublons, attachments)
        - ~120 lignes

    23. wizard-reorganize.md — /obs-wizard reorganize
        - Réorganisation assistée de la structure du vault
        - ~120 lignes

  ALSO: Mettre à jour obsidian-skill/SKILL.md :
    - Retirer tous les [PREVU]
    - Mettre à jour count (8 → 31 cmd, 1 → 4 wizards)
    - Si SKILL.md dépasse 500 lignes après mise à jour, refactorer dans references/
```

### Phase 5 : Fileorg PREVU (12 commandes)

```yaml
Task 11:
  action: CREATE (12 fichiers)
  path: ~/.claude/skills/fileorg-skill/commands/
  description: |
    Implémenter les 12 commandes [PREVU] du fileorg-skill.
    Pattern : suivre organize.md (253 lignes, medium complexity)

    === TRI & ORGANISATION (2 commandes) ===

    1. sort.md — /file-sort
       - Trie fichiers dans sous-dossiers par type/date/taille
       - Modes : by-type, by-date, by-size, by-extension
       - Script PS : Group-Object Extension, Move-Item
       - ~120 lignes

    2. flatten.md — /file-flatten
       - Aplatit une arborescence trop profonde (>3 niveaux)
       - Modes : preview (dry-run), execute, undo
       - Script PS : Get-ChildItem -Recurse -Depth, Move-Item
       - ~100 lignes

    === NOMMAGE (3 commandes) ===

    3. prefix.md — /file-prefix
       - Ajoute préfixe date ISO 8601 aux fichiers
       - Modes : add, remove, update
       - Script PS : Rename-Item avec Get-Date format
       - ~100 lignes

    4. normalize.md — /file-normalize
       - Normalise noms (espaces→tirets, accents, caractères spéciaux)
       - Modes : preview, execute, rules (afficher règles actives)
       - Script PS : regex replace, Unidecode
       - ~120 lignes

    5. version.md — /file-version
       - Gère versions (v01, v02...) et détecte les anciennes
       - Modes : list, bump, clean-old, compare
       - Script PS : regex match v\d+, Sort-Object
       - ~100 lignes

    === ANALYSE (2 commandes) ===

    6. audit.md — /file-audit
       - Audit qualité nommage et organisation d'un dossier
       - Modes : quick (score), full (rapport détaillé), fix (corrections)
       - Vérifie : conventions nommage, profondeur, doublons, extensions
       - ~150 lignes

    7. old.md — /file-old
       - Trouve fichiers anciens/obsolètes (>N jours sans accès)
       - Modes : list, archive, delete (avec confirmation)
       - Script PS : Where-Object LastWriteTime -lt (Get-Date).AddDays(-N)
       - ~100 lignes

    === NETTOYAGE (1 commande) ===

    8. trash.md — /file-trash
       - Gère la corbeille Windows
       - Modes : list, empty, restore, size
       - Script PS : Shell.Application COM object
       - ~100 lignes

    === BACKUP & SYNC (3 commandes) ===

    9. backup.md — /file-backup
       - Sauvegarde avec structure (ZIP, copie, incremental)
       - Modes : full, incremental, schedule
       - Script PS : Compress-Archive, robocopy /MIR
       - ~120 lignes

    10. sync.md — /file-sync
        - Synchronise deux dossiers (bidirectionnel)
        - Modes : preview, execute, watch
        - Script PS : robocopy, Compare-Object
        - ~120 lignes

    11. mirror.md — /file-mirror
        - Miroir exact d'un dossier (supprime les extras dans la destination)
        - Modes : preview, execute
        - Script PS : robocopy /MIR /PURGE
        - ~80 lignes

    === WIZARD (1 commande) ===

    12. wizard.md — /file-wizard
        - Assistant configuration guidée pour organiser un nouveau dossier
        - Étapes : analyser, proposer structure, appliquer, vérifier
        - ~120 lignes

  ALSO: Mettre à jour fileorg-skill/SKILL.md :
    - Retirer tous les [PREVU]
    - Mettre à jour count (9 → 21 cmd, 2 → 3 wizards)
    - Si SKILL.md dépasse 500 lignes, refactorer dans references/
```

### Phase 6 : Enrichissement Docker + Linux SKILL.md

```yaml
Task 12:
  action: MODIFY
  path: ~/.claude/skills/docker-skill/SKILL.md
  description: |
    Ajouter après les commandes :

    ## Best Practices 2025-2026
    - Multi-stage builds pour réduire la taille des images
    - Rootless Docker pour la sécurité en production
    - Docker Scout / Trivy pour le scan de vulnérabilités
    - Compose v2 (plugin Docker, pas docker-compose standalone)
    - BuildKit activé par défaut (DOCKER_BUILDKIT=1)
    - OCI images et attestations SBOM
    - Health checks dans tous les Dockerfile

    ## Références
    - [Docker Docs](https://docs.docker.com/)
    - [Docker Compose](https://docs.docker.com/compose/)
    - [Docker Security](https://docs.docker.com/engine/security/)
    - [Docker Scout](https://docs.docker.com/scout/)
    - [Best Practices Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

Task 13:
  action: MODIFY
  path: ~/.claude/skills/linux-skill/SKILL.md
  description: |
    Ajouter après les commandes :

    ## Best Practices 2025-2026
    - Systemd pour tous les services (pas init.d)
    - UFW/firewalld pour le firewall (pas iptables direct)
    - Fail2ban pour la protection SSH
    - Unattended-upgrades pour les mises à jour automatiques
    - Timesyncd/chrony pour la synchronisation NTP
    - Journalctl pour les logs (pas syslog direct)
    - SSH key-only auth (désactiver PasswordAuthentication)

    ## Références
    - [Ubuntu Server Guide](https://ubuntu.com/server/docs)
    - [Debian Admin Handbook](https://debian-handbook.info/)
    - [RHEL Documentation](https://docs.redhat.com/)
    - [Arch Wiki](https://wiki.archlinux.org/) (référence universelle)
    - [Linux Security Hardening](https://www.cisecurity.org/benchmark/ubuntu_linux)
```

### Phase 7 : Mise à jour CLAUDE.md et meta-router counts

```yaml
Task 14:
  action: MODIFY
  path: ~/.claude/CLAUDE.md
  description: |
    Mettre à jour la table "Skills (12 actifs + meta-router)" :
    - proxmox-skill : garder "22 cmd, 11 wizards" (vérifier count réel)
    - windows-skill : garder "37 cmd, 10 wizards"
    - docker-skill : 10 → 13 cmd, 3 wizards
    - linux-skill : 12 → 17 cmd, 3 wizards
    - obsidian-skill : 8 → 31 cmd, 1 → 4 wizards
    - fileorg-skill : 9 → 21 cmd, 2 → 3 wizards
    - qelectrotech-skill : 42 → 35 cmd (correction!), 9 wizards
    - Tous les autres : vérifier et corriger si nécessaire

    IMPORTANT : Compter les fichiers .md réels dans commands/ et wizards/
    pour chaque skill APRÈS les créations. Ne pas deviner.

Task 15:
  action: MODIFY
  path: ~/.claude/skills/SKILL.md (meta-router)
  description: |
    Mettre à jour les counts dans le meta-router pour correspondre
    aux nouveaux totaux de chaque skill.
    Vérifier que pai-admin-skill n'est pas référencé.
```

### Phase 8 : Validation

```yaml
Task 16:
  action: VALIDATE
  description: |
    Validation 3 niveaux complète.

    Niveau 1 — Structure :
    - Vérifier que pai-admin-skill n'existe plus
    - Vérifier que {commands,wizards,templates} n'existe plus
    - Compter les fichiers .md dans commands/ de chaque skill modifié
    - Vérifier que QET SKILL.md < 500 lignes
    - Vérifier que meta-router SKILL.md < 500 lignes
    - Vérifier frontmatter YAML dans tous les SKILL.md
    - Vérifier que les references/ de QET contiennent les 11 fichiers

    Niveau 2 — Fonctionnel :
    - Vérifier que chaque nouveau .md a les sections requises :
      titre, syntaxe, actions/modes, options, exemples
    - Vérifier cohérence des noms de commandes dans les fichiers

    Niveau 3 — Intégration :
    - Vérifier que CLAUDE.md reflète les counts réels
    - Vérifier que le meta-router liste les 12 skills avec bons counts
    - Vérifier cohérence totale (meta-router counts = CLAUDE.md counts = filesystem)
```

## Points d'intégration
```yaml
ROUTER:
  - Meta-router (skills/SKILL.md) : mettre à jour tous les counts
  - Supprimer toute référence à pai-admin-skill
  - Vérifier que les 43 nouvelles commandes sont routables via préfixes existants

CLAUDE.MD:
  - Mise à jour obligatoire : table des skills avec nouveaux counts
  - Vérifier section Hooks (pas de changement attendu)

MCP:
  - Pas d'impact sur knowledge-assistant

VAULT:
  - Pas de notes vault à créer pour cette tâche
```

## Validation Loop

### Niveau 1 : Structure & Syntax
```powershell
# pai-admin-skill supprimé
!(Test-Path "~/.claude/skills/pai-admin-skill")

# Dossier parasite supprimé
!(Test-Path "~/.claude/skills/fileorg-skill/{commands,wizards,templates}")

# QET SKILL.md < 500 lignes
(Get-Content "~/.claude/skills/qelectrotech-skill/SKILL.md").Count -lt 500

# Meta-router < 500 lignes
(Get-Content "~/.claude/skills/SKILL.md").Count -lt 500

# QET references/ créé (11 fichiers)
(Get-ChildItem "~/.claude/skills/qelectrotech-skill/references/*.md").Count -eq 11

# Frontmatter YAML présent
Select-String -Path "~/.claude/skills/vault-guardian-skill/SKILL.md" -Pattern "^---" | Measure-Object

# Nouveaux fichiers commandes existent
(Get-ChildItem "~/.claude/skills/docker-skill/commands/*.md").Count -eq 13
(Get-ChildItem "~/.claude/skills/linux-skill/commands/*.md").Count -eq 17
# ... etc pour chaque skill
```

### Niveau 2 : Fonctionnel
```powershell
# Chaque nouveau .md a les sections requises
$required = @("# /", "## Syntaxe", "## Exemples")
Get-ChildItem "~/.claude/skills/*/commands/*.md" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    foreach ($section in $required) {
        if ($content -notmatch [regex]::Escape($section)) {
            Write-Warning "MISSING '$section' in $($_.FullName)"
        }
    }
}
```

### Niveau 3 : Intégration
```powershell
# Counts dans CLAUDE.md correspondent au filesystem
# Pour chaque skill, comparer le count déclaré vs fichiers réels
$skills = Get-ChildItem "~/.claude/skills" -Directory | Where-Object { $_.Name -ne "commands" }
foreach ($skill in $skills) {
    $cmdCount = (Get-ChildItem "$($skill.FullName)/commands/*.md" -ErrorAction SilentlyContinue).Count
    Write-Output "$($skill.Name): $cmdCount commands"
}
```

## Checklist de validation finale
- [ ] pai-admin-skill supprimé
- [ ] Dossier parasite fileorg supprimé
- [ ] QET SKILL.md < 500 lignes + 11 references/
- [ ] Meta-router SKILL.md < 500 lignes
- [ ] Frontmatter YAML sur tous les SKILL.md
- [ ] 3 commandes docker créées
- [ ] 5 commandes linux créées
- [ ] 23 commandes obsidian créées
- [ ] 12 commandes fileorg créées
- [ ] Docker + Linux SKILL.md enrichis (Best Practices + Références)
- [ ] Tous les [PREVU] retirés des SKILL.md
- [ ] CLAUDE.md counts à jour
- [ ] Meta-router counts à jour
- [ ] Validation 3 niveaux : 10/10

## Anti-Patterns à éviter
- Ne pas créer de commandes vides (placeholder sans contenu)
- Ne pas copier-coller sans adapter (chaque commande doit être unique et utile)
- Ne pas oublier la section "## Voir Aussi" pour les commandes liées
- Ne pas dépasser 500 lignes dans un SKILL.md après mise à jour
- Ne pas modifier les commandes existantes qui fonctionnent déjà
- Ne pas créer de notes vault pour cette tâche (c'est un fix technique)

---

**Score de confiance PRP : 7/10**

Raisons du 7 (pas 9) :
- Scope très large (43 commandes + refactoring + cleanup)
- Les commandes obsidian (23) nécessitent une connaissance profonde des APIs Obsidian
- Le refactoring QET (944 lignes) est délicat (il faut couper aux bons endroits)
- Risque de dépasser la fenêtre de contexte sur un single pass

Recommandation : Exécuter en 2-3 passes si nécessaire (Phase 1-3, puis Phase 4-5, puis Phase 6-8).
