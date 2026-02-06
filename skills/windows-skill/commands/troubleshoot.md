# Dépannage Guidé Windows

Assistant de résolution de problèmes courants.

## Mode d'Utilisation
```
/troubleshoot                → Menu principal des problèmes
/troubleshoot internet       → Problèmes de connexion Internet
/troubleshoot slow           → PC lent / performances
/troubleshoot audio          → Problèmes audio
/troubleshoot printer        → Problèmes d'impression
/troubleshoot bluescreen     → Écrans bleus (BSOD)
/troubleshoot update         → Problèmes Windows Update
/troubleshoot boot           → Problèmes de démarrage
/troubleshoot app "nom"      → Application qui ne fonctionne pas
```

Arguments: $ARGUMENTS

---

## Menu Principal (défaut)

```
🔧 ASSISTANT DE DÉPANNAGE
═══════════════════════════════════════════════════════════════

Quel problème rencontrez-vous?

CONNECTIVITÉ:
  1. [internet]  - Pas d'accès Internet / Wi-Fi ne fonctionne pas
  2. [network]   - Réseau local inaccessible / Partages

PERFORMANCES:
  3. [slow]      - Ordinateur lent / Se fige
  4. [startup]   - Démarrage trop long

MATÉRIEL:
  5. [audio]     - Pas de son / Micro ne fonctionne pas
  6. [printer]   - Imprimante ne fonctionne pas
  7. [display]   - Problèmes d'affichage / Écran

SYSTÈME:
  8. [bluescreen] - Écrans bleus (BSOD)
  9. [update]     - Windows Update bloqué / Erreurs
  10. [boot]      - Ne démarre pas correctement

APPLICATION:
  11. [app]       - Une application ne fonctionne pas

Tapez le numéro ou le mot-clé: _
```

---

## Mode `internet`

```
🌐 DÉPANNAGE: CONNEXION INTERNET
═══════════════════════════════════════════════════════════════

📋 DIAGNOSTIC AUTOMATIQUE EN COURS...

ÉTAPE 1: Vérification de l'interface réseau
├─ Adaptateur Wi-Fi: ✅ Activé
├─ Adaptateur Ethernet: ❌ Câble non connecté
└─ Adresse IP: 192.168.1.45 ✅

ÉTAPE 2: Test de connectivité locale
├─ Passerelle (192.168.1.1): ✅ Accessible (2ms)
└─ Serveur DHCP: ✅ Fonctionnel

ÉTAPE 3: Test DNS
├─ Résolution DNS locale: ✅ OK
├─ Résolution DNS externe: ❌ ÉCHEC
└─ DNS configuré: 192.168.1.1

ÉTAPE 4: Test Internet
├─ Ping 8.8.8.8: ❌ Timeout
└─ HTTP google.com: ❌ Échec

═══════════════════════════════════════════════════════════════
🔍 PROBLÈME IDENTIFIÉ: Pas de connectivité vers Internet
   Diagnostic: La passerelle locale répond mais pas Internet
   Cause probable: Problème avec le routeur/modem ou FAI

📌 SOLUTIONS À ESSAYER (dans l'ordre):

1. REDÉMARRER LE ROUTEUR
   → Débranchez votre box/routeur 30 secondes puis rebranchez
   → Attendez 2 minutes que la connexion se rétablisse
   
   Réessayer après? [O/N]

2. RÉINITIALISER LA CONFIGURATION RÉSEAU
   → Exécuter les commandes suivantes:
   
   ipconfig /release
   ipconfig /flushdns
   ipconfig /renew
   netsh winsock reset
   
   ⚠️ Nécessite un redémarrage. Exécuter? [O/N]

3. TESTER AVEC DNS ALTERNATIFS
   → Configurer DNS Google (8.8.8.8) ou Cloudflare (1.1.1.1)
   
   Changer les DNS automatiquement? [O/N]

4. Si le problème persiste:
   → Contacter votre FAI - le problème semble externe
```

---

## Mode `slow`

