# Gestion des Variables d'Environnement

Administration des variables d'environnement système et utilisateur.

## Mode d'Utilisation
```
/env                        → Liste des variables importantes
/env list                   → Toutes les variables
/env get "NOM"              → Valeur d'une variable
/env set "NOM" "valeur"     → Définir une variable
/env delete "NOM"           → Supprimer une variable
/env path                   → Gérer le PATH
/env backup                 → Sauvegarder les variables
/env restore                → Restaurer une sauvegarde
```

Arguments: $ARGUMENTS

---

## Variables Importantes (défaut)

```
🌍 VARIABLES D'ENVIRONNEMENT
═══════════════════════════════════════════════════════════════

SYSTÈME:
├─ COMPUTERNAME     = DESKTOP-ABC123
├─ OS               = Windows_NT
├─ PROCESSOR_ARCH   = AMD64
├─ NUMBER_OF_PROC   = 8
├─ SystemRoot       = C:\Windows
├─ ProgramFiles     = C:\Program Files
├─ ProgramFiles(x86)= C:\Program Files (x86)
├─ ProgramData      = C:\ProgramData
├─ CommonProgramFiles = C:\Program Files\Common Files
└─ TEMP (système)   = C:\Windows\TEMP

UTILISATEUR:
├─ USERNAME         = Jean
├─ USERPROFILE      = C:\Users\Jean
├─ HOMEPATH         = \Users\Jean
├─ APPDATA          = C:\Users\Jean\AppData\Roaming
├─ LOCALAPPDATA     = C:\Users\Jean\AppData\Local
├─ TEMP             = C:\Users\Jean\AppData\Local\Temp
└─ OneDrive         = C:\Users\Jean\OneDrive

DÉVELOPPEMENT:
├─ JAVA_HOME        = C:\Program Files\Java\jdk-17
├─ PYTHON_HOME      = C:\Python312
├─ NODE_PATH        = C:\Program Files\nodejs
├─ GOPATH           = C:\Users\Jean\go
└─ EDITOR           = code

PATH (résumé):
├─ Entrées système: 12
├─ Entrées utilisateur: 8
└─ Total: 20 chemins

Actions: /env path | /env list | /env set
```

---

## Mode `list`

```
📋 TOUTES LES VARIABLES D'ENVIRONNEMENT
═══════════════════════════════════════════════════════════════

FILTRE: $ARGUMENTS (all, system, user, "pattern")

VARIABLES SYSTÈME (Machine):
┌─────────────────────────────┬───────────────────────────────────────┐
│ Nom                         │ Valeur                                │
├─────────────────────────────┼───────────────────────────────────────┤
│ ComSpec                     │ C:\Windows\system32\cmd.exe           │
│ DriverData                  │ C:\Windows\System32\Drivers\DriverData│
│ NUMBER_OF_PROCESSORS        │ 8                                     │
│ OS                          │ Windows_NT                            │
│ PATHEXT                     │ .COM;.EXE;.BAT;.CMD;.VBS;.JS;.PS1    │
│ PROCESSOR_ARCHITECTURE      │ AMD64                                 │
│ PROCESSOR_IDENTIFIER        │ Intel64 Family 6 Model 165...        │
│ PROCESSOR_LEVEL             │ 6                                     │
│ PROCESSOR_REVISION          │ a503                                  │
│ PSModulePath                │ C:\Program Files\WindowsPowerShell... │
│ SystemDrive                 │ C:                                    │
│ SystemRoot                  │ C:\Windows                            │
│ TEMP                        │ C:\Windows\TEMP                       │
│ TMP                         │ C:\Windows\TEMP                       │
│ windir                      │ C:\Windows                            │
└─────────────────────────────┴───────────────────────────────────────┘

VARIABLES UTILISATEUR:
┌─────────────────────────────┬───────────────────────────────────────┐
│ Nom                         │ Valeur                                │
├─────────────────────────────┼───────────────────────────────────────┤
│ EDITOR                      │ code                                  │
│ GOPATH                      │ C:\Users\Jean\go                      │
│ JAVA_HOME                   │ C:\Program Files\Java\jdk-17          │
│ OneDrive                    │ C:\Users\Jean\OneDrive                │
│ TEMP                        │ C:\Users\Jean\AppData\Local\Temp      │
│ TMP                         │ C:\Users\Jean\AppData\Local\Temp      │
└─────────────────────────────┴───────────────────────────────────────┘

Total: 45 variables (30 système, 15 utilisateur)
```

---

## Mode `path`

