# 🎯 Meta-Agent Router

Orchestrateur intelligent pour Claude Code qui route automatiquement les requêtes vers l'agent approprié.

## 🚀 Fonctionnalités

- **Détection automatique** du contexte basée sur les keywords
- **Routing intelligent** vers le bon skill (Proxmox, Windows, etc.)
- **Gestion des ambiguïtés** avec demande de clarification
- **Support multi-contexte** pour requêtes complexes
- **Commandes universelles** `/infra` pour interface unifiée
- **Debugging** et tests du routing

## 📦 Installation

```powershell
# Extraire à la racine des skills (pas dans un sous-dossier)
Expand-Archive -Path "meta-router.zip" -DestinationPath "$env:USERPROFILE\.claude\skills\" -Force
```

### Structure Finale

```
~/.claude/skills/
├── SKILL.md                 ← Meta-Router (CE FICHIER)
├── commands/                ← Commandes du router
│   ├── agents.md
│   ├── context.md
│   ├── infra.md
│   └── router.md
├── proxmox-skill/           ← Agent Proxmox
├── windows-skill/           ← Agent Windows
└── (futurs agents...)
```

## 📋 Commandes

| Commande | Description |
|----------|-------------|
| `/agents` | Liste tous les agents disponibles |
| `/agents status` | État détaillé des agents |
| `/agents help <agent>` | Aide pour un agent |
| `/agents commands <agent>` | Liste commandes d'un agent |
| `/context` | Affiche contexte actuel |
| `/context set <agent>` | Force un contexte |
| `/context auto` | Réactive détection auto |
| `/infra [agent] <action>` | Commande universelle |
| `/router debug` | Debug dernière décision |
| `/router test "requête"` | Teste routing sans exécuter |
| `/router logs` | Historique des décisions |

## 🔄 Détection Automatique

Le router analyse les keywords pour détecter l'agent :

| Agent | Keywords Primaires |
|-------|-------------------|
| 🟠 Proxmox | proxmox, pve, qemu, lxc, ceph, zfs, vzdump, corosync |
| 🔵 Windows | windows, powershell, defender, bitlocker, rdp, ad, iis |
| 🐳 Docker | docker, container, compose, kubernetes, k8s, pod |
| 🐧 Linux | ubuntu, debian, apt, systemd, nginx, bash |

## 💡 Exemples

### Détection Auto
```
"Comment créer une VM sur Proxmox?"
→ Keywords [VM, Proxmox] → 🟠 proxmox-skill → /pve-wizard vm
```

### Contexte Forcé
```
/context set windows
"Configure le firewall"
→ 🔵 windows-skill → /win-firewall
```

### Commande Universelle
```
/infra status
→ Détecte contexte → Affiche status approprié
```

### Préfixe Inline
```
@proxmox créer un pool ZFS
→ Force 🟠 proxmox-skill
```

## 🔧 Configuration

Modifier le comportement du router :

```
/router config min_confidence 80    # Seuil de confiance
/router config ask_on_ambiguity true # Demander si ambigu
```

## 📊 Agents Supportés

| Agent | Status | Commandes | Wizards |
|-------|--------|-----------|---------|
| 🟠 Proxmox | ✅ Actif | 22 | 11 |
| 🔵 Windows | ✅ Actif | 37 | 10 |
| 🐳 Docker | ✅ Actif | 13 | 3 |
| 🐧 Linux | ✅ Actif | 17 | 3 |
| 📁 Fileorg | ✅ Actif | 20 | 1 |
| 📓 Obsidian | ✅ Actif | 28 | 3 |
| ⚡ QElectroTech | ✅ Actif | 42 | 9 |
| 📚 Knowledge | ✅ Actif | 3 | 1 |
| 👁️ KWatcher | ✅ Actif | 6 | 2 |
| 🛡️ Guardian | ✅ Actif | 3 | 0 |
| 📋 SOP Creator | ✅ Actif | 1 | 6 templates |
| 🔧 Skill Creator | ✅ Actif | 1 | 0 |

## 📄 Licence

MIT License

---

**Version**: 1.3.0
**Dernière mise à jour**: Février 2026
