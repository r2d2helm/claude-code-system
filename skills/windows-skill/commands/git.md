# Gestion Git

Administration et diagnostic Git.

## Mode d'Utilisation
```
/git                        → État Git et repos récents
/git status                 → État du repo courant
/git config                 → Configuration Git
/git remotes                → Gestion des remotes
/git branches               → Gestion des branches
/git stash                  → Gestion des stash
/git history                → Historique des commits
/git cleanup                → Nettoyage du repo
/git credentials            → Gestion des credentials
/git troubleshoot           → Diagnostic des problèmes
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

## Mode `branches`

```
🌿 GESTION DES BRANCHES
═══════════════════════════════════════════════════════════════

REPO: C:\Projects\myapp

BRANCHES LOCALES:
┌──────────────────────────────────────────────────────────────────┐
│ * main                   a1b2c3d [origin/main: ahead 2]         │
│   feature/auth           d4e5f6g [origin/feature/auth]          │
│   feature/dashboard      h7i8j9k [origin/feature/dashboard: behind 3]│
│   bugfix/login           l0m1n2o (local only)                   │
│   old-feature            p3q4r5s (merged, peut être supprimée)  │
└──────────────────────────────────────────────────────────────────┘

BRANCHES REMOTE (origin):
├─ origin/main
├─ origin/develop
├─ origin/feature/auth
├─ origin/feature/dashboard
├─ origin/feature/api-v2
└─ origin/release/v2.0

BRANCHES RÉCENTES (par date):
1. main (il y a 2 heures)
2. feature/auth (il y a 1 jour)
3. bugfix/login (il y a 2 jours)
4. feature/dashboard (il y a 1 semaine)

BRANCHES MERGÉES (peuvent être supprimées):
├─ old-feature → merged dans main
└─ hotfix/security → merged dans main

STATISTIQUES:
├─ Branches locales: 5
├─ Branches remote: 6
├─ À synchroniser: 2
└─ Peuvent être supprimées: 2

ACTIONS:
1. Créer une nouvelle branche
2. Changer de branche (checkout)
3. Supprimer une branche locale
4. Supprimer une branche remote
5. Merger une branche
6. Rebase sur main
7. Nettoyer les branches mergées

Choix: _
```

---

## Mode `history`

```
📜 HISTORIQUE DES COMMITS
═══════════════════════════════════════════════════════════════

REPO: C:\Projects\myapp
BRANCHE: main

DERNIERS COMMITS:
┌─────────────────────────────────────────────────────────────────┐
│ ● a1b2c3d (HEAD -> main) feat: add user authentication         │
│ │ Author: Jean Dupont <jean@example.com>                        │
│ │ Date: 2026-02-03 08:30 (il y a 2 heures)                     │
│ │ Files: 5 changed, +120 -15                                    │
│ │                                                               │
│ ● d4e5f6g fix: resolve login redirect issue                    │
│ │ Author: Jean Dupont <jean@example.com>                        │
│ │ Date: 2026-02-03 07:15                                        │
│ │ Files: 2 changed, +8 -3                                       │
│ │                                                               │
│ ● g7h8i9j (origin/main) chore: update dependencies             │
│ │ Author: Marie Martin <marie@example.com>                      │
│ │ Date: 2026-02-02 16:45                                        │
│ │ Files: 2 changed, +450 -380                                   │
│ │                                                               │
│ ● j0k1l2m feat: add dashboard component                        │
│ │ Author: Jean Dupont <jean@example.com>                        │
│ │ Date: 2026-02-02 14:20                                        │
│ │                                                               │
│ ●─┬─ m3n4o5p Merge branch 'feature/api'                        │
│ │ │ Author: Jean Dupont                                         │
│ │ │ Date: 2026-02-01 11:00                                      │
│ │ │                                                             │
│ │ ● p6q7r8s feat: implement REST API                           │
│ │ │                                                             │
│ ● │ s9t0u1v docs: update README                                │
│ ├─┘                                                             │
│ ●   v2w3x4y Initial commit                                     │
└─────────────────────────────────────────────────────────────────┘

STATISTIQUES (30 derniers jours):
├─ Total commits: 45
├─ Contributeurs: 3
├─ Lignes ajoutées: +2,340
├─ Lignes supprimées: -890
└─ Fichiers modifiés: 78

TOP CONTRIBUTEURS:
1. Jean Dupont: 28 commits (62%)
2. Marie Martin: 12 commits (27%)
3. Pierre Durand: 5 commits (11%)

FILTRES:
1. Par auteur: /git history --author="Jean"
2. Par date: /git history --since="2026-02-01"
3. Par fichier: /git history -- src/api/
4. Chercher: /git history --grep="fix"
```

---

## Mode `cleanup`

```
🧹 NETTOYAGE GIT
═══════════════════════════════════════════════════════════════

REPO: C:\Projects\myapp

ANALYSE EN COURS...

ÉLÉMENTS NETTOYABLES:
┌────────────────────────────────────────┬──────────┬──────────┐
│ Type                                   │ Quantité │ Taille   │
├────────────────────────────────────────┼──────────┼──────────┤
│ Branches locales mergées               │ 3        │ -        │
│ Branches remote supprimées (stale)     │ 2        │ -        │
│ Objets non référencés (loose)          │ 156      │ 12 MB    │
│ Fichiers dans .git/objects (pack)      │ -        │ 145 MB   │
│ Stash anciens (> 30 jours)             │ 4        │ -        │
│ Reflog entries (> 90 jours)            │ 234      │ -        │
└────────────────────────────────────────┴──────────┴──────────┘

