# /certs - Gestion Certificats Windows

Gestion complète des certificats : magasins, SSL, export/import, PKI.

## Mode d'Utilisation

```
/certs                      # Vue d'ensemble certificats
/certs list                 # Lister tous les certificats
/certs personal             # Certificats personnels (My)
/certs trusted              # Autorités de certification racines
/certs expiring             # Certificats expirant bientôt
/certs view "thumbprint"    # Détails d'un certificat
/certs export "thumbprint"  # Exporter certificat
/certs import               # Importer certificat (.cer/.pfx)
/certs create               # Créer certificat auto-signé
/certs request              # Créer demande CSR
/certs delete "thumbprint"  # Supprimer certificat
/certs chain "thumbprint"   # Vérifier chaîne de confiance
```

Arguments: $ARGUMENTS

---

## Mode Défaut - Vue d'Ensemble

```
🔐 CERTIFICATS WINDOWS - VUE D'ENSEMBLE
═══════════════════════════════════════════════════════════════

📊 Résumé par Magasin
┌───────────────────────────────────────┬───────┬─────────────┐
│ Magasin                               │ Certs │ Alertes     │
├───────────────────────────────────────┼───────┼─────────────┤
│ 👤 Personnel (My)                     │ 12    │ ⚠️ 2 expirent│
│ 🏢 Intermediate CA                    │ 45    │ -           │
│ 🔒 Trusted Root CA                    │ 156   │ -           │
│ 🌐 Web Hosting                        │ 5     │ ⚠️ 1 expire │
│ 📧 Trusted Publishers                 │ 8     │ -           │
│ 🚫 Untrusted                          │ 3     │ -           │
└───────────────────────────────────────┴───────┴─────────────┘

⚠️ Alertes Certificats
┌─────────────────────────────────────────────────────────────┐
│ 🔴 EXPIRÉ                                                   │
│ └─ CN=old.server.com         Expiré: 2025-12-15            │
│                                                             │
│ 🟡 EXPIRE BIENTÔT (30 jours)                               │
│ ├─ CN=api.entreprise.com     Expire: 2026-03-01 (26j)      │
│ └─ CN=mail.entreprise.com    Expire: 2026-03-05 (30j)      │
└─────────────────────────────────────────────────────────────┘

📋 Certificats Utilisés (Services)
├─ IIS (HTTPS)         : *.entreprise.com ✅
├─ RDP                 : RDP-Cert-PC01 ✅
├─ WinRM (HTTPS)       : WinRM-PC01 ✅
└─ LDAPS               : DC01.entreprise.local ✅

🔧 Actions rapides:
├─ /certs expiring       - Voir tous expirants
├─ /certs create         - Créer auto-signé
└─ /certs import         - Importer certificat
```

---

## /certs personal - Certificats Personnels

```
👤 CERTIFICATS PERSONNELS (LocalMachine\My)
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│ 🟢 CN=*.entreprise.com                                      │
│ ├─ Émetteur      : DigiCert Global CA G2                    │
│ ├─ Valide        : 2025-06-15 → 2027-06-15                  │
│ ├─ Thumbprint    : A1B2C3D4E5F6G7H8I9J0...                 │
│ ├─ Clé privée    : ✅ Présente                              │
│ ├─ Usages        : Server Auth, Client Auth                 │
│ └─ Utilisé par   : IIS (Default Web Site, intranet)         │
├─────────────────────────────────────────────────────────────┤
│ 🟡 CN=api.entreprise.com                                    │
│ ├─ Émetteur      : Let's Encrypt Authority X3               │
│ ├─ Valide        : 2025-12-01 → 2026-03-01 (⚠️ 26 jours)   │
│ ├─ Thumbprint    : B2C3D4E5F6G7H8I9J0K1...                 │
│ ├─ Clé privée    : ✅ Présente                              │
│ ├─ Usages        : Server Auth                              │
│ └─ Utilisé par   : IIS (api.entreprise.com)                 │
├─────────────────────────────────────────────────────────────┤
│ 🟢 CN=PC-BUREAU.entreprise.local                            │
│ ├─ Émetteur      : Entreprise-CA                            │
│ ├─ Valide        : 2025-01-15 → 2027-01-15                  │
│ ├─ Thumbprint    : C3D4E5F6G7H8I9J0K1L2...                 │
│ ├─ Clé privée    : ✅ Présente                              │
│ ├─ Usages        : Server Auth, Client Auth                 │
│ └─ Utilisé par   : RDP, WinRM                               │
├─────────────────────────────────────────────────────────────┤
│ 🔴 CN=old.server.com (EXPIRÉ)                               │
│ ├─ Émetteur      : Let's Encrypt Authority X3               │
│ ├─ Expiré        : 2025-12-15                               │
│ ├─ Thumbprint    : D4E5F6G7H8I9J0K1L2M3...                 │
│ ├─ Clé privée    : ✅ Présente                              │
│ └─ Utilisé par   : Aucun                                    │
└─────────────────────────────────────────────────────────────┘

Total: 12 certificats (1 expiré, 1 expire bientôt)

🔧 Actions:
├─ /certs view "A1B2C3..."    - Détails certificat
├─ /certs export "A1B2C3..."  - Exporter
└─ /certs delete "D4E5F6..."  - Supprimer expiré
```

