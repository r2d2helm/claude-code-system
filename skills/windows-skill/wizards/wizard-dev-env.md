# Wizard: Dev Environment Setup

Configuration environnement développeur complet Windows 11.

## Déclenchement

```
/win-wizard dev
```

## Étapes du Wizard (6)

### Étape 1: Profil Développeur

```
╔══════════════════════════════════════════════════════════════╗
║           💻 WIZARD DEV ENVIRONMENT                          ║
║                Étape 1/6 : Profil                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Quel type de développement ?                                ║
║                                                              ║
║  [1] Web Frontend (HTML/CSS/JS/React/Vue)                    ║
║  [2] Web Backend (Node.js/Python/Go)                         ║
║  [3] Full Stack (Frontend + Backend)                         ║
║  [4] Mobile (React Native/Flutter)                           ║
║  [5] DevOps/SRE (Docker/K8s/Terraform)                       ║
║  [6] Data Science (Python/Jupyter)                           ║
║  [7] .NET/C# Development                                     ║
║  [8] Personnalisé                                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 2: Outils de Base

```
╔══════════════════════════════════════════════════════════════╗
║           💻 WIZARD DEV ENVIRONMENT                          ║
║               Étape 2/6 : Outils Base                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🧰 OUTILS ESSENTIELS:                                       ║
║                                                              ║
║  [x] Git                    - Contrôle version               ║
║  [x] Windows Terminal       - Terminal moderne               ║
║  [x] PowerShell 7           - Shell avancé                   ║
║  [x] VS Code                - Éditeur code                   ║
║  [ ] Visual Studio 2022     - IDE complet                    ║
║  [ ] JetBrains Toolbox      - IDEs JetBrains                 ║
║  [x] Oh My Posh             - Prompt personnalisé            ║
║                                                              ║
║  [1] Installer sélection  [2] Tout  [3] Suivant              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Outils de base
winget install Git.Git --silent
winget install Microsoft.WindowsTerminal --silent
winget install Microsoft.PowerShell --silent
winget install Microsoft.VisualStudioCode --silent
winget install JanDeDobbeleer.OhMyPosh --silent

# Configurer Git
git config --global user.name "Votre Nom"
git config --global user.email "email@example.com"
git config --global init.defaultBranch main
git config --global core.autocrlf true
```

### Étape 3: Langages et Runtimes

```
╔══════════════════════════════════════════════════════════════╗
║           💻 WIZARD DEV ENVIRONMENT                          ║
║               Étape 3/6 : Langages                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📦 LANGAGES ET RUNTIMES:                                    ║
║                                                              ║
║  [x] Node.js LTS (22.x)     - JavaScript runtime             ║
║  [x] Python 3.12            - Python + pip                   ║
║  [ ] Go 1.22                - Golang                         ║
║  [ ] Rust                   - Rust + Cargo                   ║
║  [ ] Java 21 (Temurin)      - OpenJDK                        ║
║  [ ] .NET 8 SDK             - C#/F#                          ║
║  [ ] Ruby 3.3               - Ruby + Gems                    ║
║  [ ] PHP 8.3                - PHP + Composer                 ║
║                                                              ║
║  Gestionnaires de versions:                                  ║
║  [x] nvm-windows            - Node versions                  ║
║  [x] pyenv-win              - Python versions                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Node.js + nvm
winget install CoreyButler.NVMforWindows --silent
nvm install lts
nvm use lts

# Python + pyenv
winget install Python.Python.3.12 --silent
pip install --upgrade pip virtualenv pipenv

# Go
winget install GoLang.Go --silent

# Rust
winget install Rustlang.Rustup --silent

# .NET
winget install Microsoft.DotNet.SDK.8 --silent
```

### Étape 4: Conteneurs et Virtualisation

```
╔══════════════════════════════════════════════════════════════╗
║           💻 WIZARD DEV ENVIRONMENT                          ║
║              Étape 4/6 : Conteneurs                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🐳 CONTENEURS ET VIRTUALISATION:                            ║
║                                                              ║
║  [x] WSL 2 + Ubuntu 24.04   - Linux natif                    ║
║  [x] Docker Desktop         - Conteneurs                     ║
║  [ ] Podman Desktop         - Alternative Docker             ║
║  [ ] Rancher Desktop        - K8s local                      ║
║  [ ] Hyper-V                - VMs Windows                    ║
║                                                              ║
║  ⚠️ Docker Desktop requiert WSL 2                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Activer WSL
wsl --install -d Ubuntu-24.04

# Docker Desktop
winget install Docker.DockerDesktop --silent

# Configurer Docker avec WSL 2 backend
# (automatique avec Docker Desktop moderne)
```

### Étape 5: Extensions VS Code

```
╔══════════════════════════════════════════════════════════════╗
║           💻 WIZARD DEV ENVIRONMENT                          ║
║              Étape 5/6 : Extensions                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔌 EXTENSIONS VS CODE:                                      ║
║                                                              ║
║  Essentielles:                                               ║
║  [x] GitLens                 [x] Prettier                    ║
║  [x] ESLint                  [x] Remote - WSL                ║
║  [x] Docker                  [x] GitHub Copilot              ║
║                                                              ║
║  Langages (selon profil):                                    ║
║  [x] Python                  [x] JavaScript/TypeScript       ║
║  [ ] Go                      [ ] Rust                        ║
║  [ ] C#                      [ ] Java                        ║
║                                                              ║
║  Thèmes:                                                     ║
║  [x] One Dark Pro            [ ] Dracula                     ║
║  [x] Material Icon Theme                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Extensions VS Code
$Extensions = @(
    "eamodio.gitlens",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-vscode-remote.remote-wsl",
    "ms-azuretools.vscode-docker",
    "github.copilot",
    "ms-python.python",
    "zhuangtongfa.material-theme",
    "pkief.material-icon-theme"
)

foreach ($Ext in $Extensions) {
    code --install-extension $Ext
}
```

### Étape 6: Finalisation

```
╔══════════════════════════════════════════════════════════════╗
║           💻 WIZARD DEV ENVIRONMENT                          ║
║              Étape 6/6 : Finalisation                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✅ ENVIRONNEMENT CONFIGURÉ:                                  ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✓ Git 2.44 + config globale                             │ ║
║  │ ✓ Node.js 22.x (via nvm)                                │ ║
║  │ ✓ Python 3.12 + pip                                     │ ║
║  │ ✓ VS Code + 10 extensions                               │ ║
║  │ ✓ WSL 2 + Ubuntu 24.04                                  │ ║
║  │ ✓ Docker Desktop                                        │ ║
║  │ ✓ Windows Terminal + Oh My Posh                         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📁 Dossiers créés:                                          ║
║  • C:\Dev\Projects                                           ║
║  • C:\Dev\Tools                                              ║
║                                                              ║
║  [1] Ouvrir VS Code  [2] Exporter config  [3] Terminer       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Créer structure dossiers
New-Item -ItemType Directory -Path "C:\Dev\Projects" -Force
New-Item -ItemType Directory -Path "C:\Dev\Tools" -Force

# Ajouter au PATH
$DevPath = "C:\Dev\Tools"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$DevPath", "User")

# Exporter configuration
$Config = @{
    Git = git --version
    Node = node --version
    Python = python --version
    Docker = docker --version
}
$Config | ConvertTo-Json | Out-File "$env:USERPROFILE\dev-config.json"
```