TAILLE DU REPO:
├─ Dossier .git: 158 MB
├─ Working directory: 45 MB
├─ Total: 203 MB
└─ Après optimisation estimée: ~120 MB (-40%)

OPTIONS DE NETTOYAGE:

1. 🟢 Nettoyage léger (sûr)
   - git fetch --prune (supprimer refs remote obsolètes)
   - git branch -d (branches mergées)
   Récupération: ~0 MB (cleanup refs seulement)

2. 🟡 Nettoyage modéré
   - Tout ci-dessus
   - git gc (garbage collection)
   - git repack
   Récupération: ~30 MB

3. 🟠 Nettoyage agressif
   - Tout ci-dessus
   - git gc --aggressive --prune=now
   - Supprimer les stash anciens
   - Compacter le reflog
   Récupération: ~40 MB
   ⚠️ Plus long (plusieurs minutes)

4. 🔴 Nettoyage des gros fichiers
   - Identifier les gros fichiers dans l'historique
   - Utiliser git-filter-repo pour les supprimer
   ⚠️ Réécrit l'historique! Nécessite force push

Choix: _
```

---

## Mode `credentials`

```
🔑 GESTION DES CREDENTIALS GIT
═══════════════════════════════════════════════════════════════

CREDENTIAL HELPER ACTUEL:
├─ Type: Git Credential Manager (manager-core)
├─ Version: 2.4.1
└─ Store: Windows Credential Manager

CREDENTIALS ENREGISTRÉS:
┌─────────────────────────────────────────────────────────────────┐
│ 🔐 github.com                                                   │
├─────────────────────────────────────────────────────────────────┤
│ Protocol : https                                                │
│ Username : jean-dupont                                          │
│ Type     : Personal Access Token                                │
│ Scopes   : repo, workflow, read:org                             │
│ Créé     : 2025-06-15                                           │
│ Expire   : 2026-06-15                                           │
├─────────────────────────────────────────────────────────────────┤
│ 🔐 gitlab.com                                                   │
├─────────────────────────────────────────────────────────────────┤
│ Protocol : https                                                │
│ Username : jean.dupont                                          │
│ Type     : Personal Access Token                                │
│ Créé     : 2025-08-20                                           │
├─────────────────────────────────────────────────────────────────┤
│ 🔐 dev.azure.com                                                │
├─────────────────────────────────────────────────────────────────┤
│ Protocol : https                                                │
│ Username : jean@company.com                                     │
│ Type     : Azure AD Token                                       │
│ Org      : company-org                                          │
└─────────────────────────────────────────────────────────────────┘

CLÉS SSH POUR GIT:
├─ github.com: ~/.ssh/github_key (ED25519)
├─ gitlab.com: ~/.ssh/gitlab_key (ED25519)
└─ bitbucket.org: ~/.ssh/id_ed25519

ACTIONS:
1. Ajouter/Modifier un credential
2. Supprimer un credential
3. Tester l'authentification
4. Configurer SSH au lieu de HTTPS
5. Renouveler un token expirant
6. Voir le Credential Manager Windows

Choix: _
```

---

## Mode `troubleshoot`

```
🔧 DIAGNOSTIC GIT
═══════════════════════════════════════════════════════════════

VÉRIFICATIONS:

1. INSTALLATION
   ├─ Git installé: ✅ 2.43.0
   ├─ Dans le PATH: ✅ Oui
   └─ Git Bash: ✅ Disponible

2. CONFIGURATION
   ├─ user.name: ✅ Configuré
   ├─ user.email: ✅ Configuré
   └─ Credential helper: ✅ manager-core

3. CONNECTIVITÉ
   ├─ github.com: ✅ SSH OK
   ├─ gitlab.com: ✅ HTTPS OK
   └─ Proxy: Non configuré

4. REPO COURANT
   ├─ Est un repo git: ✅ Oui
   ├─ Remote configuré: ✅ origin
   └─ État: ✅ Pas de conflits

═══════════════════════════════════════════════════════════════
RÉSULTAT: ✅ Tout est OK

PROBLÈMES COURANTS:

❓ "Permission denied (publickey)"
   → Vérifier la clé SSH: ssh -T git@github.com
   → Ajouter la clé à l'agent: ssh-add ~/.ssh/github_key

❓ "fatal: Authentication failed"
   → Token expiré: renouveler sur GitHub/GitLab
   → Supprimer credential: git credential reject

❓ "fatal: refusing to merge unrelated histories"
   → git pull origin main --allow-unrelated-histories

❓ "error: failed to push some refs"
   → git pull --rebase origin main
   → Puis git push

❓ Conflits de merge
   → git mergetool (utiliser VS Code)
   → Après résolution: git add . && git commit

❓ "filename too long"
   → git config --global core.longpaths true

❓ Problèmes de CRLF/LF
   → git config --global core.autocrlf true (Windows)
```

---

## Commandes de Référence

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

# Branches
git branch -a
git checkout -b nouvelle-branche
git branch -d branche-mergee
git push origin --delete branche-remote

# Sync
git fetch --all --prune
git pull --rebase
git push origin main

# Stash
git stash
git stash list
git stash pop
git stash drop

# Historique
git log --oneline --graph
git log --author="Nom" --since="2026-01-01"
git blame fichier.txt

# Nettoyage
git gc
git prune
git remote prune origin

# Reset
git reset --soft HEAD~1    # Annule commit, garde changes staged
git reset --mixed HEAD~1   # Annule commit, garde changes unstaged
git reset --hard HEAD~1    # Annule tout (⚠️ destructif)

# Credentials
git credential reject
git config --global credential.helper manager-core
```
