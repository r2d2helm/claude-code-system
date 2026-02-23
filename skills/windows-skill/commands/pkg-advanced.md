# Gestion des Packages - Avancé

Voir aussi: [[pkg]]

Liste, export/import, nettoyage et opérations batch.

---

## Mode `list`

```
PACKAGES INSTALLÉS
═══════════════════════════════════════════════════════════════

WINGET (45 packages):
┌────────────────────────────────────────┬─────────────┬────────────┐
│ Nom                                    │ Version     │ Source     │
├────────────────────────────────────────┼─────────────┼────────────┤
│ 7zip.7zip                              │ 23.01       │ winget     │
│ Discord.Discord                        │ 1.0.9035    │ winget     │
│ Docker.DockerDesktop                   │ 4.27.1      │ winget     │
│ Git.Git                                │ 2.44.0      │ winget     │
│ Google.Chrome                          │ 122.0.6273  │ winget     │
│ Microsoft.PowerShell                   │ 7.4.1       │ winget     │
│ Microsoft.VisualStudioCode             │ 1.86.2      │ winget     │
│ Microsoft.WindowsTerminal              │ 1.19.10302  │ winget     │
│ Mozilla.Firefox                        │ 123.0.1     │ winget     │
│ Notepad++.Notepad++                    │ 8.6.4       │ winget     │
│ OpenJS.NodeJS                          │ 20.11.1     │ winget     │
│ Python.Python.3.12                     │ 3.12.2      │ winget     │
│ ... (33 autres)                        │             │            │
└────────────────────────────────────────┴─────────────┴────────────┘

CHOCOLATEY (23 packages):
┌────────────────────────────────────────┬─────────────┬────────────┐
│ Nom                                    │ Version     │ Source     │
├────────────────────────────────────────┼─────────────┼────────────┤
│ chocolatey                             │ 2.2.2       │ choco      │
│ chocolatey-core.extension              │ 1.4.0       │ choco      │
│ curl                                   │ 8.6.0       │ choco      │
│ fzf                                    │ 0.46.1      │ choco      │
│ jq                                     │ 1.7.1       │ choco      │
│ neovim                                 │ 0.9.5       │ choco      │
│ ripgrep                                │ 14.1.0      │ choco      │
│ wget                                   │ 1.21.4      │ choco      │
│ ... (15 autres)                        │             │            │
└────────────────────────────────────────┴─────────────┴────────────┘

RÉSUMÉ:
├─ Total packages: 68
├─ Winget: 45
├─ Chocolatey: 23
└─ Dernière mise à jour: 2026-02-03 10:30
```

---

## Mode `export`

```
EXPORTER LA LISTE DES PACKAGES
═══════════════════════════════════════════════════════════════

FORMAT D'EXPORT:

1. WINGET JSON (recommandé)
   → winget export -o packages.json
   → Restaurable avec: winget import -i packages.json
   → Inclut les sources et versions

2. CHOCOLATEY PACKAGES.CONFIG
   → Format XML standard Chocolatey
   → Restaurable avec: choco install packages.config

3. SCRIPT POWERSHELL
   → Script qui installe tous les packages
   → Fonctionne sur nouvelle machine

4. LISTE TEXTE
   → Simple liste de noms de packages
   → Pour référence/documentation

5. TOUT EXPORTER
   → Exporte dans tous les formats
   → Destination: C:\Backups\Packages\

Choix: 5

═══════════════════════════════════════════════════════════════
EXPORT EN COURS...

✅ Fichiers créés:
├─ C:\Backups\Packages\winget-packages.json (45 packages)
├─ C:\Backups\Packages\choco-packages.config (23 packages)
├─ C:\Backups\Packages\install-all.ps1 (script)
└─ C:\Backups\Packages\packages-list.txt (liste)

Pour restaurer sur une nouvelle machine:
1. Winget: winget import -i winget-packages.json
2. Choco: choco install packages.config -y
3. Ou: .\install-all.ps1
```

---

## Mode `cleanup`

```
NETTOYAGE DU CACHE
═══════════════════════════════════════════════════════════════

ANALYSE DU CACHE:

WINGET:
├─ Cache installateurs: 234 MB
├─ Cache sources: 45 MB
├─ Logs: 12 MB
└─ Total: 291 MB

CHOCOLATEY:
├─ Packages téléchargés: 512 MB
├─ Cache nupkg: 156 MB
├─ Logs: 8 MB
└─ Total: 676 MB

ESPACE TOTAL RÉCUPÉRABLE: 967 MB

OPTIONS:
├─ [1] Nettoyer le cache Winget (291 MB)
├─ [2] Nettoyer le cache Chocolatey (676 MB)
├─ [3] Tout nettoyer (967 MB)
├─ [4] Nettoyage agressif (+ anciens packages)
└─ [5] Annuler

Choix: 3

═══════════════════════════════════════════════════════════════
NETTOYAGE EN COURS...

Nettoyage Winget... ✅ 291 MB libérés
Nettoyage Chocolatey... ✅ 676 MB libérés

✅ Nettoyage terminé!
Espace total récupéré: 967 MB
```

---

## Commandes de Référence (Avancé)

```powershell
# === WINGET ===

# Lister
winget list

# Export/Import
winget export -o packages.json
winget import -i packages.json

# === CHOCOLATEY ===

# Lister
choco list --local-only

# Export
choco export packages.config

# Installer depuis config
choco install packages.config -y

# Nettoyage
choco cache remove

# === SCOOP (Alternative) ===
# Installation: irm get.scoop.sh | iex
scoop search terme
scoop install package
scoop update *
```
