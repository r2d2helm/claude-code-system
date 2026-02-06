# 🖥️ Super Agent Windows 11/Server 2025

Agent d'administration Windows complet pour Claude Code avec commandes slash, wizards interactifs et best practices 2025-2026.

## 📦 Contenu

```
windows-skill/
├── SKILL.md              # Point d'entrée principal
├── README.md             # Ce fichier
├── commands/             # 36 commandes slash
│   ├── diagnostic.md     # Diagnostic système
│   ├── network.md        # Configuration réseau
│   ├── security.md       # Audit sécurité
│   ├── defender.md       # Windows Defender
│   ├── ... (32 autres)
└── wizards/              # 10 assistants interactifs
    ├── wizard-setup.md       # Setup initial
    ├── wizard-security.md    # Hardening sécurité
    ├── wizard-network.md     # Configuration réseau
    ├── wizard-ad-join.md     # Jonction AD
    ├── wizard-dev-env.md     # Environnement dev
    ├── wizard-server-roles.md# Rôles serveur
    ├── wizard-backup.md      # Stratégie backup
    ├── wizard-remote-access.md# Accès distant
    ├── wizard-performance.md # Optimisation
    └── wizard-troubleshoot.md# Dépannage
```

## 🚀 Installation

### Windows PowerShell

```powershell
# Extraire dans le dossier Claude Code
Expand-Archive -Path windows-skill.zip -DestinationPath "$env:USERPROFILE\.claude\skills\" -Force

# Vérifier l'installation
Get-ChildItem "$env:USERPROFILE\.claude\skills\windows-skill"
```

## 📋 Commandes Disponibles

### Système & Diagnostic
| Commande | Description |
|----------|-------------|
| `/win-diagnostic` | Diagnostic complet système |
| `/win-perf` | Analyse performances |
| `/win-maintenance` | Nettoyage et optimisation |
| `/win-inventory` | Inventaire matériel/logiciel |
| `/win-troubleshoot` | Résolution problèmes |
| `/win-update` | Windows Update |
| `/win-logs` | Analyse Event Viewer |

### Réseau
| Commande | Description |
|----------|-------------|
| `/win-network` | Configuration IP/DNS |
| `/win-vpn` | VPN (IKEv2, WireGuard...) |
| `/win-wifi` | WiFi et sans fil |
| `/win-rdp` | Remote Desktop |
| `/win-ssh` | OpenSSH Server/Client |
| `/win-firewall` | Windows Firewall |

### Stockage
| Commande | Description |
|----------|-------------|
| `/win-disk` | Disques et partitions |
| `/win-backup` | Sauvegarde Windows |

### Sécurité
| Commande | Description |
|----------|-------------|
| `/win-security` | Audit sécurité global |
| `/win-defender` | Windows Defender avancé |
| `/win-bitlocker` | Chiffrement BitLocker |
| `/win-certs` | Certificats PKI |

### Utilisateurs & Services
| Commande | Description |
|----------|-------------|
| `/win-users` | Gestion utilisateurs |
| `/win-services` | Services Windows |
| `/win-apps` | Applications installées |

### Développement
| Commande | Description |
|----------|-------------|
| `/win-git` | Configuration Git |
| `/win-docker` | Docker Desktop |
| `/win-wsl` | WSL 2 |
| `/win-hyperv` | Hyper-V |
| `/win-powershell` | PowerShell 7 |
| `/win-env` | Variables environnement |
| `/win-pkg` | Gestionnaires paquets |

### Infrastructure
| Commande | Description |
|----------|-------------|
| `/win-iis` | IIS Web Server |
| `/win-tasks` | Tâches planifiées |
| `/win-registry` | Registre Windows |
| `/win-drivers` | Pilotes |

### Périphériques
| Commande | Description |
|----------|-------------|
| `/win-printer` | Imprimantes |
| `/win-bluetooth` | Bluetooth |

## 🧙 Wizards Interactifs

| Wizard | Commande | Description |
|--------|----------|-------------|
| Setup Initial | `/win-wizard setup` | Configuration post-installation (8 étapes) |
| Security | `/win-wizard security` | Hardening sécurité (6 étapes) |
| Network | `/win-wizard network` | Configuration réseau (5 étapes) |
| AD Join | `/win-wizard ad-join` | Jonction Active Directory (4 étapes) |
| Dev Environment | `/win-wizard dev` | Environnement développeur (6 étapes) |
| Server Roles | `/win-wizard server-roles` | Installation rôles serveur (5 étapes) |
| Backup | `/win-wizard backup` | Stratégie sauvegarde (4 étapes) |
| Remote Access | `/win-wizard remote-access` | RDP/SSH/WinRM sécurisé (5 étapes) |
| Performance | `/win-wizard performance` | Optimisation système (4 étapes) |
| Troubleshoot | `/win-wizard troubleshoot` | Diagnostic guidé (5 étapes) |

## 💡 Exemples d'Utilisation

```powershell
# Diagnostic rapide
/win-diagnostic quick

# Configurer le réseau
/win-wizard network

# Sécuriser le système
/win-wizard security

# Installer environnement dev
/win-wizard dev

# Dépanner un problème réseau
/win-troubleshoot network

# Configurer Windows Defender
/win-defender config full
```

## ✅ Best Practices 2025-2026

### Sécurité
- Windows Defender avec ASR rules activées
- BitLocker TPM+PIN sur disques système
- Credential Guard et HVCI
- LAPS pour mots de passe admin locaux
- SMB 3.1.1 avec chiffrement

### PowerShell
- PowerShell 7.4+ par défaut
- Execution Policy RemoteSigned
- Transcription activée
- Modules signés en production

### Réseau
- TLS 1.3 uniquement
- DNS over HTTPS (DoH)
- LLMNR désactivé
- IPv6 désactivé si non utilisé

### Maintenance
- Windows Update : Patch Tuesday + 7 jours
- Redémarrage hebdomadaire planifié
- Nettoyage disque mensuel
- Windows Admin Center pour monitoring

## 📚 Références

- [Microsoft Docs](https://learn.microsoft.com/windows/)
- [PowerShell Documentation](https://learn.microsoft.com/powershell/)
- [Windows Security Baselines](https://learn.microsoft.com/windows/security/)
- [Windows Admin Center](https://learn.microsoft.com/windows-server/manage/windows-admin-center/)

## 📄 Licence

MIT License - Libre d'utilisation et modification.

---

**Version**: 1.0.0  
**Compatibilité**: Windows 11 23H2+, Windows Server 2022/2025  
**Dernière mise à jour**: Février 2026
