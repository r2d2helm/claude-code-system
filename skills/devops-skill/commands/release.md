# Commande: /devops-release

Preparer et publier une release.

## Syntaxe

```
/devops-release [version] [options]
```

## Processus de Release

```bash
# 1. Creer la branche release
git checkout main && git pull
git checkout -b release/v{version}

# 2. Mettre a jour les versions
# - docker-compose.yml (tags images)
# - package.json (si applicable)
# - CHANGELOG.md

# 3. Tester
# - Deployer en staging (VM 100)
# - Verifier les fonctionnalites
# - Verifier les logs

# 4. Merger dans main
git checkout main
git merge --no-ff release/v{version}
git tag -a v{version} -m "Release v{version}"

# 5. Deployer en production
# /devops-deploy {service} {vm}

# 6. Push tag
git push origin main --tags

# 7. Nettoyer
git branch -d release/v{version}
```

## Versioning (SemVer)

| Increment | Quand | Exemple |
|-----------|-------|---------|
| MAJOR | Breaking changes | 1.0.0 → 2.0.0 |
| MINOR | Nouvelles fonctionnalites | 1.0.0 → 1.1.0 |
| PATCH | Bug fixes | 1.0.0 → 1.0.1 |