```
🐌 DÉPANNAGE: ORDINATEUR LENT
═══════════════════════════════════════════════════════════════

📋 ANALYSE DES PERFORMANCES EN COURS...

UTILISATION ACTUELLE:
├─ CPU: 85% ⚠️ ÉLEVÉ
├─ RAM: 92% 🔴 CRITIQUE (14.7/16 GB)
├─ Disque C: 45% activité
└─ Réseau: 2% activité

TOP CONSOMMATEURS:
┌────────────────────────────┬───────┬──────────┬──────────────┐
│ Processus                  │ CPU % │ RAM (MB) │ Recommandation│
├────────────────────────────┼───────┼──────────┼──────────────┤
│ chrome.exe (42 onglets)    │ 35%   │ 4,200    │ Fermer onglets│
│ MsMpEng.exe (Defender)     │ 25%   │ 450      │ Analyse active│
│ Teams.exe                  │ 12%   │ 1,800    │ Normal       │
│ Code.exe                   │ 8%    │ 1,200    │ Normal       │
│ SearchIndexer.exe          │ 5%    │ 150      │ Indexation   │
└────────────────────────────┴───────┴──────────┴──────────────┘

═══════════════════════════════════════════════════════════════
🔍 PROBLÈMES IDENTIFIÉS:

1. 🔴 MÉMOIRE RAM SATURÉE
   → Chrome utilise 4.2 GB avec 42 onglets ouverts
   
   Solutions:
   a) Fermer les onglets Chrome inutiles
   b) Utiliser une extension de gestion d'onglets
   c) Considérer plus de RAM (16→32 GB)

2. ⚠️ ANALYSE ANTIVIRUS EN COURS
   → Windows Defender effectue une analyse
   → Durée estimée: ~15 minutes
   → Le CPU reviendra à la normale après

📌 ACTIONS RAPIDES:

1. LIBÉRER DE LA MÉMOIRE MAINTENANT
   → Fermer Chrome? (libère ~4 GB) [O/N]
   → Fermer Teams? (libère ~1.8 GB) [O/N]

2. OPTIMISATIONS RECOMMANDÉES
   → Désactiver programmes au démarrage inutiles
   → Vider le cache système
   → Vérifier si mise à jour Windows en arrière-plan

Exécuter les optimisations automatiques? [O/N]
```

---

## Mode `bluescreen`

```
💀 DÉPANNAGE: ÉCRAN BLEU (BSOD)
═══════════════════════════════════════════════════════════════

📋 ANALYSE DES CRASHS SYSTÈME...

HISTORIQUE DES BSOD (90 derniers jours):
┌──────────────────┬─────────────────────────┬───────────────────┐
│ Date             │ Code d'arrêt            │ Module fautif     │
├──────────────────┼─────────────────────────┼───────────────────┤
│ 2026-02-02 23:45 │ KERNEL_DATA_INPAGE_ERROR│ ntfs.sys          │
│ 2026-01-28 15:30 │ DRIVER_IRQL_NOT_LESS    │ nvlddmkm.sys      │
│ 2026-01-15 09:20 │ DRIVER_IRQL_NOT_LESS    │ nvlddmkm.sys      │
└──────────────────┴─────────────────────────┴───────────────────┘

ANALYSE DÉTAILLÉE:

🔍 BSOD #1: KERNEL_DATA_INPAGE_ERROR (2026-02-02)
├─ Signification: Erreur de lecture de données depuis le disque
├─ Module: ntfs.sys (système de fichiers)
├─ Causes possibles:
│  ├─ Secteurs défectueux sur le disque
│  ├─ Câble SATA défectueux
│  └─ RAM défectueuse
└─ Actions recommandées:
   1. Vérifier la santé du disque: /disk health
   2. Exécuter chkdsk: chkdsk C: /F /R
   3. Tester la RAM: mdsched.exe

🔍 BSOD #2 & #3: DRIVER_IRQL_NOT_LESS (répété)
├─ Signification: Pilote accédant à mémoire invalide
├─ Module: nvlddmkm.sys (pilote NVIDIA)
├─ Causes possibles:
│  ├─ Pilote graphique corrompu ou incompatible
│  └─ Carte graphique défaillante
└─ Actions recommandées:
   1. Mettre à jour le pilote NVIDIA
   2. Ou réinstaller proprement (DDU + pilote frais)

═══════════════════════════════════════════════════════════════
📌 PLAN D'ACTION RECOMMANDÉ:

PRIORITÉ 1: Problème de pilote NVIDIA (2 occurrences)
→ Télécharger le dernier pilote NVIDIA
→ Utiliser DDU pour désinstaller proprement
→ Installer le nouveau pilote

PRIORITÉ 2: Vérifier l'intégrité du disque
→ Exécuter chkdsk au prochain redémarrage

Voulez-vous:
1. Voir comment mettre à jour le pilote NVIDIA
2. Planifier un chkdsk
3. Lancer le diagnostic mémoire Windows
4. Voir les fichiers dump pour analyse avancée

Choix: _
```

---

## Mode `update`

