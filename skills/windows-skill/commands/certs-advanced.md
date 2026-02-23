# /certs - Gestion Certificats Windows - Avancé

Voir aussi: [[certs]]

Export, renouvellement, certificats expirants et commandes avancées.

---

## /certs export - Exporter Certificat

```
EXPORTER CERTIFICAT
═══════════════════════════════════════════════════════════════

Certificat sélectionné:
CN=*.entreprise.com
Thumbprint: A1B2C3D4E5F6G7H8I9J0...

Format d'export:

1. Certificat seul (.cer)
   └─ Sans clé privée, format DER ou Base64

2. Avec clé privée (.pfx)
   └─ Inclut la clé privée (protégé par mot de passe)

3. Chaîne complète (.p7b)
   └─ Certificat + intermédiaires + racine

Choix: [2]

═══════════════════════════════════════════════════════════════

Export PFX:

Chemin destination : [C:\Backup\cert-entreprise.pfx]

Mot de passe PFX:
   Nouveau           : [*******************]
   Confirmer         : [*******************]

Options:
   Inclure tous les certificats dans le chemin
   Inclure propriétés étendues
   Supprimer clé privée après export

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

EXPIRÉS (Action immédiate requise)
┌─────────────────────────────────────────────────────────────┐
│ CN=old.server.com                                           │
│ ├─ Magasin    : LocalMachine\My                             │
│ ├─ Expiré    : 2025-12-15 (il y a 50 jours)                │
│ ├─ Thumbprint: D4E5F6G7H8...                               │
│ └─ Utilisé   : Aucun (peut être supprimé)                   │
└─────────────────────────────────────────────────────────────┘

EXPIRE DANS 30 JOURS
┌─────────────────────────────────────────────────────────────┐
│ CN=api.entreprise.com                                       │
│ ├─ Magasin    : LocalMachine\My                             │
│ ├─ Expire     : 2026-03-01 (26 jours)                       │
│ ├─ Issuer     : Let's Encrypt                               │
│ ├─ Thumbprint : B2C3D4E5F6...                              │
│ └─ Utilisé    : IIS (api.entreprise.com)                   │
│                                                             │
│ Action: Renouveler via certbot ou ACME                      │
├─────────────────────────────────────────────────────────────┤
│ CN=mail.entreprise.com                                      │
│ ├─ Magasin    : LocalMachine\My                             │
│ ├─ Expire     : 2026-03-05 (30 jours)                       │
│ ├─ Issuer     : Let's Encrypt                               │
│ ├─ Thumbprint : E5F6G7H8I9...                              │
│ └─ Utilisé    : SMTP Server                                │
└─────────────────────────────────────────────────────────────┘

EXPIRE DANS 90 JOURS
└─ Aucun

Résumé:
├─ Expirés              : 1
├─ Expire < 30 jours    : 2
├─ Expire < 90 jours    : 0
└─ Total à surveiller   : 3

Actions recommandées:
├─ /certs delete "D4E5F6G7H8..." - Supprimer expiré inutilisé
├─ Renouveler api.entreprise.com via ACME/certbot
└─ Planifier renouvellement mail.entreprise.com
```

---

## Commandes PowerShell de Référence (Avancé)

```powershell
# Créer avec SAN et usages
New-SelfSignedCertificate -DnsName "server.local" `
    -CertStoreLocation "Cert:\LocalMachine\My" `
    -KeyUsage DigitalSignature,KeyEncipherment `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.1,1.3.6.1.5.5.7.3.2")

# Exporter certificat
$cert = Get-ChildItem Cert:\LocalMachine\My\A1B2C3D4...
Export-Certificate -Cert $cert -FilePath "C:\export.cer"

# Exporter avec clé privée
$pwd = ConvertTo-SecureString -String "password" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "C:\export.pfx" -Password $pwd

# Vérifier chaîne
$cert = Get-ChildItem Cert:\LocalMachine\My\A1B2C3D4...
Test-Certificate -Cert $cert -Policy SSL

# Certificat pour RDP
$rdpCert = Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -like "*RDP*"}
wmic /namespace:\\root\cimv2\TerminalServices PATH Win32_TSGeneralSetting Set SSLCertificateSHA1Hash="$($rdpCert.Thumbprint)"
```
