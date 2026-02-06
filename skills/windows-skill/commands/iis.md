# /iis - Gestion Internet Information Services (IIS)

Administration complète d'IIS : sites web, pools d'applications, certificats SSL.

## Mode d'Utilisation

```
/iis                        # État général IIS
/iis sites                  # Liste des sites web
/iis site "NomSite"         # Détails d'un site
/iis pools                  # Pools d'applications
/iis start "NomSite"        # Démarrer un site
/iis stop "NomSite"         # Arrêter un site
/iis restart "NomSite"      # Redémarrer un site
/iis create                 # Assistant création site
/iis bindings "NomSite"     # Gérer liaisons (ports/domaines)
/iis ssl                    # Gestion certificats SSL
/iis logs                   # Accès aux logs IIS
/iis config                 # Configuration avancée
/iis troubleshoot           # Dépannage IIS
```

Arguments: $ARGUMENTS

---

## Mode Défaut - État IIS

```
🌐 IIS - INTERNET INFORMATION SERVICES
═══════════════════════════════════════════════════════════════

📊 Service IIS
┌─────────────────────────────────────────────────────────────┐
│ Service W3SVC        : ✅ Running                           │
│ Version IIS          : 10.0.22621.1                         │
│ Mode Pipeline        : Intégré                              │
│ .NET CLR             : v4.0.30319                           │
│ Uptime               : 15 jours 8:23:45                     │
└─────────────────────────────────────────────────────────────┘

🌍 Sites Web (4)
┌──────────────────────┬──────────┬───────────────┬───────────┐
│ Site                 │ État     │ Liaisons      │ Chemin    │
├──────────────────────┼──────────┼───────────────┼───────────┤
│ Default Web Site     │ 🟢 Started│ *:80, *:443  │ C:\inet..│
│ api.entreprise.com   │ 🟢 Started│ *:443 (SSL)  │ D:\Web\..│
│ intranet             │ 🟢 Started│ *:8080       │ D:\Intra.│
│ dev-test             │ 🔴 Stopped│ *:8081       │ D:\Dev\..│
└──────────────────────┴──────────┴───────────────┴───────────┘

⚙️ Pools d'Applications (4)
┌──────────────────────┬──────────┬───────────┬───────────────┐
│ Pool                 │ État     │ .NET      │ Mode Pipeline │
├──────────────────────┼──────────┼───────────┼───────────────┤
│ DefaultAppPool       │ 🟢 Started│ v4.0     │ Intégré       │
│ ApiAppPool           │ 🟢 Started│ v4.0     │ Intégré       │
│ IntranetPool         │ 🟢 Started│ v4.0     │ Intégré       │
│ DevPool              │ 🔴 Stopped│ v4.0     │ Intégré       │
└──────────────────────┴──────────┴───────────┴───────────────┘

📈 Statistiques (24h)
├─ Requêtes totales    : 45,234
├─ Requêtes/sec (moy)  : 0.52
├─ Erreurs 4xx         : 234 (0.5%)
├─ Erreurs 5xx         : 12 (0.03%)
└─ Bande passante      : 2.3 GB

⚠️ Alertes
├─ 🟡 Certificat SSL "api.entreprise.com" expire dans 30 jours
└─ 🔴 Site "dev-test" arrêté
```

---

## /iis site "NomSite" - Détails Site

