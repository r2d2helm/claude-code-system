# Super Agent Windows 11/Server 2025

Agent d'administration Windows avec commandes slash, wizards interactifs et best practices 2025-2026.

## Compatibilité

| Composant | Version |
|-----------|---------|
| Windows | 11 23H2+, Server 2022/2025 |
| PowerShell | 7.4+ (recommandé), 5.1 (compatible) |
| WinRM | Activé pour administration distante |
| .NET | 8.0+ pour outils modernes |

## Commandes Slash

### Système & Diagnostic

| Commande | Description |
|----------|-------------|
| `/win-diagnostic` | Diagnostic système complet (CPU, RAM, disque, réseau) |
| `/win-perf` | Analyse performances et goulots d'étranglement |
| `/win-maintenance` | Nettoyage, optimisation, santé système |
| `/win-inventory` | Inventaire matériel et logiciel |
| `/win-troubleshoot` | Résolution problèmes courants |
| `/win-update` | Windows Update et gestion patches |
| `/win-logs` | Analyse Event Viewer et journaux |

### Réseau

| Commande | Description |
|----------|-------------|
| `/win-network` | Configuration réseau, IP, DNS, passerelle |
| `/win-vpn` | VPN Windows (IKEv2, L2TP, SSTP, WireGuard) |
| `/win-wifi` | WiFi, profils sans fil, diagnostics |
| `/win-rdp` | Remote Desktop configuration et sécurité |
| `/win-ssh` | OpenSSH Server/Client Windows |
| `/win-firewall` | Windows Defender Firewall avancé |

### Stockage

| Commande | Description |
|----------|-------------|
| `/win-disk` | Gestion disques, partitions, Storage Spaces |
| `/win-backup` | Sauvegarde Windows, wbadmin, VSS |

### Sécurité

| Commande | Description |
|----------|-------------|
| `/win-security` | Audit sécurité global et hardening |
| `/win-defender` | Windows Defender avancé, ASR, EDR |
| `/win-bitlocker` | Chiffrement BitLocker TPM/PIN |
| `/win-certs` | Certificats, PKI, SSL/TLS |

### Utilisateurs & Services

| Commande | Description |
|----------|-------------|
| `/win-users` | Gestion utilisateurs locaux et groupes |
| `/win-services` | Services Windows, dépendances, recovery |
| `/win-apps` | Applications installées, AppX, MSIX |

### Développement & Conteneurs

| Commande | Description |
|----------|-------------|
| `/win-git` | Git configuration et workflows |
| `/win-docker` | Docker Desktop, conteneurs Windows/Linux |
| `/win-wsl` | Windows Subsystem for Linux 2 |
| `/win-hyperv` | Hyper-V, VMs, intégration |
| `/win-powershell` | PowerShell 7, modules, profils |
| `/win-env` | Variables environnement, PATH |
| `/win-pkg` | Gestionnaires paquets (winget, choco, scoop) |

### Infrastructure & Serveur

| Commande | Description |
|----------|-------------|
| `/win-iis` | Internet Information Services |
| `/win-tasks` | Planificateur de tâches |
| `/win-registry` | Registre Windows, clés, optimisations |
| `/win-drivers` | Pilotes, mise à jour, rollback |

### Périphériques

| Commande | Description |
|----------|-------------|
| `/win-printer` | Imprimantes, spooler, dépannage |
| `/win-bluetooth` | Périphériques Bluetooth |

### Wizards Interactifs

| Commande | Description |
|----------|-------------|
| `/win-wizard` | Assistant configuration guidée |

## Syntaxe

```
/win-<commande> [action] [options]
```

### Exemples

```powershell
/win-diagnostic full          # Diagnostic complet
/win-network status           # État réseau
/win-defender scan quick      # Scan rapide Defender
/win-backup create            # Créer sauvegarde
/win-wizard setup             # Assistant setup initial
/win-wizard security          # Assistant hardening
```

## Wizards Disponibles

| Wizard | Étapes | Description |
|--------|--------|-------------|
| Setup Initial | 8 | Configuration post-installation complète |
| Security Hardening | 6 | Sécurisation système production |
| Network Setup | 5 | Configuration réseau entreprise |
| AD Join | 4 | Jonction domaine Active Directory |
| Dev Environment | 6 | Environnement développeur complet |
| Server Roles | 5 | Installation rôles Windows Server |
| Backup Strategy | 4 | Configuration stratégie sauvegarde |
| Remote Access | 5 | RDP, SSH, VPN sécurisés |
| Performance Tuning | 4 | Optimisation performances |
| Troubleshooting | 5 | Diagnostic problèmes guidé |

## Best Practices 2025-2026

### Sécurité
- Windows Defender activé avec ASR rules
- BitLocker TPM+PIN sur tous les disques système
- Credential Guard et HVCI activés
- LAPS pour mots de passe admin locaux
- AppLocker ou WDAC pour contrôle applications
- SMB 3.1.1 avec chiffrement obligatoire

### PowerShell
- PowerShell 7.4+ comme shell par défaut
- Execution Policy RemoteSigned minimum
- Transcription et logging activés
- Modules signés uniquement en production

### Réseau
- TLS 1.3 uniquement (désactiver TLS 1.0/1.1)
- DNS over HTTPS (DoH) activé
- Firewall profil Domain/Private/Public configuré
- IPv6 désactivé si non utilisé

### Maintenance
- Windows Update : Patch Tuesday + 7 jours
- Redémarrage planifié hebdomadaire
- Nettoyage disque mensuel automatisé
- Monitoring avec Windows Admin Center

### Sauvegarde
- Règle 3-2-1 : 3 copies, 2 médias, 1 hors-site
- VSS pour snapshots applicatifs
- Test restauration trimestriel
- Rétention : 7 jours local, 30 jours archive

## Structure Fichiers

```
windows-skill/
├── SKILL.md                 # Ce fichier
├── commands/                # Commandes slash
│   ├── diagnostic.md
│   ├── network.md
│   ├── security.md
│   ├── defender.md
│   ├── ... (36 fichiers)
└── wizards/                 # Assistants interactifs
    ├── wizard-setup.md
    ├── wizard-security.md
    ├── wizard-network.md
    └── ... (10 fichiers)
```

## Références

- [Microsoft Docs](https://learn.microsoft.com/windows/)
- [PowerShell Documentation](https://learn.microsoft.com/powershell/)
- [Windows Security Baselines](https://learn.microsoft.com/windows/security/threat-protection/windows-security-configuration-framework/windows-security-baselines)
- [Windows Admin Center](https://learn.microsoft.com/windows-server/manage/windows-admin-center/overview)
