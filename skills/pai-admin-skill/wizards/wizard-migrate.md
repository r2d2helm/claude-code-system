# Wizard : Migration vers PAI

Assistant interactif pour migrer une configuration Claude Code existante vers PAI v2.5.

## Etape 1 : Analyse de l'existant

1. Verifier ~/.claude/ existant :
   ```bash
   ls -la ~/.claude/
   ```
2. Identifier les composants :
   - settings.json (configuration)
   - skills/ (skills existants)
   - mcpServers (serveurs MCP)
   - hooks/ (hooks existants)
   - Fichiers custom
3. Afficher un inventaire a l'utilisateur

## Etape 2 : Sauvegarde complete

1. Creer backup complet :
   ```bash
   mkdir -p ~/backups/pai/
   tar czf ~/backups/pai/pre-migration-$(date +%Y%m%d-%H%M).tar.gz -C ~ .claude/
   ```
2. Confirmer le backup :
   ```bash
   ls -la ~/backups/pai/pre-migration-*.tar.gz
   ```

## Etape 3 : Identification des elements a preserver

Demander via AskUserQuestion :
- Preserver les skills existants ? (Oui/Non)
- Preserver les serveurs MCP ? (Oui — toujours recommande)
- Preserver les hooks custom ? (Oui/Non)

Lister les elements detectes et demander confirmation pour chacun.

## Etape 4 : Installation PAI avec preservation

1. Copier la release v2.5 :
   ```bash
   cp -r /home/r2d2helm/Personal_AI_Infrastructure/Releases/v2.5/.claude/* ~/.claude/
   ```
2. **Fusionner settings.json** (critique) :
   - Restaurer mcpServers depuis le backup
   - Restaurer les sections custom
   - Appliquer la configuration PAI
3. Restaurer les skills custom si demande :
   ```bash
   cp -r ~/backups/pai/.claude/skills/custom_skill ~/.claude/skills/
   ```

## Etape 5 : Verification et test

1. Executer `/pai-verify`
2. Verifier que les elements preserves sont intacts :
   - `cat ~/.claude/settings.json | jq '.mcpServers'`
   - `ls ~/.claude/skills/`
3. Afficher rapport de migration :
   ```
   | Element | Etat |
   |---------|------|
   | settings.json | Fusionne (mcpServers preserves) |
   | Skills PAI | Installes (19 SYSTEM/ docs) |
   | Skills custom | 2 preserves |
   | Hooks PAI | 15 installes |
   | MCP Servers | 3 preserves |
   ```
4. Rappeler de redemarrer Claude Code
