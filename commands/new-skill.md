# Créer un nouveau skill

## Nom du skill : $ARGUMENTS

Crée un nouveau skill Claude Code en suivant les conventions du système r2d2.

## Processus

### 1. Validation du nom
- Format : hyphen-case (minuscules, chiffres, tirets)
- Max 64 caractères
- Pas de tirets en début/fin ni consécutifs
- Vérifier qu'il n'existe pas déjà dans `~/.claude/skills/`

### 2. Scaffolding
Créer la structure suivante :
```
~/.claude/skills/{nom-du-skill}/
├── SKILL.md              # Instructions principales (requis)
├── commands/              # Commandes du skill
│   └── {commande}.md     # Au moins une commande
└── wizards/               # Wizards interactifs (optionnel)
    └── wizard-setup.md    # Wizard de setup initial
```

### 3. SKILL.md
Le SKILL.md DOIT contenir :
- Un titre H1 avec le nom du skill
- Une description claire de ce que fait le skill
- La liste des commandes disponibles avec leur syntaxe
- Les conventions et patterns spécifiques au domaine
- Les références vers la documentation externe si applicable

### 4. Commandes
Chaque commande dans `commands/` DOIT :
- Avoir un titre H1 descriptif
- Décrire le processus étape par étape
- Utiliser `$ARGUMENTS` pour les paramètres
- Inclure des exemples d'utilisation

### 5. Intégration au Meta-Router
Mettre à jour `~/.claude/skills/SKILL.md` pour ajouter :
- Le nouveau skill dans le tableau des skills actifs
- Les keywords de détection
- Les commandes disponibles

### 6. Mise à jour CLAUDE.md
Mettre à jour `~/.claude/CLAUDE.md` pour ajouter :
- Le skill dans le tableau des Skills Actifs
- Le préfixe de commandes et le nombre de commandes/wizards

### 7. Indexation vault (optionnel)
Si pertinent, créer une note dans le vault :
- Chemin : `Knowledge/Concepts/C_{Nom-Skill}.md`
- Template : Concept
- Tags : `dev/claude-code`, `ai/agents`
- Related : `[[C_Meta-Router]]`

## Validation

### Structure
```powershell
Test-Path "~/.claude/skills/{nom}/SKILL.md"
Test-Path "~/.claude/skills/{nom}/commands/"
```

### Router
- Le meta-router liste le nouveau skill
- Les keywords routent correctement

### Checklist
- [ ] SKILL.md créé avec contenu pertinent
- [ ] Au moins une commande fonctionnelle
- [ ] Meta-Router mis à jour (SKILL.md)
- [ ] CLAUDE.md mis à jour
- [ ] Encodage UTF-8 sans BOM
- [ ] Note vault créée (si applicable)
