# /iis - Gestion IIS - Avancé

Voir aussi: [[iis]]

SSL, logs, configuration avancée et dépannage IIS.

---

## /iis ssl - Gestion Certificats SSL

```
CERTIFICATS SSL IIS
═══════════════════════════════════════════════════════════════

Certificats Installés (Web Hosting)
┌─────────────────────────────────────────────────────────────┐
│ api.entreprise.com                                          │
│ ├─ Issuer       : Let's Encrypt Authority X3                │
│ ├─ Expire       : 2026-03-01 (⚠️ 26 jours)                 │
│ ├─ Thumbprint   : A1B2C3D4E5F6...                          │
│ └─ Utilisé par  : api.entreprise.com (2 bindings)          │
├─────────────────────────────────────────────────────────────┤
│ *.entreprise.com (Wildcard)                                 │
│ ├─ Issuer       : DigiCert Global CA                        │
│ ├─ Expire       : 2027-06-15 (✅ 498 jours)                │
│ ├─ Thumbprint   : B2C3D4E5F6G7...                          │
│ └─ Utilisé par  : Default Web Site, intranet               │
├─────────────────────────────────────────────────────────────┤
│ old.entreprise.com (EXPIRÉ)                                 │
│ ├─ Issuer       : Let's Encrypt                             │
│ ├─ Expiré       : 2025-12-15 (-50 jours)                   │
│ ├─ Thumbprint   : C3D4E5F6G7H8...                          │
│ └─ Utilisé par  : Aucun                                     │
└─────────────────────────────────────────────────────────────┘

⚠️ Alertes Certificats:
├─ api.entreprise.com expire dans 26 jours
└─ old.entreprise.com expiré (supprimer?)

Actions:
├─ [1] Importer certificat (.pfx)
├─ [2] Créer demande certificat (CSR)
├─ [3] Générer certificat auto-signé
├─ [4] Renouveler Let's Encrypt
├─ [5] Associer certificat à binding
├─ [6] Supprimer certificat inutilisé
└─ [7] Voir certificats expirés

Choix: _
```

---

## /iis troubleshoot - Dépannage IIS

```
DÉPANNAGE IIS
═══════════════════════════════════════════════════════════════

DIAGNOSTIC AUTOMATIQUE

1. Services IIS
   ├─ W3SVC (World Wide Web)        ✅ Running
   ├─ WAS (Process Activation)       ✅ Running
   ├─ WMSVC (Web Management)         ✅ Running
   └─ HTTP.sys (Kernel driver)       ✅ Chargé

2. Pools d'Applications
   ├─ Tous les pools démarrés        ⚠️ 1/4 arrêté
   ├─ Workers processus santé        ✅ OK
   └─ Recyclages récents (1h)        ✅ 0 crash

3. Sites Web
   ├─ Chemins physiques accessibles  ✅ OK
   ├─ Permissions NTFS               ✅ OK
   └─ Bindings uniques               ✅ Pas de conflit

4. Configuration
   ├─ applicationHost.config         ✅ Valide
   ├─ web.config sites               ⚠️ 1 erreur
   └─ Modules chargés                ✅ OK

5. Connectivité
   ├─ Port 80 accessible             ✅ OK
   ├─ Port 443 accessible            ✅ OK
   └─ Firewall règles IIS            ✅ OK

═══════════════════════════════════════════════════════════════

⚠️ PROBLÈMES DÉTECTÉS:

Erreur web.config: dev-test
┌─────────────────────────────────────────────────────────────┐
│ Fichier: D:\Dev\test\web.config                             │
│ Erreur: Configuration section 'customModule' not found      │
│ Ligne: 45                                                   │
│                                                             │
│ Solution: Vérifier que le module est installé ou            │
│          commenter la section dans web.config               │
└─────────────────────────────────────────────────────────────┘

⚠️ Pool arrêté: DevPool
┌─────────────────────────────────────────────────────────────┐
│ Le pool DevPool est arrêté. Sites affectés: dev-test        │
│                                                             │
│ Dernière erreur: Unhandled exception in worker process      │
│ Voir: Event Log > Application                               │
│                                                             │
│ Démarrer le pool: /iis pools start "DevPool"                │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

PROBLÈMES COURANTS

Erreur 500 (Internal Server Error):
├─ 1. Vérifier web.config
├─ 2. Activer erreurs détaillées (dev)
├─ 3. Consulter Event Viewer
└─ 4. Vérifier permissions

Erreur 503 (Service Unavailable):
├─ 1. Vérifier pool d'applications
├─ 2. Vérifier Event Viewer pour crash
└─ 3. Recycler le pool

Site inaccessible:
├─ 1. Vérifier binding (port/hostname)
├─ 2. Vérifier firewall Windows
├─ 3. Vérifier fichier hosts
└─ 4. ipconfig /flushdns
```

---

## Commandes PowerShell de Référence (Avancé)

```powershell
# Certificats SSL
Get-ChildItem Cert:\LocalMachine\WebHosting
Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.HasPrivateKey }

# Associer certificat
$cert = Get-ChildItem Cert:\LocalMachine\WebHosting | Where-Object {$_.Subject -like "*site.com*"}
New-Item IIS:\SslBindings\0.0.0.0!443!site.com -Value $cert

# Logs IIS
Get-WebConfigurationProperty -Filter "system.applicationHost/sites/siteDefaults/logFile" -Name "directory"
# Logs par défaut: C:\inetpub\logs\LogFiles\

# Configuration
Get-WebConfiguration -Filter "/system.webServer/defaultDocument" -PSPath "IIS:\Sites\NomSite"

# Dépannage
& "$env:windir\system32\inetsrv\appcmd.exe" list site
& "$env:windir\system32\inetsrv\appcmd.exe" list apppool

# Interface graphique
inetmgr.exe
```
