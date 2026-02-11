# Sauvegarder un projet QET

Cree une copie de sauvegarde d'un fichier .qet avec horodatage.

## Actions

1. **Verifier** que le fichier source existe
2. **Creer le dossier de backup** si necessaire (`_backups/` a cote du fichier)
3. **Copier** le fichier avec horodatage : `NomProjet_YYYYMMDD_HHmmss.qet`
4. **Nettoyer** les anciennes sauvegardes (garder les 10 dernieres par defaut)
5. **Afficher** la liste des backups existants

## Bonus : Versioning Git

Si le projet est dans un repo git, proposer un commit avec message descriptif.
Les fichiers .qet etant du XML, ils se mergent raisonnablement bien avec git.

## Exemple

```
/qet-backup "C:\Desktop\NELU_ELEC_COMPLET.qet"
/qet-backup projet.qet --keep 20
```

$ARGUMENTS