---

## /certs view "thumbprint" - Détails Certificat

```
🔍 DÉTAILS CERTIFICAT
═══════════════════════════════════════════════════════════════

📋 Informations Générales
┌─────────────────────────────────────────────────────────────┐
│ Subject             : CN=*.entreprise.com                   │
│                       O=Entreprise SAS                      │
│                       L=Paris, C=FR                         │
│                                                             │
│ Issuer              : CN=DigiCert Global CA G2              │
│                       O=DigiCert Inc                        │
│                                                             │
│ Serial Number       : 0A:1B:2C:3D:4E:5F:6G:7H              │
│ Thumbprint (SHA1)   : A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6    │
│ Thumbprint (SHA256) : AA11BB22CC33DD44EE55FF66...          │
└─────────────────────────────────────────────────────────────┘

📅 Validité
┌─────────────────────────────────────────────────────────────┐
│ Valide à partir de  : 2025-06-15 00:00:00 UTC              │
│ Expire le           : 2027-06-15 23:59:59 UTC              │
│ Jours restants      : 498 jours ✅                          │
└─────────────────────────────────────────────────────────────┘

🔑 Clé Publique
┌─────────────────────────────────────────────────────────────┐
│ Algorithme          : RSA                                   │
│ Taille clé          : 2048 bits                             │
│ Clé privée          : ✅ Présente et exportable            │
│ Provider            : Microsoft RSA SChannel Provider       │
└─────────────────────────────────────────────────────────────┘

📝 Extensions
┌─────────────────────────────────────────────────────────────┐
│ Key Usage           : Digital Signature, Key Encipherment   │
│ Enhanced Key Usage  : Server Authentication (1.3.6.1...)    │
│                       Client Authentication (1.3.6.1...)    │
│                                                             │
│ Subject Alt Names   :                                       │
│   DNS: *.entreprise.com                                     │
│   DNS: entreprise.com                                       │
│                                                             │
│ CRL Distribution    : http://crl.digicert.com/...          │
│ OCSP                : http://ocsp.digicert.com              │
│ CA Issuers          : http://cacerts.digicert.com/...      │
└─────────────────────────────────────────────────────────────┘

🔗 Chaîne de Certification
├─ [Root]   DigiCert Global Root CA          ✅ Trusted
├─ [Inter]  DigiCert Global CA G2            ✅ Valid
└─ [End]    *.entreprise.com                 ✅ Valid

🔧 Actions:
├─ /certs export "A1B2C3D4..." --with-key  - Exporter avec clé
├─ /certs chain "A1B2C3D4..."              - Vérifier chaîne
└─ /certs delete "A1B2C3D4..."             - Supprimer
```

---

## /certs create - Créer Certificat Auto-signé

