# Create SOP / Runbook

## Cible : $ARGUMENTS

Crée une documentation opérationnelle (SOP, runbook, playbook, checklist) selon les templates du skill sop-creator.

## Processus

1. **Analyser le besoin** : Identifier le type de documentation demandé
   - Si le type n'est pas clair, consulter le Format Selection Guide dans SKILL.md
   - Demander des précisions si nécessaire (domaine, audience, criticité)

2. **Sélectionner le template** : Charger le template approprié depuis `references/`
   - Runbook -> `references/runbook.md`
   - Standard SOP -> `references/standard-sop.md`
   - How-To Guide -> `references/how-to-guide.md`
   - Onboarding -> `references/onboarding-guide.md`
   - Decision Tree -> `references/decision-tree.md`
   - Checklist -> `references/checklist.md`

3. **Rédiger le contenu** : Appliquer les Writing Rules du SKILL.md
   - Definition of Done en premier
   - Steps actionnables (verbes, pas de descriptions)
   - Spécifique (noms, chiffres, seuils)
   - Pour l'infra r2d2 : utiliser les commandes PowerShell/bash réelles

4. **Vérifier la qualité** : Appliquer le Quality Checklist
   - Lisible par quelqu'un qui ne connaît pas le contexte
   - Chaque étape est une action concrète
   - État "terminé" clairement défini

5. **Optionnel - Stocker dans le vault** : Si pertinent pour le système r2d2
   - Placer dans `Knowledge/References/SOPs/`
   - Ajouter le frontmatter YAML obligatoire
   - Nommer : `SOP_{Domain}_{Title}.md`

## Exemples

```
/sop-create runbook backup proxmox
/sop-create checklist pre-deploy docker
/sop-create how-to setup rdp windows server
/sop-create sop maintenance hebdo vault
```
