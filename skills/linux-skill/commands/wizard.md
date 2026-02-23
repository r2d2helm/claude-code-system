# Commande: /lx-wizard

Assistants de configuration guides pour taches complexes.

## Syntaxe

```
/lx-wizard <wizard-name> [options]
```

## Wizards Disponibles

| Wizard | Description | Fichier |
|--------|-------------|---------|
| `setup` | Hardening initial du serveur | `wizards/wizard-setup.md` |
| `lamp` | Installation stack LAMP | `wizards/wizard-lamp.md` |
| `docker-host` | Configuration hote Docker | `wizards/wizard-docker-host.md` |

## Description

Les wizards guident pas a pas pour les configurations complexes.
Chaque wizard pose des questions et genere les commandes adaptees.

## Wizard: setup

Securisation initiale d'un serveur Linux fraichement installe.

```bash
/lx-wizard setup
```

Etapes couvertes :
1. Mise a jour systeme complete
2. Creation utilisateur administrateur avec sudo
3. Configuration SSH (cles Ed25519, desactivation password auth)
4. Firewall UFW (politique deny, ouverture SSH)
5. Fail2ban pour protection brute-force
6. Configuration NTP (chrony/systemd-timesyncd)
7. Activation mises a jour automatiques (unattended-upgrades)
8. Verification finale

## Wizard: lamp

Installation d'une stack LAMP (Linux, Apache, MySQL/MariaDB, PHP).

```bash
/lx-wizard lamp
```

Etapes couvertes :
1. Installation Apache2
2. Installation MariaDB/MySQL
3. Securisation base de donnees (mysql_secure_installation)
4. Installation PHP et modules
5. Configuration vhost Apache
6. Test avec phpinfo
7. Configuration firewall (ports 80, 443)

## Wizard: docker-host

Configuration d'un serveur comme hote Docker.

```bash
/lx-wizard docker-host
```

Etapes couvertes :
1. Installation Docker CE depuis le depot officiel
2. Configuration du daemon Docker (logging, storage driver)
3. Installation Docker Compose
4. Creation utilisateur Docker (groupe docker)
5. Configuration firewall pour Docker
6. Activation du service au demarrage
7. Test avec conteneur hello-world
8. Configuration log rotation

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher les commandes sans executer |
| `--auto` | Valeurs par defaut sans interaction |
| `--verbose` | Details supplementaires a chaque etape |

## Exemples

```bash
/lx-wizard setup                  # Hardening initial
/lx-wizard lamp                   # Stack LAMP
/lx-wizard docker-host            # Hote Docker
/lx-wizard setup --dry-run        # Voir les commandes sans executer
```

## Voir Aussi

- `/lx-security` - Audit de securite
- `/lx-ssh` - Configuration SSH detaillee
- `/lx-firewall` - Gestion firewall
- `/lx-docker` - Gestion conteneurs Docker
- `/lx-nginx` - Alternative a Apache avec Nginx
