# Commande: /devops-git

Workflows Git pour le homelab.

## Syntaxe

```
/devops-git [action] [options]
```

## Branching

```bash
# Creer une feature branch
git checkout -b feature/{name}

# Creer un fix
git checkout -b fix/{name}

# Creer une release
git checkout -b release/v{version}
```

## Commits Conventionnels

Format : `type(scope): message`

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalite |
| `fix` | Correction de bug |
| `docs` | Documentation |
| `refactor` | Refactoring sans changement fonctionnel |
| `test` | Ajout/modification de tests |
| `chore` | Maintenance, dependencies |
| `ci` | CI/CD |

```bash
git commit -m "feat(auth): add JWT refresh token support"
git commit -m "fix(backup): correct pg_dump path on VM 104"
git commit -m "docs(skill): update devops-skill commands"
```

## Tags & Releases

```bash
# Creer un tag
git tag -a v{version} -m "Release v{version}: description"

# Pousser le tag
git push origin v{version}

# Lister les tags
git tag -l --sort=-version:refname | head -10
```

## Operations Courantes

```bash
# Status
git status && git log --oneline -5

# Diff avant commit
git diff --stat

# Stash (sauvegarder temporairement)
git stash push -m "description"
git stash list
git stash pop
```
