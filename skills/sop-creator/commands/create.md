# Create SOP / Runbook

## Cible : $ARGUMENTS

Crée une documentation opérationnelle (SOP, runbook, playbook, checklist) selon les templates du skill sop-creator.

## Processus

1. **Analyser le besoin** : Identifier le type de documentation demandé
   - Si le type n'est pas clair, consulter le Format Selection Guide dans SKILL.md
   - Demander des précisions si nécessaire (domaine, audience, criticité)

2. **Sélectionner le template** : Charger le template de reference approprié depuis `references/`

   **Decision logic -- pick the first match:**
   - Is this for an emergency or incident response? -> `references/runbook.md`
   - Is this a multi-phase deployment, migration, or release? -> `references/standard-sop.md` (playbook variant)
   - Is this a debugging/diagnosis workflow with branching? -> `references/decision-tree.md`
   - Is this a one-time setup or configuration task? -> `references/how-to-guide.md`
   - Is this for onboarding a new person to a system? -> `references/onboarding-guide.md`
   - Is this a verification or quality control list? -> `references/checklist.md`
   - Is this any other repeatable process? -> `references/standard-sop.md`

   Template mapping:
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

   **Vault integration example (Obsidian frontmatter):**
   ```yaml
   ---
   title: "SOP - Backup Proxmox VMs"
   date: 2026-02-22
   type: reference
   status: evergreen
   tags:
     - sop/infrastructure
     - infra/proxmox
   related:
     - "[[C_Proxmox-Backup]]"
     - "[[SOP_Proxmox_Restore]]"
   ---
   ```

## Exemples

```
/sop-create runbook backup proxmox
/sop-create checklist pre-deploy docker
/sop-create how-to setup rdp windows server
/sop-create sop maintenance hebdo vault
```
