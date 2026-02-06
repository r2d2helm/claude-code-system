# Commande: /context

Gestion du contexte actif pour le routing des requêtes.

## Syntaxe

```
/context [action] [agent]
```

## Actions

### /context (sans argument)

Affiche le contexte actuellement détecté :

```
╔══════════════════════════════════════════════════════════════╗
║                   🎯 CONTEXTE ACTUEL                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Mode      : 🔄 AUTO (détection automatique)                 ║
║  Détecté   : 🟠 PROXMOX-SKILL                                ║
║  Confiance : ████████████░░░░░░░░ 85%                        ║
║                                                              ║
║  Keywords détectés dans la conversation:                     ║
║  • "proxmox" (×3)                                            ║
║  • "vm" (×5)                                                 ║
║  • "cluster" (×2)                                            ║
║                                                              ║
║  Historique récent:                                          ║
║  └── 🟠 proxmox → 🟠 proxmox → 🟠 proxmox                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

💡 /context set <agent> pour forcer un contexte
💡 /context auto pour réactiver la détection
```

### /context set <agent>

Force un contexte spécifique :

```
/context set windows
```

```
╔══════════════════════════════════════════════════════════════╗
║                   🔒 CONTEXTE FORCÉ                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Mode    : 🔒 FORCÉ                                          ║
║  Agent   : 🔵 WINDOWS-SKILL                                  ║
║  Préfixe : /win-*                                            ║
║                                                              ║
║  ✅ Toutes les requêtes seront traitées par windows-skill    ║
║                                                              ║
║  Commandes disponibles:                                      ║
║  /win-diagnostic, /win-network, /win-security,               ║
║  /win-defender, /win-backup, /win-wizard, ...                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

💡 /context auto pour réactiver la détection automatique
```

### /context auto

Réactive la détection automatique :

```
/context auto
```

```
╔══════════════════════════════════════════════════════════════╗
║               🔄 DÉTECTION AUTOMATIQUE ACTIVÉE               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Mode : 🔄 AUTO                                              ║
║                                                              ║
║  Le router analysera chaque requête pour détecter            ║
║  automatiquement l'agent approprié.                          ║
║                                                              ║
║  Ordre de priorité:                                          ║
║  1. Commande explicite (/pve-*, /win-*)                      ║
║  2. Keywords primaires (haute confiance)                     ║
║  3. Keywords secondaires + contexte                          ║
║  4. Historique de conversation                               ║
║  5. Demande de clarification si ambigu                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /context history

Affiche l'historique des contextes :

```
/context history
```

```
╔══════════════════════════════════════════════════════════════╗
║               📜 HISTORIQUE DES CONTEXTES                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  # │ Heure │ Agent    │ Confiance │ Trigger                  ║
║  ──┼───────┼──────────┼───────────┼────────────────────────  ║
║  1 │ 19:45 │ 🟠 pve   │    95%    │ "cluster proxmox"        ║
║  2 │ 19:42 │ 🟠 pve   │    90%    │ "/pve-status"            ║
║  3 │ 19:38 │ 🔵 win   │    85%    │ "powershell rdp"         ║
║  4 │ 19:35 │ 🔵 win   │    88%    │ "windows defender"       ║
║  5 │ 19:30 │ 🟠 pve   │    92%    │ "créer vm ubuntu"        ║
║                                                              ║
║  Distribution: 🟠 60% │ 🔵 40%                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /context clear

Réinitialise le contexte :

```
/context clear
```

```
╔══════════════════════════════════════════════════════════════╗
║                 🗑️ CONTEXTE RÉINITIALISÉ                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✅ Historique effacé                                        ║
║  ✅ Contexte forcé désactivé                                 ║
║  ✅ Mode AUTO activé                                         ║
║                                                              ║
║  Prêt pour une nouvelle session.                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Préfixes Contextuels

Alternative au `/context set`, utiliser @ pour forcer un contexte inline :

```
@proxmox Comment créer un pool ZFS?
@windows Configure le firewall pour autoriser le port 8080
@docker Lance un conteneur nginx
```

Équivalent à:
```
/context set proxmox
Comment créer un pool ZFS?
```

## Détection Multi-Contexte

Quand une requête implique plusieurs agents :

```
╔══════════════════════════════════════════════════════════════╗
║              🔀 MULTI-CONTEXTE DÉTECTÉ                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Requête: "Créer VM Windows sur Proxmox puis configurer RDP" ║
║                                                              ║
║  Contextes identifiés:                                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Phase 1: 🟠 PROXMOX                                     │ ║
║  │ └── Action: Création VM Windows                         │ ║
║  │ └── Commande: /pve-wizard vm                            │ ║
║  │                                                         │ ║
║  │ Phase 2: 🔵 WINDOWS                                     │ ║
║  │ └── Action: Configuration RDP                           │ ║
║  │ └── Commande: /win-rdp enable                           │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Exécuter séquentiellement                               ║
║  [2] Commencer par Phase 1 uniquement                        ║
║  [3] Voir les détails de chaque phase                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