```
➕ CRÉER CERTIFICAT AUTO-SIGNÉ
═══════════════════════════════════════════════════════════════

📋 Configuration:

1️⃣ Type de certificat
   ● Serveur Web (SSL/TLS)
   ○ Client Authentication
   ○ Code Signing
   ○ Encryption (Document)

2️⃣ Subject (CN)
   Common Name       : [monserver.local________]
   Organization      : [Mon Entreprise_________] (optionnel)
   Locality          : [Paris__________________] (optionnel)
   Country           : [FR] (optionnel)

3️⃣ Subject Alternative Names (SAN)
   ☑️ DNS: monserver.local
   ☑️ DNS: localhost
   ☐ IP: 192.168.1.100
   [+ Ajouter SAN]

4️⃣ Paramètres de clé
   Algorithme        : [RSA ▼]
   Taille            : [2048 ▼] bits
   Hash              : [SHA256 ▼]

5️⃣ Validité
   Durée             : [365] jours (max 398 pour SSL public)

6️⃣ Options
   ☑️ Clé privée exportable
   ☐ Ajouter aux Trusted Root CA (confiance locale)
   Magasin           : [LocalMachine\My ▼]

═══════════════════════════════════════════════════════════════

📋 Résumé:
┌─────────────────────────────────────────────────────────────┐
│ CN                : monserver.local                         │
│ SANs              : monserver.local, localhost              │
│ Validité          : 365 jours                               │
│ Clé               : RSA 2048, SHA256                        │
│ Magasin           : LocalMachine\My                         │
│ Exportable        : Oui                                     │
└─────────────────────────────────────────────────────────────┘

⚠️ Créer ce certificat? [O/N]

═══════════════════════════════════════════════════════════════

✅ Certificat créé avec succès!

Thumbprint: F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1

💡 Pour utiliser dans IIS:
   /iis bindings "SiteName" --add https --cert "F6G7H8..."
```

---

## /certs import - Importer Certificat

```
📥 IMPORTER CERTIFICAT
═══════════════════════════════════════════════════════════════

📋 Type de fichier:

1️⃣ Certificat seul (.cer, .crt, .pem)
   └─ Sans clé privée (pour CA ou vérification)

2️⃣ Certificat + Clé privée (.pfx, .p12)
   └─ Avec clé privée (pour serveurs SSL)

3️⃣ Chaîne de certificats (.p7b)
   └─ Plusieurs certificats CA

Choix: [2]

═══════════════════════════════════════════════════════════════

📁 Fichier PFX:
   Chemin            : [C:\Certs\nouveau-cert.pfx_]
   
🔑 Mot de passe PFX : [*******************]

📂 Magasin destination:
   ● LocalMachine\My (Personnel - serveurs)
   ○ LocalMachine\WebHosting (IIS)
   ○ CurrentUser\My (Personnel - utilisateur)
   ○ LocalMachine\Root (CA racine - ⚠️ Attention)

⚙️ Options d'import:
   ☑️ Marquer clé comme exportable
   ☑️ Inclure toutes les propriétés étendues
   ☐ Activer protection forte de la clé

═══════════════════════════════════════════════════════════════

✅ Import réussi!

┌─────────────────────────────────────────────────────────────┐
│ Certificat importé : CN=api.monsite.com                     │
│ Thumbprint         : G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2     │
│ Magasin            : LocalMachine\My                        │
│ Clé privée         : ✅ Présente                            │
│ Chaîne             : 2 certificats intermédiaires inclus    │
└─────────────────────────────────────────────────────────────┘
```

---

## /certs export - Exporter Certificat

```
📤 EXPORTER CERTIFICAT
═══════════════════════════════════════════════════════════════

📋 Certificat sélectionné:
CN=*.entreprise.com
Thumbprint: A1B2C3D4E5F6G7H8I9J0...

Format d'export:

1️⃣ Certificat seul (.cer)
   └─ Sans clé privée, format DER ou Base64

2️⃣ Avec clé privée (.pfx)
   └─ Inclut la clé privée (protégé par mot de passe)

3️⃣ Chaîne complète (.p7b)
   └─ Certificat + intermédiaires + racine

Choix: [2]

═══════════════════════════════════════════════════════════════

📁 Export PFX:

Chemin destination : [C:\Backup\cert-entreprise.pfx]

🔑 Mot de passe PFX:
   Nouveau           : [*******************]
   Confirmer         : [*******************]

⚙️ Options:
   ☑️ Inclure tous les certificats dans le chemin
   ☑️ Inclure propriétés étendues
   ☐ Supprimer clé privée après export

═══════════════════════════════════════════════════════════════

✅ Export réussi!

┌─────────────────────────────────────────────────────────────┐
│ Fichier            : C:\Backup\cert-entreprise.pfx          │
│ Taille             : 4.2 KB                                 │
│ Contenu            : Certificat + clé + 2 intermédiaires    │
│ Protégé            : ✅ Mot de passe                        │
└─────────────────────────────────────────────────────────────┘

⚠️ Conservez ce fichier et le mot de passe en lieu sûr!
```

---

## /certs expiring - Certificats Expirants

