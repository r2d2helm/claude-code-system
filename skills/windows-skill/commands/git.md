# Gestion Git

Voir aussi: [[git-advanced]]

Administration et diagnostic Git.

## Mode d'Utilisation
```
/git                        → État Git et repos récents
/git status                 → État du repo courant
/git config                 → Configuration Git
/git remotes                → Gestion des remotes
/git branches               → Gestion des branches (voir git-advanced)
/git stash                  → Gestion des stash (voir git-advanced)
/git history                → Historique des commits (voir git-advanced)
/git cleanup                → Nettoyage du repo (voir git-advanced)
/git credentials            → Gestion des credentials (voir git-advanced)
/git troubleshoot           → Diagnostic des problèmes (voir git-advanced)
```

Arguments: $ARGUMENTS

---

## État Git (défaut)

```
📦 GIT - ÉTAT GÉNÉRAL
═══════════════════════════════════════════════════════════════

VERSION ET CONFIGURATION:
├─ Git Version: 2.43.0.windows.1
├─ Utilisateur: Jean Dupont <jean@example.com>
├─ Éditeur: code --wait
├─ Merge tool: vscode
└─ Credential helper: manager-core

REPOS RÉCEMMENT UTILISÉS:
┌─────────────────────────────────────────────────────────────────┐
│ 📁 C:\Projects\myapp                                            │
│ ├─ Branche: main (↑2 ↓0 avec origin/main)                      │
│ ├─ Modifié: il y a 30 minutes                                   │
│ ├─ Status: 3 fichiers modifiés, 1 non suivi                     │
│ └─ Remote: git@github.com:jean/myapp.git                        │
├─────────────────────────────────────────────────────────────────┤
│ 📁 C:\Projects\api-backend                                      │
│ ├─ Branche: feature/auth (↑0 ↓5 avec origin)                   │
│ ├─ Modifié: il y a 2 heures                                     │
│ ├─ Status: ✅ Clean                                             │
│ └─ Remote: git@gitlab.com:company/api-backend.git               │
├─────────────────────────────────────────────────────────────────┤
│ 📁 C:\Projects\dotfiles                                         │
│ ├─ Branche: master                                              │
│ ├─ Modifié: il y a 3 jours                                      │
│ ├─ Status: ✅ Clean                                             │
│ └─ Remote: git@github.com:jean/dotfiles.git                     │
└─────────────────────────────────────────────────────────────────┘

STATISTIQUES GLOBALES:
├─ Repos Git trouvés: 12
├─ Total commits (30 jours): 156
├─ Lignes ajoutées: +4,523
└─ Lignes supprimées: -1,287

⚠️ ALERTES:
├─ myapp: 2 commits en avance sur origin (push nécessaire)
└─ api-backend: 5 commits en retard (pull recommandé)
```

---

## Mode `status`

```
📊 GIT STATUS: C:\Projects\myapp
═══════════════════════════════════════════════════════════════

BRANCHE ACTUELLE:
├─ Nom: main
├─ Tracking: origin/main
├─ Ahead: 2 commits (à push)
├─ Behind: 0 commits
└─ Dernier commit: a1b2c3d "feat: add user authentication" (il y a 2h)

CHANGEMENTS:
┌─────────────────────────────────────────────────────────────┐
│ 📝 STAGED (prêts à commit):                                 │
│    (aucun)                                                  │
├─────────────────────────────────────────────────────────────┤
│ ✏️ MODIFIED (non staged):                                   │
│    M  src/components/Login.tsx                              │
│    M  src/api/auth.ts                                       │
│    M  package.json                                          │
├─────────────────────────────────────────────────────────────┤
│ ❓ UNTRACKED (non suivis):                                  │
│    ?  src/components/NewFeature.tsx                         │
│    ?  tests/auth.test.ts                                    │
├─────────────────────────────────────────────────────────────┤
│ 🗑️ DELETED:                                                 │
│    (aucun)                                                  │
└─────────────────────────────────────────────────────────────┘

DIFF RÉSUMÉ:
├─ Fichiers modifiés: 3
├─ Insertions: +45 lignes
├─ Suppressions: -12 lignes
└─ Fichiers non suivis: 2

STASH:
├─ stash@{0}: WIP on main: feature login (il y a 1 jour)
└─ stash@{1}: temp changes (il y a 3 jours)

ACTIONS SUGGÉRÉES:
1. Voir les différences: git diff
2. Stager les fichiers: git add <files>
3. Commit: git commit -m "message"
4. Push: git push origin main
5. Appliquer un stash: git stash pop

Choix: _
```

---

## Mode `config`

```
⚙️ CONFIGURATION GIT
═══════════════════════════════════════════════════════════════

CONFIGURATION GLOBALE (~/.gitconfig):
┌─────────────────────────────────────────────────────────────┐
│ [user]                                                      │
│     name = Jean Dupont                                      │
│     email = jean@example.com                                │
│     signingkey = A1B2C3D4E5F6G7H8                           │
│                                                             │
│ [core]                                                      │
│     editor = code --wait                                    │
│     autocrlf = true                                         │
│     longpaths = true                                        │
│     excludesfile = ~/.gitignore_global                      │
│                                                             │
│ [init]                                                      │
│     defaultBranch = main                                    │
│                                                             │
│ [pull]                                                      │
│     rebase = true                                           │
│                                                             │
│ [push]                                                      │
│     autoSetupRemote = true                                  │
│     default = current                                       │
│                                                             │
│ [merge]                                                     │
│     tool = vscode                                           │
│     conflictstyle = diff3                                   │
│                                                             │
│ [diff]                                                      │
│     tool = vscode                                           │
│                                                             │
│ [alias]                                                     │
│     st = status                                             │
│     co = checkout                                           │
│     br = branch                                             │
│     ci = commit                                             │
│     lg = log --oneline --graph --decorate                   │
│     undo = reset HEAD~1 --soft                              │
│     amend = commit --amend --no-edit                        │
│                                                             │
│ [credential]                                                │
│     helper = manager-core                                   │
│                                                             │
│ [commit]                                                    │
│     gpgsign = true                                          │
│                                                             │
│ [gpg]                                                       │
│     program = gpg                                           │
└─────────────────────────────────────────────────────────────┘

CONFIGURATION LOCALE (repo courant):
├─ user.email: jean@company.com (override pour ce projet)
└─ (autres paramètres hérités de global)

ACTIONS:
1. Modifier le nom/email global
2. Ajouter un alias
3. Configurer le credential helper
4. Configurer GPG signing
5. Éditer .gitconfig directement
6. Voir la configuration effective (merged)

Choix: _
```

---

## Commandes de Référence (Core)

```powershell
# Configuration
git config --global user.name "Nom"
git config --global user.email "email@example.com"
git config --list --show-origin

# Status et diff
git status
git diff
git diff --staged

# Commits
git add .
git commit -m "message"
git commit --amend

# Sync
git fetch --all --prune
git pull --rebase
git push origin main
```
