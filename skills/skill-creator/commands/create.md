# Create Skill

## Cible : $ARGUMENTS

Guide la creation d'un nouveau skill Claude Code pour le systeme r2d2.

## Processus

1. **Analyser le besoin** : Comprendre les cas d'usage du skill
   - Quelles commandes seront necessaires ?
   - Quel domaine couvre-t-il ?
   - Verifier qu'aucun skill existant ne couvre deja ce domaine
   - Choisir un prefixe de commande unique

2. **Initialiser la structure** : L'utilisateur execute le script d'initialisation **dans son terminal** (pas depuis Claude)
   ```bash
   # Commande a copier-coller dans le terminal par l'utilisateur
   python ~/.claude/skills/skill-creator/scripts/init_skill.py <nom-skill> --path ~/.claude/skills
   ```
   > **Note:** `init_skill.py` cree la structure de dossiers et les fichiers template. Il doit etre lance manuellement par l'utilisateur via son terminal. Claude n'invoque pas ce script directement -- il guide l'utilisateur et edite les fichiers generes ensuite.

3. **Editer le SKILL.md** : Completer les TODO du template
   - Frontmatter : name + description (avec triggers)
   - Body : vue d'ensemble, commandes, conventions du domaine

4. **Creer les commandes** : Au minimum une commande dans `commands/`
   - Format : `{action}.md` avec processus etape par etape
   - Inclure des exemples concrets

5. **Ajouter les ressources** : Si necessaire
   - `wizards/` : parcours interactifs guides
   - `scripts/` : automatisations PowerShell/Python
   - `references/` : documentation detaillee

6. **Valider** : Executer la validation
   ```bash
   python ~/.claude/skills/skill-creator/scripts/quick_validate.py ~/.claude/skills/<nom-skill>
   ```

7. **Integrer** : Publier le contrat et mettre a jour le systeme
   - Meta-router (SKILL.md) : ajouter keywords et routage
   - CLAUDE.md : ajouter au tableau Skills Actifs
   - Vault : creer note concept `C_{Skill-Name}.md`

## Exemples

```
/skill-create monitoring-skill
/skill-create backup-skill
/skill-create network-skill
```

## Walkthrough : creation de "monitoring-skill"

Exemple concret de creation d'un skill de monitoring systeme :

**Etape 1 - Analyser le besoin :**
- Commandes necessaires : `/mon-status`, `/mon-alerts`, `/mon-dashboard`
- Domaine : surveillance systeme (CPU, RAM, disque, services)
- Prefixe : `mon`
- Aucun skill existant ne couvre ce domaine

**Etape 2 - L'utilisateur initialise :**
```bash
python ~/.claude/skills/skill-creator/scripts/init_skill.py monitoring-skill --path ~/.claude/skills
```
Resultat : `~/.claude/skills/monitoring-skill/` avec SKILL.md, commands/, wizards/

**Etape 3 - Editer SKILL.md :**
```yaml
---
name: monitoring-skill
description: "Surveillance systeme Linux. Alertes CPU, RAM, disque, services Docker et systemd. Utiliser pour 'check system', 'alertes serveur', 'dashboard systeme', 'monitoring', 'etat du serveur'."
prefix: /mon-*
---
```

**Etape 4 - Creer les commandes :**
- `commands/status.md` : Etat global systeme (CPU, RAM, disque, uptime)
- `commands/alerts.md` : Verification des seuils et alertes actives
- `commands/dashboard.md` : Vue synthetique avec metriques cles

**Etape 5 - Valider :**
```bash
python ~/.claude/skills/skill-creator/scripts/quick_validate.py ~/.claude/skills/monitoring-skill
```

**Etape 6 - Integrer :**
- Publier contrat pour router-updater et knowledge-indexer
- Mettre a jour CLAUDE.md avec la ligne du skill
- Creer `C_Monitoring-Skill.md` dans le vault
