# Gestion BitLocker

Chiffrement de disque BitLocker.

## Mode d'Utilisation
```
/bitlocker                  → État du chiffrement
/bitlocker status           → Statut détaillé de tous les disques
/bitlocker enable "C:"      → Activer BitLocker sur un volume
/bitlocker disable "C:"     → Désactiver BitLocker
/bitlocker lock "D:"        → Verrouiller un volume
/bitlocker unlock "D:"      → Déverrouiller un volume
/bitlocker key              → Gérer les clés de récupération
/bitlocker tpm              → État du TPM
```

Arguments: $ARGUMENTS

---

## État Général (défaut)

```
🔐 BITLOCKER - ÉTAT DU CHIFFREMENT
═══════════════════════════════════════════════════════════════

TPM (Trusted Platform Module):
├─ Présent: ✅ Oui
├─ Version: 2.0
├─ Activé: ✅ Oui
├─ Propriétaire: ✅ Défini
└─ État: Prêt pour BitLocker

VOLUMES:
┌────────┬─────────────┬────────────────┬───────────────┬───────────────┐
│ Volume │ Taille      │ État           │ Protection    │ Méthode       │
├────────┼─────────────┼────────────────┼───────────────┼───────────────┤
│ C:     │ 500 GB      │ ✅ Chiffré     │ ✅ Activée    │ XTS-AES 256   │
│ D:     │ 1 TB        │ ✅ Chiffré     │ 🔓 Déverrouillé│ XTS-AES 256  │
│ E:     │ 256 GB      │ ❌ Non chiffré │ -             │ -             │
└────────┴─────────────┴────────────────┴───────────────┴───────────────┘

RÉCUPÉRATION:
├─ Clés sauvegardées: ✅ Azure AD
├─ Clés sauvegardées: ✅ Fichier local
└─ Dernière sauvegarde: 2026-01-15

ALERTES:
└─ ℹ️ Volume E: non protégé (données potentiellement exposées)
```

---

## Mode `status`

```
📊 STATUT DÉTAILLÉ BITLOCKER
═══════════════════════════════════════════════════════════════

VOLUME C: (Système)
┌──────────────────────────────────────────────────────────────────────────┐
│ État: ✅ Entièrement chiffré                                            │
├──────────────────────────────────────────────────────────────────────────┤
│ Protection: ✅ Activée                                                   │
│ Méthode de chiffrement: XTS-AES 256 bits                                │
│ Pourcentage chiffré: 100%                                               │
│ État du verrouillage: Déverrouillé                                      │
│                                                                          │
│ Protecteurs de clé:                                                      │
│ ├─ TPM (protecteur principal)                                           │
│ │  └─ PCR Validation: 0, 2, 4, 11                                       │
│ ├─ Clé de récupération numérique                                        │
│ │  └─ ID: {ABC123DE-F456-...}                                           │
│ └─ Mot de passe de récupération                                         │
│    └─ ID: {DEF456GH-I789-...}                                           │
│                                                                          │
│ Déverrouillage automatique: ✅ Activé (TPM)                             │
└──────────────────────────────────────────────────────────────────────────┘

VOLUME D: (Données)
┌──────────────────────────────────────────────────────────────────────────┐
│ État: ✅ Chiffré                                                        │
├──────────────────────────────────────────────────────────────────────────┤
│ Protection: 🔓 Volume déverrouillé                                      │
│ Méthode: XTS-AES 256 bits                                               │
│                                                                          │
│ Protecteurs:                                                             │
│ ├─ Mot de passe                                                         │
│ ├─ Clé de récupération                                                  │
│ └─ Déverrouillage auto: ✅ (basé sur C:)                               │
└──────────────────────────────────────────────────────────────────────────┘

VOLUME E: (USB)
┌──────────────────────────────────────────────────────────────────────────┐
│ État: ❌ Non chiffré                                                    │
├──────────────────────────────────────────────────────────────────────────┤
│ Type: Disque amovible                                                    │
│ Système de fichiers: NTFS                                               │
│ BitLocker To Go: Disponible                                             │
│                                                                          │
│ 💡 Suggestion: Protéger avec BitLocker To Go                            │
│    /bitlocker enable E:                                                 │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Mode `enable "volume"`

```
🔒 ACTIVER BITLOCKER: E:
═══════════════════════════════════════════════════════════════

VÉRIFICATIONS PRÉALABLES:
├─ Volume valide: ✅
├─ Espace libre suffisant: ✅ (2% minimum)
├─ Système de fichiers: ✅ NTFS
└─ TPM disponible: ✅

CONFIGURATION:

1. MÉTHODE DE CHIFFREMENT:
   [1] XTS-AES 128 bits (plus rapide)
   [2] XTS-AES 256 bits (plus sécurisé) - Recommandé

2. PROTECTEUR DE CLÉ:
   [x] Mot de passe (pour volumes non-système)
   [x] Clé de récupération (obligatoire)
   [ ] Clé USB de démarrage
   [ ] TPM + PIN (volumes système)

3. MODE DE CHIFFREMENT:
   [1] Espace utilisé uniquement (plus rapide)
   [2] Volume entier (plus sécurisé)

