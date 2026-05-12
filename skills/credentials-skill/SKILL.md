---
name: credentials-skill
description: "Gestion credentials : registre structure, validation, rotation, audit, export."
prefix: /cred-*
version: 1.0.0
---

# Super Agent Credential Management

Agent intelligent pour gerer les credentials du homelab : registre Markdown structure, validation de connectivite, rotation planifiee, audit de compliance, import/export multi-format.

## Philosophie

> "Un credential non inventorie est un credential compromis. Un credential non rotationne est une porte ouverte."

## Architecture

### Registre

Le registre est un ensemble de fichiers Markdown enrichis YAML, un par service :

```
data/registry/
├── _index.json        # Index auto-genere (metadata sans passwords)
├── _archive/          # Credentials supprimes (archivage)
├── beszel.md          # Un fichier par service
├── postgres-shared.md
├── litellm.md
└── ...
```

Chaque fichier contient :
- **Frontmatter YAML** : metadata structuree (service, slug, category, host, port, vm, criticality, auth_type, rotation, validation)
- **Body Markdown** : acces (URL, username, password), container info, rotation notes

### Perimetre

| Cible | IP | Services |
|-------|----|----------|
| VM 100 r2d2-stage | 192.168.1.162 | Beszel Hub, Uptime Kuma, Netdata, Dozzle, ntfy |
| VM 103 r2d2-main | 192.168.1.163 | Supabase, LiteLLM, Langfuse, Taskyn, monitoring |
| VM 104 r2d2-store | 192.168.1.164 | PostgreSQL, NFS, monitoring |
| VM 105 r2d2-lab | 192.168.1.161 | RAG, Taskyn |
| Proxmox Host | 192.168.1.215 | Web UI, SSH |
| PC Windows | localhost | SSH agent Beszel, RDP |

### Scripts PowerShell

| Script | Role |
|--------|------|
| `CredentialRegistry.psm1` | Module core : CRUD, parse YAML, index |
| `Test-Credential.ps1` | Validation connectivite (SSH, HTTP, DB, API, Telegram) |
| `New-SecurePassword.ps1` | Generation cryptographique securisee |
| `Export-Credentials.ps1` | Export Bitwarden CSV / KeePass XML / JSON / CSV |
| `Import-Credentials.ps1` | Import multi-format avec detection auto |
| `Invoke-CredentialDiscovery.ps1` | Scan VMs via SSH (.env, docker inspect) |
| `Measure-CredentialHealth.ps1` | Score sante /100 (age, force, couverture, fraicheur) |
| `Sync-CredentialRegistry.ps1` | Comparaison registre vs valeurs live |

Tous compatibles PS 5.1, encodes UTF-8 BOM.

## Commandes Slash

### Dashboard & Inventaire

| Commande | Description |
|----------|-------------|
| `/cred-status` | Dashboard synthese : totaux, rotations, validations, score |
| `/cred-list [filtre]` | Lister/filtrer par category, vm, status, criticality |
| `/cred-show <slug>` | Details complets d'un credential (password masque par defaut) |

### CRUD

| Commande | Description |
|----------|-------------|
| `/cred-add <service>` | Ajouter une nouvelle entree au registre |
| `/cred-edit <slug>` | Modifier un credential existant |
| `/cred-remove <slug>` | Supprimer (avec archivage) |

### Validation & Decouverte

| Commande | Description |
|----------|-------------|
| `/cred-validate [slug\|all]` | Tester la connectivite (SSH, HTTP, DB, API, Telegram) |
| `/cred-discover [vm]` | Scanner VMs pour secrets non repertories |
| `/cred-sync [vm]` | Comparer registre vs valeurs live (detecter drift) |

### Rotation & Audit

| Commande | Description |
|----------|-------------|
| `/cred-rotate <slug>` | Rotation guidee : generer, deployer, valider, logger |
| `/cred-schedule` | Calendrier de rotation (overdue, due soon, on track) |
| `/cred-audit` | Rapport compliance : score /100 + recommandations |

### Import / Export / Backup

| Commande | Description |
|----------|-------------|
| `/cred-export <format>` | Export vers Bitwarden CSV, KeePass XML, JSON, CSV |
| `/cred-import <fichier>` | Import depuis Bitwarden, .env, docker-compose, markdown |
| `/cred-backup` | Sauvegarder le registre (archive + checksums) |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/cred-wizard setup` | Migration initiale depuis vm100-credentials.md |
| `/cred-wizard rotate` | Rotation groupee multi-services avec rollback |
| `/cred-wizard onboard` | Onboarding d'un nouveau service (decouverte + enregistrement) |

## Categories de Credentials

| Category | Services | Auth Type |
|----------|----------|-----------|
| `monitoring` | Beszel, Uptime Kuma, Netdata, Dozzle, ntfy | password |
| `database` | PostgreSQL, Redis | password |
| `api` | LiteLLM, Langfuse, Taskyn | apikey/password |
| `ssh` | VMs, Proxmox | ssh-key |
| `web` | Supabase Studio, NetBox, pgAdmin | password |
| `bot` | Telegram | token |
| `infra` | Docker, NFS, SMTP | password/none |
| `oauth` | GitHub, Google | oauth |

## Score de Sante (/100)

| Axe | Points | Criteres |
|-----|--------|----------|
| Age | /25 | Penalite pour credentials jamais rotationnees ou > interval |
| Force | /25 | Longueur, complexite, entropie des passwords |
| Couverture | /25 | % de services du homelab couverts par le registre |
| Fraicheur | /25 | % de credentials valides recemment (< 7 jours) |

## Securite

### Protection des donnees
- Le registre est dans `~/.claude/skills/` (PAS dans le vault Obsidian)
- `path_guard` bloque le Read tool direct sur `data/registry/`
- Les commandes accedent aux credentials via scripts PowerShell (Bash tool)
- Export protege : fichiers dans `data/exports/`, jamais envoyes en externe
- Archivage avant toute suppression dans `_archive/`

### Bonnes pratiques
- Rotation tous les 90 jours (par defaut, configurable par service)
- Passwords generes cryptographiquement (RandomNumberGenerator)
- Validation reguliere de la connectivite
- Audit periodique avec score de sante

## Integration avec les Autres Skills

| Skill | Relation |
|-------|----------|
| **security-skill** | `/sec-passwords` redirige vers `/cred-audit` pour la gestion complete |
| **monitoring-skill** | Credentials des services monitores (Beszel, Uptime Kuma, Netdata) |
| **backup-skill** | `/cred-backup` pour sauvegarder le registre |
| **docker-skill** | Credentials extraits des containers (docker inspect) |
| **linux-skill** | Validation SSH, deploiement des rotations sur les VMs |

## References

- `references/credential-types.md` : types, categories, criticality
- `references/rotation-procedures.md` : procedures de rotation par service
- `references/validation-methods.md` : methodes de test par type

## Troubleshooting

### Le registre est vide
1. Lancer `/cred-wizard setup` pour migrer depuis vm100-credentials.md
2. Ou `/cred-import` pour importer depuis une autre source

### Validation echoue sur toutes les VMs
1. Verifier la connectivite SSH : `ssh vm100 echo ok`
2. Verifier les cles SSH : `~/.ssh/config`
3. Verifier que les services tournent : `ssh vm100 docker ps`

### Index desynchronise
```
powershell.exe -NoProfile -Command "
Import-Module ~/.claude/skills/credentials-skill/scripts/CredentialRegistry.psm1 -Force
Update-CredentialIndex
"
```
