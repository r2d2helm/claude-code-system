# Gestion Windows Update

Administration complète des mises à jour Windows.

## Mode d'Utilisation
```
/update                     → État et mises à jour disponibles
/update check               → Rechercher les mises à jour
/update install             → Installer les mises à jour (avec confirmation)
/update history             → Historique des mises à jour
/update failed              → Mises à jour échouées et diagnostic
/update pause               → Suspendre les mises à jour
/update drivers             → Mises à jour de pilotes disponibles
/update rollback            → Désinstaller une mise à jour récente
```

Arguments: $ARGUMENTS

---

## État Actuel (défaut)

```
🔄 WINDOWS UPDATE
═══════════════════════════════════════════════════════════════

ÉTAT DU SERVICE:
├─ Service wuauserv: ✅ Running
├─ Service BITS: ✅ Running
├─ Dernière vérification: 2026-02-03 06:00
└─ Dernière installation: 2026-01-28

VERSION WINDOWS:
├─ Édition: Windows 10 Pro
├─ Version: 22H2
├─ Build: 19045.3996
└─ Experience Pack: 1000.19053.1000.0

MISES À JOUR DISPONIBLES: 3
┌────────────────────────────────────────────────┬───────┬──────────┐
│ Mise à jour                                    │ Type  │ Taille   │
├────────────────────────────────────────────────┼───────┼──────────┤
│ KB5034441 - Cumulative Update (Feb 2026)       │ 🔴 Crit│ 450 MB   │
│ KB5034203 - .NET Framework 4.8.1               │ 🟡 Imp │ 56 MB    │
│ Intel - Display - 31.0.101.5122               │ 🟢 Opt │ 890 MB   │
└────────────────────────────────────────────────┴───────┴──────────┘

STATUT:
├─ Mises à jour critiques en attente: 1 ⚠️
├─ Redémarrage requis: Non
└─ Suspension active: Non

Actions suggérées:
→ Installer KB5034441 (mise à jour de sécurité critique)
```

---

## Mode `check`

```
🔍 RECHERCHE DE MISES À JOUR...
═══════════════════════════════════════════════════════════════

Connexion au serveur Windows Update... ✅
Téléchargement du catalogue... ✅
Analyse du système... ✅

RÉSULTATS:
┌────────────────────────────────────────────────────────────────┐
│ 🔴 CRITIQUES (Sécurité)                                        │
├────────────────────────────────────────────────────────────────┤
│ KB5034441 - 2026-02 Cumulative Update for Windows 10           │
│   Taille: 450 MB │ Date: 2026-02-13                            │
│   Corrige: 12 vulnérabilités dont 3 critiques                  │
├────────────────────────────────────────────────────────────────┤
│ 🟠 IMPORTANTES                                                 │
├────────────────────────────────────────────────────────────────┤
│ KB5034203 - .NET Framework 4.8.1 Security Update               │
│   Taille: 56 MB │ Date: 2026-02-10                             │
├────────────────────────────────────────────────────────────────┤
│ 🟢 OPTIONNELLES                                                │
├────────────────────────────────────────────────────────────────┤
│ Intel Corporation - Display - 31.0.101.5122                    │
│   Taille: 890 MB │ Date: 2026-01-25                            │
└────────────────────────────────────────────────────────────────┘

Total: 3 mises à jour (1.4 GB)
Temps d'installation estimé: 15-30 minutes

Installer maintenant? [O/N/Sélectionner]
```

---

## Mode `install`

⚠️ DEMANDER CONFIRMATION AVANT D'INSTALLER

```
📥 INSTALLATION DES MISES À JOUR
═══════════════════════════════════════════════════════════════

Mises à jour à installer:
1. [x] KB5034441 - Cumulative Update (450 MB) - CRITIQUE
2. [x] KB5034203 - .NET Framework (56 MB)
3. [ ] Intel Display Driver (890 MB) - Optionnel

Options:
├─ Redémarrer automatiquement si nécessaire: [O/N]
└─ Installer en arrière-plan: [O/N]

⚠️ AVERTISSEMENT:
- Sauvegarder le travail en cours
- L'installation peut prendre 15-30 minutes
- Un redémarrage peut être nécessaire

Confirmer l'installation? [O/N]
```

Progression:
```
📥 Installation en cours...

[1/2] KB5034441 - Téléchargement... 100%
[1/2] KB5034441 - Installation... ████████████░░░░░░░░ 65%
      Étape: Applying changes...

[2/2] KB5034203 - En attente...

Temps écoulé: 8m 32s
Temps restant estimé: ~5 minutes
```

---

## Mode `history`

```
📜 HISTORIQUE DES MISES À JOUR
═══════════════════════════════════════════════════════════════

30 DERNIERS JOURS:
┌──────────────┬─────────────────────────────────────┬─────────┐
│ Date         │ Mise à jour                         │ Statut  │
├──────────────┼─────────────────────────────────────┼─────────┤
│ 2026-01-28   │ KB5034122 - Security Update         │ ✅ OK   │
│ 2026-01-28   │ KB5033920 - Servicing Stack         │ ✅ OK   │
│ 2026-01-15   │ KB5033456 - Cumulative Update       │ ✅ OK   │
│ 2026-01-15   │ KB5033123 - .NET Framework          │ ❌ Échec│
│ 2026-01-10   │ Windows Malicious Software Removal  │ ✅ OK   │
│ 2026-01-02   │ KB5032890 - Cumulative Update       │ ✅ OK   │
└──────────────┴─────────────────────────────────────┴─────────┘

Statistiques:
├─ Installées avec succès: 28
├─ Échecs: 2
└─ Désinstallées: 1

Filtrer: /update history failed | /update history 90days
```