4. SAUVEGARDE CLÉ DE RÉCUPÉRATION:
   [x] Fichier local (C:\BitLocker\recovery-E.txt)
   [ ] Compte Microsoft
   [ ] Azure AD
   [ ] Imprimer

RÉSUMÉ:
├─ Volume: E: (256 GB)
├─ Chiffrement: XTS-AES 256
├─ Mode: Espace utilisé
└─ Durée estimée: ~15 minutes

⚠️ Ne pas interrompre le processus de chiffrement.

Activer BitLocker? [O/N]
```

---

## Mode `key`

```
🔑 CLÉS DE RÉCUPÉRATION BITLOCKER
═══════════════════════════════════════════════════════════════

CLÉS DISPONIBLES:
┌────────┬─────────────────────────┬─────────────────────────────────┐
│ Volume │ ID Clé                  │ Sauvegardes                     │
├────────┼─────────────────────────┼─────────────────────────────────┤
│ C:     │ {ABC123DE-F456-...}     │ ☁️ Azure AD, 📄 Fichier        │
│ D:     │ {DEF456GH-I789-...}     │ 📄 Fichier                      │
└────────┴─────────────────────────┴─────────────────────────────────┘

ACTIONS:
1. Afficher une clé de récupération
2. Sauvegarder une clé vers un fichier
3. Sauvegarder vers Azure AD
4. Sauvegarder vers compte Microsoft
5. Ajouter un nouveau protecteur
6. Supprimer un protecteur

Choix: _

---

AFFICHER CLÉ: C:
⚠️ ATTENTION: Cette clé permet de déchiffrer votre disque.
Gardez-la en lieu sûr et ne la partagez jamais.

ID: {ABC123DE-F456-7890-ABCD-EF1234567890}
Clé de récupération:
╔═══════════════════════════════════════════════════════╗
║  123456-789012-345678-901234-567890-123456-789012-34 ║
╚═══════════════════════════════════════════════════════╝

Copier dans le presse-papiers? [O/N]
```

---

## Mode `tpm`

```
🔧 MODULE TPM (Trusted Platform Module)
═══════════════════════════════════════════════════════════════

INFORMATIONS TPM:
├─ Présent: ✅ Oui
├─ Version: 2.0
├─ Fabricant: Intel (inteltpm)
├─ Version firmware: 403.1.0.0
├─ Niveau de spécification: 1.16

ÉTAT:
├─ TPM activé: ✅ Oui
├─ TPM prêt: ✅ Oui
├─ Propriétaire défini: ✅ Oui
├─ Verrouillé: ❌ Non
└─ Compteur lockout: 0/32

ATTESTATION:
├─ EK Certificate: ✅ Présent
├─ AIK: ✅ Configuré
└─ PCR Banks: SHA-256

UTILISATION:
├─ BitLocker: ✅ En cours d'utilisation
├─ Windows Hello: ✅ Configuré
├─ Credential Guard: ✅ Activé
└─ Device Guard: ✅ Activé

ACTIONS:
1. Effacer le TPM (⚠️ perte données BitLocker)
2. Réinitialiser le lockout
3. Exporter les informations
4. Résoudre les problèmes TPM
```

---

## Mode `unlock "volume"`

```
🔓 DÉVERROUILLER VOLUME: D:
═══════════════════════════════════════════════════════════════

MÉTHODES DISPONIBLES:
1. [password] Mot de passe BitLocker
2. [recovery] Clé de récupération (48 chiffres)
3. [key] Fichier clé USB

Choix: _

---

MOT DE PASSE:
Entrez le mot de passe BitLocker: ********

✅ Volume D: déverrouillé avec succès!

OPTIONS:
[ ] Activer le déverrouillage automatique
    (déverrouille automatiquement quand C: est déverrouillé)

Activer? [O/N]
```

---

## Commandes de Référence

```powershell
# État de tous les volumes
Get-BitLockerVolume

# Détails d'un volume
Get-BitLockerVolume -MountPoint "C:"

# Activer BitLocker
Enable-BitLocker -MountPoint "E:" -EncryptionMethod XtsAes256 -PasswordProtector -Password (Read-Host -AsSecureString)

# Ajouter clé de récupération
Add-BitLockerKeyProtector -MountPoint "E:" -RecoveryPasswordProtector

# Sauvegarder clé vers fichier
(Get-BitLockerVolume -MountPoint "C:").KeyProtector | Out-File "C:\recovery.txt"

# Déverrouiller
Unlock-BitLocker -MountPoint "D:" -Password (Read-Host -AsSecureString)
Unlock-BitLocker -MountPoint "D:" -RecoveryPassword "123456-789012-..."

# Verrouiller
Lock-BitLocker -MountPoint "D:"

# Désactiver BitLocker
Disable-BitLocker -MountPoint "E:"

# TPM
Get-Tpm
Initialize-Tpm
Clear-Tpm  # ⚠️ Dangereux

# Suspendre protection (ex: BIOS update)
Suspend-BitLocker -MountPoint "C:" -RebootCount 1
Resume-BitLocker -MountPoint "C:"
```
