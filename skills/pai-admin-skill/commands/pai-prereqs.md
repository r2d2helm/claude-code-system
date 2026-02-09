# /pai-prereqs — Verifier/installer prerequis

Verifier que tous les prerequis PAI sont presents sur le systeme. Optionnellement les installer.

## Syntaxe

```
/pai-prereqs [--install]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `--install` | Installer les prerequis manquants | Non (verifier seulement) |

## Prerequis verifies

| Prerequis | Commande test | Installation |
|-----------|---------------|-------------|
| Git | `which git` | `sudo apt install git` |
| Bun | `which bun` | `curl -fsSL https://bun.sh/install \| bash && source ~/.bashrc` |
| mpg123 | `which mpg123` | `sudo apt install mpg123` |
| notify-send | `which notify-send` | `sudo apt install libnotify-bin` |
| curl | `which curl` | `sudo apt install curl` |

## Procedure

1. Pour chaque prerequis, executer la commande test
2. Afficher un tableau recapitulatif :
   ```
   | Prerequis | Etat | Version |
   |-----------|------|---------|
   | Git       | OK   | 2.43.0  |
   | Bun       | ABSENT | -     |
   | mpg123    | OK   | 1.32.3  |
   ```
3. Si `--install` et prerequis manquants :
   - Demander confirmation avant chaque installation (sudo requis pour apt)
   - Installer dans l'ordre : curl, git, bun, mpg123, notify-send
   - Pour Bun : `curl -fsSL https://bun.sh/install | bash` puis `source ~/.bashrc`
   - Reverifier apres installation
4. Afficher le resultat final