```
📂 GESTION DU PATH
═══════════════════════════════════════════════════════════════

PATH SYSTÈME (s'applique à tous les utilisateurs):
┌───┬───────────────────────────────────────────────────┬───────────┐
│ # │ Chemin                                            │ État      │
├───┼───────────────────────────────────────────────────┼───────────┤
│ 1 │ C:\Windows\system32                               │ ✅ Existe │
│ 2 │ C:\Windows                                        │ ✅ Existe │
│ 3 │ C:\Windows\System32\Wbem                          │ ✅ Existe │
│ 4 │ C:\Windows\System32\WindowsPowerShell\v1.0        │ ✅ Existe │
│ 5 │ C:\Windows\System32\OpenSSH                       │ ✅ Existe │
│ 6 │ C:\Program Files\nodejs                           │ ✅ Existe │
│ 7 │ C:\Program Files\Git\cmd                          │ ✅ Existe │
│ 8 │ C:\Program Files\Docker\Docker\resources\bin      │ ✅ Existe │
│ 9 │ C:\Program Files\dotnet                           │ ✅ Existe │
│10 │ C:\OldProgram\bin                                 │ ❌ N'EXISTE PAS │
└───┴───────────────────────────────────────────────────┴───────────┘

PATH UTILISATEUR:
┌───┬───────────────────────────────────────────────────┬───────────┐
│ # │ Chemin                                            │ État      │
├───┼───────────────────────────────────────────────────┼───────────┤
│ 1 │ C:\Users\Jean\AppData\Local\Programs\Python312    │ ✅ Existe │
│ 2 │ C:\Users\Jean\AppData\Local\Programs\Python312\Sc │ ✅ Existe │
│ 3 │ C:\Users\Jean\.cargo\bin                          │ ✅ Existe │
│ 4 │ C:\Users\Jean\go\bin                              │ ✅ Existe │
│ 5 │ C:\Users\Jean\AppData\Local\Microsoft\WindowsApps │ ✅ Existe │
│ 6 │ C:\Users\Jean\.local\bin                          │ ❌ N'EXISTE PAS │
└───┴───────────────────────────────────────────────────┴───────────┘

⚠️ PROBLÈMES DÉTECTÉS:
├─ Chemin invalide (système): C:\OldProgram\bin
└─ Chemin invalide (user): C:\Users\Jean\.local\bin

ACTIONS:
1. Ajouter un chemin au PATH
2. Supprimer un chemin du PATH
3. Réordonner les chemins
4. Nettoyer les chemins invalides
5. Exporter la configuration PATH

Choix: _
```

---

## Mode `set "NOM" "valeur"`

```
✏️ DÉFINIR UNE VARIABLE
═══════════════════════════════════════════════════════════════

Variable: $NOM
Valeur: $VALEUR

PORTÉE:
1. [user] Utilisateur actuel (HKCU)
   └─ Disponible uniquement pour Jean

2. [system] Système (HKLM) - Nécessite admin
   └─ Disponible pour tous les utilisateurs

Choix: _

---

VÉRIFICATION:
├─ Variable existante: ❌ Non (nouvelle variable)
├─ Valeur valide: ✅
└─ Permissions: ✅

⚠️ Note: Les programmes ouverts ne verront pas la nouvelle 
   variable. Redémarrez les applications concernées ou 
   ouvrez une nouvelle session.

Créer JAVA_HOME = "C:\Program Files\Java\jdk-17" (user)? [O/N]

---

SI VARIABLE EXISTE:
├─ Valeur actuelle: C:\Program Files\Java\jdk-11
├─ Nouvelle valeur: C:\Program Files\Java\jdk-17
└─ Écraser? [O/N]
```

---

## Mode `backup/restore`

```
💾 SAUVEGARDE DES VARIABLES D'ENVIRONNEMENT
═══════════════════════════════════════════════════════════════

Cette action va sauvegarder:
├─ Variables système (nécessite admin)
├─ Variables utilisateur
├─ PATH système et utilisateur
└─ PATHEXT

Format: JSON + Script PowerShell de restauration
Destination: C:\Backups\EnvVars\env-backup-2026-02-03.json

Sauvegarder? [O/N]

---

🔄 RESTAURATION
═══════════════════════════════════════════════════════════════

SAUVEGARDES DISPONIBLES:
┌───┬──────────────────────────────┬────────────────┬──────────┐
│ # │ Fichier                      │ Date           │ Vars     │
├───┼──────────────────────────────┼────────────────┼──────────┤
│ 1 │ env-backup-2026-02-03.json   │ Aujourd'hui    │ 45       │
│ 2 │ env-backup-2026-01-15.json   │ Il y a 19j     │ 43       │
│ 3 │ env-backup-2025-12-01.json   │ Il y a 2 mois  │ 42       │
└───┴──────────────────────────────┴────────────────┴──────────┘

OPTIONS DE RESTAURATION:
1. [all] Restaurer toutes les variables
2. [user] Variables utilisateur uniquement
3. [path] PATH uniquement
4. [select] Sélectionner les variables

⚠️ Les variables existantes seront écrasées.

Choix: _
```

---

## Commandes de Référence

```powershell
# Lister toutes les variables
Get-ChildItem Env:

# Obtenir une variable
$env:JAVA_HOME
[Environment]::GetEnvironmentVariable("JAVA_HOME", "User")
[Environment]::GetEnvironmentVariable("JAVA_HOME", "Machine")

# Définir une variable (session)
$env:MAVARIABLE = "valeur"

# Définir variable persistante (utilisateur)
[Environment]::SetEnvironmentVariable("MAVARIABLE", "valeur", "User")

# Définir variable persistante (système - admin requis)
[Environment]::SetEnvironmentVariable("MAVARIABLE", "valeur", "Machine")

# Supprimer une variable
[Environment]::SetEnvironmentVariable("MAVARIABLE", $null, "User")

# PATH - Ajouter
$path = [Environment]::GetEnvironmentVariable("Path", "User")
$newPath = "$path;C:\MonChemin"
[Environment]::SetEnvironmentVariable("Path", $newPath, "User")

# PATH - Lister
$env:Path -split ';'

# Rafraîchir variables (nouvelle session)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Exporter
Get-ChildItem Env: | Export-Csv "env-backup.csv"
```
