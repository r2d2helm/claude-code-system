# /pai-bundle-install — Installer via Bundle + packs

Installer PAI en utilisant le Bundle officiel puis les packs individuels. Approche educative.

## Syntaxe

```
/pai-bundle-install
```

## Procedure

1. Verifier prerequis (`/pai-prereqs`)
2. Sauvegarder settings.json existant
3. Executer le Bundle wizard :
   ```bash
   cd /home/r2d2helm/Personal_AI_Infrastructure/Bundles/Official && bun run install.ts
   ```
4. Installer les packs dans l'ordre :
   - pai-hook-system (fondation)
   - pai-core-install (CORE skill)
   - pai-statusline (status line)
   - pai-voice-system (optionnel)
   - pai-observability-server (optionnel)
5. Pour chaque pack, suivre son INSTALL.md et VERIFY.md
6. Fusionner settings.json (preserver mcpServers)
7. Configurer identite R2D2
8. Executer `/pai-verify`
