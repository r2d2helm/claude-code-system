# /pai-restore — Restaurer depuis backup

Restaurer une installation PAI depuis une sauvegarde.

## Syntaxe

```
/pai-restore [fichier-backup]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `fichier-backup` | Chemin du fichier .tar.gz | Interactif (lister et choisir) |

## Procedure

1. Si pas de fichier specifie, lister les backups disponibles :
   ```bash
   ls -lt ~/backups/pai/pai-backup-*.tar.gz
   ```
2. Demander quel backup restaurer via AskUserQuestion
3. **Sauvegarder l'etat actuel** avant restauration :
   ```bash
   cp -r ~/.claude ~/.claude-pre-restore-$(date +%Y%m%d)
   ```
4. Extraire le backup :
   ```bash
   tar xzf <fichier-backup> -C ~/
   ```
5. Verifier l'extraction : `/pai-verify`
6. Rappeler de redemarrer Claude Code
