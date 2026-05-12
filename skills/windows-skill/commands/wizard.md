# /win-wizard - Assistants Interactifs Windows

## Description

Wizards de configuration guidée pour Windows 10/11 et Windows Server. Interface conversationnelle avec étapes numérotées, validation à chaque étape et génération de scripts PowerShell.

## Syntaxe

```
/win-wizard <wizard> [--auto] [--export] [--dry-run]
```

## Wizards Disponibles

| Wizard | Fichier | Description | Etapes |
|--------|---------|-------------|--------|
| `setup` | [wizard-setup.md](../wizards/wizard-setup.md) | Configuration initiale poste de travail | 10 |
| `security` | [wizard-security.md](../wizards/wizard-security.md) | Hardening sécurité complet (CIS/Microsoft Baselines) | 8 |
| `developer` | [wizard-dev-env.md](../wizards/wizard-dev-env.md) | Setup environnement développeur | 7 |
| `server` | [wizard-server-roles.md](../wizards/wizard-server-roles.md) | Configuration Windows Server 2022/2025 | 9 |
| `network` | [wizard-network.md](../wizards/wizard-network.md) | Configuration réseau avancée | 6 |
| `backup` | [wizard-backup.md](../wizards/wizard-backup.md) | Stratégie sauvegarde | 5 |
| `domain` | [wizard-ad-join.md](../wizards/wizard-ad-join.md) | Jonction domaine Active Directory | 6 |
| `performance` | [wizard-performance.md](../wizards/wizard-performance.md) | Optimisation performance système | 5 |
| `remote` | [wizard-remote-access.md](../wizards/wizard-remote-access.md) | Accès distant (RDP, SSH, VPN) | 5 |
| `troubleshoot` | [wizard-troubleshoot.md](../wizards/wizard-troubleshoot.md) | Diagnostic et résolution de problèmes | 6 |

## Options

| Option | Description |
|--------|-------------|
| `--auto` | Mode automatique avec valeurs par défaut |
| `--export` | Exporter script PowerShell généré |
| `--dry-run` | Afficher commandes sans exécuter |

## Utilisation

```powershell
# Lancer un wizard spécifique
/win-wizard setup

# Mode automatique (valeurs par défaut)
/win-wizard security --auto

# Exporter script sans exécuter
/win-wizard developer --export --dry-run

# Aide sur un wizard
/win-wizard server --help
```

## Références

- [Microsoft Security Baselines](https://docs.microsoft.com/windows/security/threat-protection/windows-security-baselines)
- [CIS Benchmarks Windows](https://www.cisecurity.org/benchmark/microsoft_windows_desktop)
- [PowerShell Documentation](https://docs.microsoft.com/powershell)
