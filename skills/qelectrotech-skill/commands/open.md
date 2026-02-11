# Ouvrir un projet dans QElectroTech

Ouvre un fichier `.qet` dans QElectroTech GUI.

## Actions

1. **Verifier** que le fichier existe et est un XML valide
2. **Afficher un resume** rapide (nombre de folios, elements, taille)
3. **Lancer** QElectroTech avec le fichier en argument

## Commande d'ouverture

```powershell
Start-Process 'C:\Program Files\QElectroTech\qelectrotech-0.100.1+git8595-x86-win64-readytouse\bin\qelectrotech.exe' -ArgumentList '<chemin_fichier>'
```

## Si aucun chemin fourni

Chercher les fichiers .qet recents :
- Bureau de l'utilisateur
- Documents\Archives
- Dernier fichier ouvert

$ARGUMENTS
