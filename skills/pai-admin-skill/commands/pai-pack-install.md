# /pai-pack-install — Installer un pack individuel

Installer un pack PAI specifique depuis le depot.

## Syntaxe

```
/pai-pack-install <nom-pack>
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `nom-pack` | Nom du pack (ex: pai-voice-system) | Obligatoire |

## Procedure

1. Verifier que le pack existe dans `/home/r2d2helm/Personal_AI_Infrastructure/Packs/<nom-pack>/`
2. Lire le README.md du pack
3. Verifier les dependances du pack (frontmatter YAML: dependencies)
4. Si dependances manquantes, proposer de les installer d'abord
5. Suivre le INSTALL.md du pack etape par etape
6. Copier les fichiers depuis src/ vers les emplacements cibles
7. Mettre a jour settings.json si necessaire (hooks, permissions)
8. Executer les verifications VERIFY.md
9. Confirmer l'installation