```
🌐 SITE: api.entreprise.com
═══════════════════════════════════════════════════════════════

📊 État Général
┌─────────────────────────────────────────────────────────────┐
│ ID Site              : 2                                    │
│ État                 : 🟢 Started                           │
│ Pool d'applications  : ApiAppPool                           │
│ Démarrage auto       : ✅ Oui                               │
│ Chemin physique      : D:\Web\API\wwwroot                   │
│ Protocole logging    : W3C                                  │
└─────────────────────────────────────────────────────────────┘

🔗 Liaisons (Bindings)
┌───────────┬───────────────────────────┬───────┬─────────────┐
│ Protocol  │ Host Name                 │ Port  │ SSL         │
├───────────┼───────────────────────────┼───────┼─────────────┤
│ https     │ api.entreprise.com        │ 443   │ ✅ Cert OK  │
│ https     │ api.staging.entreprise.com│ 443   │ ✅ Cert OK  │
│ http      │ *                         │ 80    │ → Redirect  │
└───────────┴───────────────────────────┴───────┴─────────────┘

📁 Applications Virtuelles
├─ / (Racine)                    → D:\Web\API\wwwroot
├─ /docs                         → D:\Web\API\docs
└─ /swagger                      → D:\Web\API\swagger-ui

⚙️ Configuration
┌─────────────────────────────────────────────────────────────┐
│ Document par défaut  : index.html, default.aspx             │
│ Navigation répertoire: ❌ Désactivé                         │
│ Erreurs détaillées   : ❌ Désactivé (Production)            │
│ Compression          : ✅ Gzip activé                       │
│ CORS                 : ✅ Configuré                         │
│ URL Rewrite          : ✅ 3 règles actives                  │
└─────────────────────────────────────────────────────────────┘

📈 Statistiques Site (24h)
├─ Requêtes           : 12,456
├─ Temps réponse moy  : 45ms
├─ Codes 2xx          : 11,890 (95.5%)
├─ Codes 3xx          : 234 (1.9%)
├─ Codes 4xx          : 298 (2.4%)
├─ Codes 5xx          : 34 (0.3%)
└─ Bande passante     : 890 MB

🔐 Certificat SSL
┌─────────────────────────────────────────────────────────────┐
│ Subject              : api.entreprise.com                   │
│ Issuer               : Let's Encrypt Authority X3           │
│ Valide du            : 2025-12-01                           │
│ Expire le            : 2026-03-01 (⚠️ 26 jours)            │
│ Thumbprint           : A1B2C3D4...                          │
└─────────────────────────────────────────────────────────────┘

🔧 Actions:
├─ /iis stop "api.entreprise.com"    - Arrêter
├─ /iis restart "api.entreprise.com" - Redémarrer
├─ /iis bindings "api.entreprise.com"- Gérer liaisons
└─ /iis logs "api.entreprise.com"    - Voir logs
```

---

## /iis pools - Pools d'Applications

```
⚙️ POOLS D'APPLICATIONS IIS
═══════════════════════════════════════════════════════════════

📋 Pools Configurés
┌────────────────────┬──────────┬─────────────┬────────────────┐
│ Pool               │ État     │ Worker PID  │ Mémoire        │
├────────────────────┼──────────┼─────────────┼────────────────┤
│ DefaultAppPool     │ 🟢 Started│ 4532       │ 125 MB         │
│ ApiAppPool         │ 🟢 Started│ 5678       │ 456 MB         │
│ IntranetPool       │ 🟢 Started│ 6789       │ 234 MB         │
│ DevPool            │ 🔴 Stopped│ -          │ -              │
└────────────────────┴──────────┴─────────────┴────────────────┘

📊 Détails: ApiAppPool
┌─────────────────────────────────────────────────────────────┐
│ Version .NET        : v4.0                                  │
│ Mode Pipeline       : Intégré                               │
│ Identité            : ApplicationPoolIdentity               │
│ Enable 32-bit       : ❌ Non                                │
│ Démarrage auto      : ✅ Oui                                │
│ Idle Timeout        : 20 minutes                            │
│ Recyclage           : 29:00:00 (quotidien)                  │
│ Limite mémoire      : 0 (illimité)                          │
│ Limite CPU          : 0 (illimité)                          │
│ Max Worker Process  : 1                                     │
│ Queue Length        : 1000                                  │
└─────────────────────────────────────────────────────────────┘

📈 Santé des Pools (5 dernières minutes)
├─ ApiAppPool
│  ├─ CPU         : ██░░░░░░░░ 8%
│  ├─ Mémoire     : ████░░░░░░ 456 MB / 2 GB
│  ├─ Requêtes    : 234/min
│  └─ Erreurs     : 0
├─ DefaultAppPool
│  ├─ CPU         : █░░░░░░░░░ 2%
│  ├─ Mémoire     : █░░░░░░░░░ 125 MB / 2 GB
│  └─ Requêtes    : 45/min

🔧 Actions:
├─ /iis pools recycle "ApiAppPool" - Recycler
├─ /iis pools stop "ApiAppPool"    - Arrêter
└─ /iis pools config "ApiAppPool"  - Configurer
```

---

## /iis create - Assistant Création Site