```
🔄 DÉPANNAGE: WINDOWS UPDATE
═══════════════════════════════════════════════════════════════

📋 DIAGNOSTIC WINDOWS UPDATE...

ÉTAT DU SERVICE:
├─ Service wuauserv: ✅ Running
├─ Service BITS: ✅ Running
├─ Service cryptsvc: ✅ Running
└─ Service msiserver: ✅ Running

DERNIÈRE ERREUR DÉTECTÉE:
├─ Code: 0x80070002
├─ Date: 2026-02-01 14:32
├─ Mise à jour: KB5033123
└─ Description: Le système ne trouve pas le fichier spécifié

VÉRIFICATIONS:
├─ Espace disque C: 147 GB libre ✅
├─ Connexion Internet: ✅ OK
├─ Serveurs Windows Update: ✅ Accessibles
└─ Cache Windows Update: 2.8 GB (peut être corrompu)

═══════════════════════════════════════════════════════════════
📌 SOLUTIONS AUTOMATISÉES:

NIVEAU 1: Nettoyage du cache (résout 80% des problèmes)
┌────────────────────────────────────────────────────────────┐
│ Cette action va:                                           │
│ 1. Arrêter les services Windows Update                     │
│ 2. Vider le dossier SoftwareDistribution                   │
│ 3. Vider le dossier catroot2                               │
│ 4. Redémarrer les services                                 │
│                                                            │
│ Durée: ~2 minutes | Risque: Aucun                          │
└────────────────────────────────────────────────────────────┘
Exécuter? [O/N]

NIVEAU 2: Réparation des composants système
┌────────────────────────────────────────────────────────────┐
│ 1. DISM /Online /Cleanup-Image /RestoreHealth              │
│ 2. sfc /scannow                                            │
│                                                            │
│ Durée: 20-45 minutes | Risque: Aucun                       │
└────────────────────────────────────────────────────────────┘
Exécuter si niveau 1 échoue? [O/N]

NIVEAU 3: Réinitialisation complète de Windows Update
┌────────────────────────────────────────────────────────────┐
│ Script Microsoft officiel de réinitialisation              │
│ Réinitialise tous les composants Windows Update            │
│                                                            │
│ Durée: 5-10 minutes | Risque: Faible                       │
└────────────────────────────────────────────────────────────┘
```

---

## Mode `app "nom"`

```
🔧 DÉPANNAGE APPLICATION: Microsoft Teams
═══════════════════════════════════════════════════════════════

📋 ANALYSE DE L'APPLICATION...

INFORMATIONS:
├─ Version installée: 24004.1307.2669.7070
├─ Type: Application UWP (Store)
├─ Emplacement: C:\Program Files\WindowsApps\...
└─ Dernière mise à jour: 2026-01-28

ÉTAT ACTUEL:
├─ Processus en cours: ❌ Non
├─ Services dépendants: ✅ OK
└─ Fichiers: ✅ Intègres

SYMPTÔMES COURANTS ET SOLUTIONS:

1. L'APPLICATION NE DÉMARRE PAS
   → Effacer le cache: %AppData%\Microsoft\Teams
   → Réinitialiser l'application via Paramètres
   → Réinstaller

2. L'APPLICATION SE FIGE / CRASH
   → Vérifier les mises à jour
   → Désactiver l'accélération matérielle
   → Mode de compatibilité

3. PROBLÈMES AUDIO/VIDÉO
   → Vérifier les permissions (Caméra, Micro)
   → Mettre à jour les pilotes audio/vidéo
   → Sélectionner les bons périphériques dans Teams

📌 ACTIONS DISPONIBLES:

1. Effacer le cache Teams (garde les identifiants)
2. Réinitialiser complètement Teams
3. Réparer l'application (Windows)
4. Désinstaller et réinstaller
5. Vérifier les permissions Windows

Quel problème rencontrez-vous? Ou choisissez une action (1-5): _
```

---

## Commandes de Référence

```powershell
# Lancer l'utilitaire de résolution des problèmes Windows
msdt.exe /id NetworkDiagnosticsWeb
msdt.exe /id WindowsUpdateDiagnostic
msdt.exe /id AudioPlaybackDiagnostic
msdt.exe /id PrinterDiagnostic

# Réinitialiser la pile réseau
netsh winsock reset
netsh int ip reset

# Réinitialiser Windows Update
net stop wuauserv
net stop bits
net stop cryptsvc
del /q/f/s %SYSTEMROOT%\SoftwareDistribution\*
net start cryptsvc
net start bits
net start wuauserv

# Analyser les fichiers dump BSOD
Get-WinEvent -FilterHashtable @{LogName='System'; Id=1001} | Select-Object -First 10

# Réinitialiser une application UWP
Get-AppxPackage *Teams* | Reset-AppxPackage

# Réparer une application
Get-AppxPackage *Teams* | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"}
```