```
⚠️ CERTIFICATS EXPIRANTS
═══════════════════════════════════════════════════════════════

🔴 EXPIRÉS (Action immédiate requise)
┌─────────────────────────────────────────────────────────────┐
│ CN=old.server.com                                           │
│ ├─ Magasin    : LocalMachine\My                             │
│ ├─ Expiré    : 2025-12-15 (il y a 50 jours)                │
│ ├─ Thumbprint: D4E5F6G7H8...                               │
│ └─ Utilisé   : ❌ Aucun (peut être supprimé)               │
└─────────────────────────────────────────────────────────────┘

🟠 EXPIRE DANS 30 JOURS
┌─────────────────────────────────────────────────────────────┐
│ CN=api.entreprise.com                                       │
│ ├─ Magasin    : LocalMachine\My                             │
│ ├─ Expire     : 2026-03-01 (26 jours)                       │
│ ├─ Issuer     : Let's Encrypt                               │
│ ├─ Thumbprint : B2C3D4E5F6...                              │
│ └─ Utilisé    : IIS (api.entreprise.com)                   │
│                                                             │
│ 💡 Action: Renouveler via certbot ou ACME                  │
├─────────────────────────────────────────────────────────────┤
│ CN=mail.entreprise.com                                      │
│ ├─ Magasin    : LocalMachine\My                             │
│ ├─ Expire     : 2026-03-05 (30 jours)                       │
│ ├─ Issuer     : Let's Encrypt                               │
│ ├─ Thumbprint : E5F6G7H8I9...                              │
│ └─ Utilisé    : SMTP Server                                │
└─────────────────────────────────────────────────────────────┘

🟡 EXPIRE DANS 90 JOURS
└─ Aucun

📊 Résumé:
├─ Expirés              : 1
├─ Expire < 30 jours    : 2
├─ Expire < 90 jours    : 0
└─ Total à surveiller   : 3

🔧 Actions recommandées:
├─ /certs delete "D4E5F6G7H8..." - Supprimer expiré inutilisé
├─ Renouveler api.entreprise.com via ACME/certbot
└─ Planifier renouvellement mail.entreprise.com
```

---

## Commandes PowerShell de Référence

```powershell
# Lister certificats par magasin
Get-ChildItem Cert:\LocalMachine\My
Get-ChildItem Cert:\LocalMachine\Root
Get-ChildItem Cert:\LocalMachine\WebHosting
Get-ChildItem Cert:\CurrentUser\My

# Détails certificat
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Thumbprint -eq "A1B2C3..."}
Get-ChildItem Cert:\LocalMachine\My | Format-List *

# Certificats expirants
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.NotAfter -lt (Get-Date).AddDays(30)}

# Créer certificat auto-signé
New-SelfSignedCertificate -DnsName "server.local","localhost" `
    -CertStoreLocation "Cert:\LocalMachine\My" `
    -NotAfter (Get-Date).AddYears(1) `
    -KeyAlgorithm RSA `
    -KeyLength 2048 `
    -KeyExportPolicy Exportable `
    -Provider "Microsoft RSA SChannel Cryptographic Provider"

# Créer avec SAN et usages
New-SelfSignedCertificate -DnsName "server.local" `
    -CertStoreLocation "Cert:\LocalMachine\My" `
    -KeyUsage DigitalSignature,KeyEncipherment `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.1,1.3.6.1.5.5.7.3.2")

# Importer certificat
Import-Certificate -FilePath "C:\cert.cer" -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath "C:\cert.pfx" -CertStoreLocation Cert:\LocalMachine\My -Password (ConvertTo-SecureString -String "password" -AsPlainText -Force)

# Exporter certificat
$cert = Get-ChildItem Cert:\LocalMachine\My\A1B2C3D4...
Export-Certificate -Cert $cert -FilePath "C:\export.cer"

# Exporter avec clé privée
$pwd = ConvertTo-SecureString -String "password" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "C:\export.pfx" -Password $pwd

# Supprimer certificat
Remove-Item Cert:\LocalMachine\My\A1B2C3D4...

# Vérifier chaîne
$cert = Get-ChildItem Cert:\LocalMachine\My\A1B2C3D4...
Test-Certificate -Cert $cert -Policy SSL

# Certificat pour RDP
$rdpCert = Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -like "*RDP*"}
wmic /namespace:\\root\cimv2\TerminalServices PATH Win32_TSGeneralSetting Set SSLCertificateSHA1Hash="$($rdpCert.Thumbprint)"

# Interface graphique
certmgr.msc        # Utilisateur
certlm.msc         # Machine locale
```
