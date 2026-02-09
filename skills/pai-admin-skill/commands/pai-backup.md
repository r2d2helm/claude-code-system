# /pai-backup — Sauvegarder l'installation PAI

Creer une sauvegarde complete de l'installation PAI.

## Syntaxe

```
/pai-backup [--dir <repertoire>]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `--dir` | Repertoire de destination | `~/backups/pai/` |

## Procedure

1. Creer le repertoire de backup si necessaire :
   ```bash
   mkdir -p ~/backups/pai/
   ```
2. Generer le nom : `pai-backup-YYYY-MM-DD_HH-MM.tar.gz`
3. Sauvegarder ~/.claude/ (excluant node_modules et caches) :
   ```bash
   tar czf ~/backups/pai/pai-backup-$(date +%Y-%m-%d_%H-%M).tar.gz \
     --exclude='node_modules' \
     --exclude='.cache' \
     --exclude='observability/apps/*/dist' \
     -C ~ .claude/
   ```
4. Verifier l'archive :
   ```bash
   tar tzf ~/backups/pai/pai-backup-*.tar.gz | head -20
   ```
5. Afficher taille et emplacement
6. Lister les backups existants
7. Proposer nettoyage si plus de 10 backups
