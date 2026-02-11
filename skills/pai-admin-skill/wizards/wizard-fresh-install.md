# Wizard : Installation Complete PAI

Assistant interactif pour une installation complete de PAI v2.5 sur Ubuntu Linux depuis zero.

## Etape 1 : Presentation

Expliquer PAI a l'utilisateur :
- PAI = Personal AI Infrastructure
- Framework open-source pour construire un systeme IA personnel
- Memoire, skills, hooks, securite, objectifs
- Le DA (Digital Assistant) s'appellera R2D2

Demander via AskUserQuestion :
- "Pret a installer PAI ?" → Oui / J'ai des questions

## Etape 2 : Verification prerequis

Executer `/pai-prereqs` automatiquement :
- Verifier Git, Bun, curl, mpg123, notify-send
- Si Bun absent :
  ```bash
  curl -fsSL https://bun.sh/install | bash
  source ~/.bashrc
  ```
- Si mpg123/notify-send absent :
  ```bash
  sudo apt install -y mpg123 libnotify-bin
  ```
- Reverifier tous les prerequis

## Etape 3 : Sauvegarde existant

1. Verifier si ~/.claude/settings.json existe
2. Si oui, sauvegarder :
   ```bash
   cp ~/.claude/settings.json ~/.claude/settings.json.pre-pai-$(date +%Y%m%d)
   ```
3. Sauvegarder tout fichier custom dans ~/.claude/ :
   ```bash
   mkdir -p ~/backups/pai/
   tar czf ~/backups/pai/pre-pai-install-$(date +%Y%m%d).tar.gz -C ~ .claude/ 2>/dev/null || true
   ```

## Etape 4 : Choix methode installation

Demander via AskUserQuestion :
- **Full Release v2.5** (Recommande) — Systeme complet pre-configure
- **Bundle + Packs** — Installation educative piece par piece

## Etape 5 : Installation

### Si Release v2.5 (recommande) :
1. Copier la release :
   ```bash
   cp -r /home/r2d2helm/Personal_AI_Infrastructure/Releases/v2.5/.claude/* ~/.claude/
   ```
2. Ne PAS ecraser settings.json s'il existe — le fusionner a l'etape 6

### Si Bundle + Packs :
1. Executer le bundle wizard
2. Installer dans l'ordre :
   - pai-hook-system
   - pai-core-install
   - pai-statusline
3. Demander pour les optionnels :
   - pai-voice-system (voix)
   - pai-observability-server (dashboard)

## Etape 6 : Fusion settings.json

**Etape critique** — preserver la config existante :

1. Lire le settings.json existant (backup)
2. Lire le settings.json PAI (nouveau)
3. Algorithme de fusion :
   - Preserver `mcpServers` de l'existant integralement
   - Preserver toute section custom de l'existant
   - Ajouter/mettre a jour : `paiVersion`, `env`, `contextFiles`, `hooks`, `statusLine`
   - Fusionner `permissions` (ajouter patterns ask PAI)
   - Configurer `daidentity` et `principal` (etape 7)
4. Ecrire le resultat fusionne
5. Valider JSON : `cat ~/.claude/settings.json | jq . > /dev/null`

## Etape 7 : Configuration identite

Demander via AskUserQuestion :

1. **Nom du principal** : "Quel est votre prenom ?"
2. **Fuseau horaire** : Proposer les plus courants
   - Europe/Paris
   - America/New_York
   - America/Los_Angeles
   - Autre (saisie libre)

Mettre a jour settings.json :
```json
{
  "daidentity": {
    "name": "R2D2",
    "fullName": "R2D2 - Personal AI",
    "displayName": "R2D2",
    "startupCatchphrase": "R2D2 here, ready to go."
  },
  "principal": {
    "name": "<reponse>",
    "timezone": "<reponse>"
  }
}
```

## Etape 8 : Verification et finalisation

1. Executer `/pai-verify` complet
2. Afficher tableau resultats
3. Rappeler les prochaines etapes :
   - **Redemarrer Claude Code** pour activer les hooks
   - Tester avec `/pai-status`
   - Optionnel : configurer voix avec `/pai-voice install`
   - Optionnel : configurer observability avec `/pai-observability start`
4. Feliciter l'utilisateur : "PAI v2.5 installe. R2D2 est pret."