---

## Mode `failed`

```
❌ MISES À JOUR ÉCHOUÉES
═══════════════════════════════════════════════════════════════

ÉCHECS RÉCENTS:
┌────────────────────────────────────────────────────────────────┐
│ KB5033123 - .NET Framework 4.8.1 Update                        │
│ Date: 2026-01-15 14:32                                         │
│ Code erreur: 0x80070002                                        │
│ Description: Le système ne peut pas trouver le fichier spécifié│
├────────────────────────────────────────────────────────────────┤
│ DIAGNOSTIC:                                                    │
│ ├─ Cause probable: Fichiers système corrompus                  │
│ ├─ Espace disque: ✅ Suffisant (147 GB libre)                  │
│ └─ Intégrité système: ⚠️ Non vérifié                          │
├────────────────────────────────────────────────────────────────┤
│ SOLUTIONS SUGGÉRÉES:                                           │
│ 1. Exécuter sfc /scannow                                       │
│ 2. Exécuter DISM /Online /Cleanup-Image /RestoreHealth         │
│ 3. Vider le cache Windows Update                               │
│ 4. Réessayer l'installation                                    │
└────────────────────────────────────────────────────────────────┘

Lancer le diagnostic automatique? [O/N]
```

Script de réparation automatique:
```powershell
# 1. Arrêter les services
Stop-Service wuauserv, bits -Force

# 2. Vider le cache
Remove-Item "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force

# 3. Réinitialiser les composants
DISM /Online /Cleanup-Image /RestoreHealth

# 4. Redémarrer les services
Start-Service wuauserv, bits

# 5. Relancer la détection
wuauclt /detectnow
```

---

## Mode `pause`

```
⏸️ SUSPENSION DES MISES À JOUR
═══════════════════════════════════════════════════════════════

État actuel: Mises à jour actives

Options de suspension:
1. Suspendre 7 jours
2. Suspendre 14 jours
3. Suspendre 30 jours (maximum)
4. Reprendre les mises à jour

⚠️ Note: Les mises à jour de sécurité critiques peuvent 
   quand même s'installer selon la politique configurée.

Choix: _
```

---

## Mode `drivers`

```
🔧 MISES À JOUR DE PILOTES
═══════════════════════════════════════════════════════════════

DISPONIBLES VIA WINDOWS UPDATE:
┌────────────────────────────────────────────────┬─────────────┐
│ Pilote                                         │ Version     │
├────────────────────────────────────────────────┼─────────────┤
│ Intel - Display - Intel UHD Graphics           │ 31.0.101.5122│
│ Realtek - Audio - High Definition Audio        │ 6.0.9285.1  │
└────────────────────────────────────────────────┴─────────────┘

PILOTES ACTUELS:
┌────────────────────────────────────────────────┬─────────────┬────────────┐
│ Périphérique                                   │ Version     │ Date       │
├────────────────────────────────────────────────┼─────────────┼────────────┤
│ Intel UHD Graphics 630                         │ 30.0.101.1994│ 2025-08-15│
│ Realtek High Definition Audio                  │ 6.0.9071.1  │ 2025-06-20│
│ Intel I219-V Ethernet                          │ 12.19.2.44  │ 2025-04-10│
│ Samsung NVMe Controller                        │ 3.3.0.2003  │ 2025-01-05│
└────────────────────────────────────────────────┴─────────────┴────────────┘

⚠️ Recommandation: Installer les pilotes graphiques depuis le site Intel
   pour des fonctionnalités optimales (OpenCL, encodage vidéo, etc.)
```

---

## Mode `rollback`

```
↩️ DÉSINSTALLATION DE MISE À JOUR
═══════════════════════════════════════════════════════════════

⚠️ ATTENTION: Opération sensible
   Ne désinstaller que si problèmes avérés après mise à jour.

MISES À JOUR DÉSINSTALLABLES:
┌────────────────────────────────────────────────┬──────────────┐
│ Mise à jour                                    │ Installée le │
├────────────────────────────────────────────────┼──────────────┤
│ 1. KB5034122 - Security Update                 │ 2026-01-28   │
│ 2. KB5033920 - Servicing Stack                 │ 2026-01-28   │
│ 3. KB5033456 - Cumulative Update               │ 2026-01-15   │
└────────────────────────────────────────────────┴──────────────┘

Numéro de la mise à jour à désinstaller: _

⚠️ Un redémarrage sera nécessaire.
⚠️ Créer un point de restauration avant? [Recommandé]
```

---

## Commandes de Référence

```powershell
# Installer le module PSWindowsUpdate
Install-Module PSWindowsUpdate -Force

# Rechercher les mises à jour
Get-WindowsUpdate

# Installer toutes les mises à jour
Install-WindowsUpdate -AcceptAll -AutoReboot

# Historique
Get-WUHistory | Select-Object -First 30

# Cacher une mise à jour
Hide-WindowsUpdate -KBArticleID KB5034441

# Désinstaller
wusa /uninstall /kb:5034122 /quiet /norestart

# Vérifier le service
Get-Service wuauserv, bits | Select-Object Name, Status

# Forcer la détection
wuauclt /detectnow
(New-Object -ComObject Microsoft.Update.AutoUpdate).DetectNow()
```