```
➕ ASSISTANT CRÉATION SITE WEB
═══════════════════════════════════════════════════════════════

📋 Configuration du Site:

1️⃣ Informations générales
   Nom du site        : [nouveau-site___________]
   Chemin physique    : [D:\Web\nouveau-site\___]

2️⃣ Pool d'applications
   ○ Utiliser pool existant: [DefaultAppPool ▼]
   ● Créer nouveau pool    : [NouveauSitePool____]
     ├─ Version .NET      : [v4.0 ▼]
     └─ Mode Pipeline     : [Intégré ▼]

3️⃣ Liaisons (Bindings)
   ┌─────────┬─────────────────────────┬───────┐
   │ Type    │ Host Name               │ Port  │
   ├─────────┼─────────────────────────┼───────┤
   │ http    │ nouveau-site.local      │ 80    │
   │ [+ Ajouter liaison]                       │
   └─────────┴─────────────────────────┴───────┘

   ☐ Ajouter HTTPS (nécessite certificat)

4️⃣ Authentification
   ● Anonyme (public)
   ○ Windows (intranet)
   ○ Basic + Windows

═══════════════════════════════════════════════════════════════

📋 Résumé:
┌─────────────────────────────────────────────────────────────┐
│ Nom               : nouveau-site                            │
│ Chemin            : D:\Web\nouveau-site\                    │
│ Pool              : NouveauSitePool (Nouveau)               │
│ URL               : http://nouveau-site.local               │
│ Authentification  : Anonyme                                 │
└─────────────────────────────────────────────────────────────┘

⚠️ Créer ce site? [O/N]
```

---

## /iis ssl - Gestion Certificats SSL

```
🔐 CERTIFICATS SSL IIS
═══════════════════════════════════════════════════════════════

📋 Certificats Installés (Web Hosting)
┌─────────────────────────────────────────────────────────────┐
│ 🟢 api.entreprise.com                                       │
│ ├─ Issuer       : Let's Encrypt Authority X3                │
│ ├─ Expire       : 2026-03-01 (⚠️ 26 jours)                 │
│ ├─ Thumbprint   : A1B2C3D4E5F6...                          │
│ └─ Utilisé par  : api.entreprise.com (2 bindings)          │
├─────────────────────────────────────────────────────────────┤
│ 🟢 *.entreprise.com (Wildcard)                              │
│ ├─ Issuer       : DigiCert Global CA                        │
│ ├─ Expire       : 2027-06-15 (✅ 498 jours)                │
│ ├─ Thumbprint   : B2C3D4E5F6G7...                          │
│ └─ Utilisé par  : Default Web Site, intranet               │
├─────────────────────────────────────────────────────────────┤
│ 🔴 old.entreprise.com (EXPIRÉ)                              │
│ ├─ Issuer       : Let's Encrypt                             │
│ ├─ Expiré       : 2025-12-15 (❌ -50 jours)                │
│ ├─ Thumbprint   : C3D4E5F6G7H8...                          │
│ └─ Utilisé par  : Aucun                                     │
└─────────────────────────────────────────────────────────────┘

⚠️ Alertes Certificats:
├─ 🟡 api.entreprise.com expire dans 26 jours
└─ 🔴 old.entreprise.com expiré (supprimer?)

🔧 Actions:
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
🔧 DÉPANNAGE IIS
═══════════════════════════════════════════════════════════════

📋 DIAGNOSTIC AUTOMATIQUE

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

❌ Erreur web.config: dev-test
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
│ 🔧 Démarrer le pool: /iis pools start "DevPool"            │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

🛠️ PROBLÈMES COURANTS

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

## Commandes PowerShell de Référence

```powershell
# Importer module IIS
Import-Module WebAdministration
Import-Module IISAdministration

# État IIS
Get-Service W3SVC, WAS
Get-IISServerManager

# Sites
Get-IISSite
Get-Website
Get-Website -Name "NomSite" | Format-List *

# Démarrer/Arrêter sites
Start-IISSite -Name "NomSite"
Stop-IISSite -Name "NomSite"
Start-Website -Name "NomSite"
Stop-Website -Name "NomSite"

# Créer site
New-IISSite -Name "NouveauSite" -BindingInformation "*:80:nouveau.local" -PhysicalPath "D:\Web\nouveau"
New-Website -Name "NouveauSite" -Port 80 -HostHeader "nouveau.local" -PhysicalPath "D:\Web\nouveau"

# Pools d'applications
Get-IISAppPool
Get-WebAppPoolState -Name "NomPool"
Start-WebAppPool -Name "NomPool"
Stop-WebAppPool -Name "NomPool"
Restart-WebAppPool -Name "NomPool"

# Créer pool
New-WebAppPool -Name "NouveauPool"
Set-ItemProperty IIS:\AppPools\NouveauPool -Name managedRuntimeVersion -Value "v4.0"

# Bindings
Get-WebBinding -Name "NomSite"
New-WebBinding -Name "NomSite" -Protocol https -Port 443 -HostHeader "site.com" -SslFlags 1

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
