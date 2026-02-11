# /pai-packs — Lister packs disponibles/installes

Lister les packs PAI disponibles dans le depot et leur etat d'installation.

## Syntaxe

```
/pai-packs [--available | --installed]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `--available` | Lister seulement les packs disponibles | Non |
| `--installed` | Lister seulement les packs installes | Non |

## Procedure

1. Lister les packs disponibles dans `/home/r2d2helm/Personal_AI_Infrastructure/Packs/`
2. Pour chaque pack, lire la version et description depuis README.md (frontmatter YAML)
3. Verifier si installe : chercher les artefacts dans `~/.claude/`
   - `hooks/` pour pai-hook-system
   - `skills/PAI/` pour pai-core-install
   - `VoiceServer/` pour pai-voice-system
   - `observability/` pour pai-observability-server
   - `skills/<NomSkill>/` pour les skill packs
4. Afficher tableau :
   ```
   | Pack | Version | Categorie | Installe |
   |------|---------|-----------|----------|
   | pai-hook-system | 2.3.0 | Foundation | Non |
   | pai-core-install | 2.3.0 | Core | Non |
   ```
