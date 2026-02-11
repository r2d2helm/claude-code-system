# Create Skill

## Cible : $ARGUMENTS

Guide la creation d'un nouveau skill Claude Code pour le systeme r2d2.

## Processus

1. **Analyser le besoin** : Comprendre les cas d'usage du skill
   - Quelles commandes seront necessaires ?
   - Quel domaine couvre-t-il ?
   - Verifier qu'aucun skill existant ne couvre deja ce domaine
   - Choisir un prefixe de commande unique

2. **Initialiser la structure** : Executer le script d'initialisation
   ```bash
   python ~/.claude/skills/skill-creator/scripts/init_skill.py <nom-skill> --path ~/.claude/skills
   ```

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
