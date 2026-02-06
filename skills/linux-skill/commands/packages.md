# Commande: /lx-packages

Gestion des packages (auto-detection apt/dnf).

## Syntaxe

```
/lx-packages [action] [package]
```

## Actions (apt - Debian/Ubuntu)

```bash
# Mettre a jour la liste
sudo apt update

# Mettre a jour les packages
sudo apt upgrade -y

# Installer
sudo apt install -y <package>

# Supprimer
sudo apt remove <package>
sudo apt autoremove -y

# Rechercher
apt search <keyword>

# Info sur un package
apt show <package>

# Packages avec mises a jour de securite
sudo apt list --upgradable 2>/dev/null | grep -i security
```

## Actions (dnf - RHEL/Rocky)

```bash
sudo dnf check-update
sudo dnf upgrade -y
sudo dnf install -y <package>
sudo dnf remove <package>
dnf search <keyword>
dnf info <package>
sudo dnf updateinfo list security
```

## Options

| Option | Description |
|--------|-------------|
| `update` | Mettre a jour la liste |
| `upgrade` | Mettre a jour les packages |
| `install` | Installer un package |
| `remove` | Supprimer un package |
| `search` | Rechercher |
| `security` | Mises a jour de securite |

## Exemples

```bash
/lx-packages update            # Rafraichir les repos
/lx-packages install htop      # Installer htop
/lx-packages security          # Check securite
```
