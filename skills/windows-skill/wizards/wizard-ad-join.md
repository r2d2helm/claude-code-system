# Wizard: Active Directory Join

Jonction domaine Active Directory Windows 11/Server 2025.

## Déclenchement

```
/win-wizard ad-join
```

## Étapes du Wizard (4)

### Étape 1: Prérequis

```
╔══════════════════════════════════════════════════════════════╗
║           🏢 WIZARD AD JOIN                                  ║
║                Étape 1/4 : Prérequis                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔍 VÉRIFICATION PRÉREQUIS:                                  ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✅ Connectivité réseau         : OK                     │ ║
║  │ ✅ DNS configuré               : 192.168.1.10 (DC)      │ ║
║  │ ✅ Résolution domaine          : corp.local OK          │ ║
║  │ ✅ Port LDAP (389)             : Accessible             │ ║
║  │ ✅ Port Kerberos (88)          : Accessible             │ ║
║  │ ⚠️  Heure système              : Décalage 2 min         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⚠️ Synchronisez l'heure avec le DC avant de continuer       ║
║                                                              ║
║  [1] Synchroniser l'heure et continuer                       ║
║  [2] Ignorer et continuer                                    ║
║  [3] Annuler                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Vérifier prérequis
Test-NetConnection -ComputerName "dc01.corp.local" -Port 389
Test-NetConnection -ComputerName "dc01.corp.local" -Port 88
Resolve-DnsName "corp.local"

# Synchroniser heure avec DC
w32tm /resync /rediscover
```

### Étape 2: Informations Domaine

```
╔══════════════════════════════════════════════════════════════╗
║           🏢 WIZARD AD JOIN                                  ║
║               Étape 2/4 : Domaine                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Entrez les informations du domaine :                        ║
║                                                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Nom de domaine    : corp.local_______________           │ ║
║  │                                                         │ ║
║  │ Compte avec droits de jonction :                        │ ║
║  │ Utilisateur       : admin@corp.local________            │ ║
║  │ Mot de passe      : ************************            │ ║
║  │                                                         │ ║
║  │ OU de destination (optionnel) :                         │ ║
║  │ OU=Workstations,DC=corp,DC=local                        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Valider et continuer                                    ║
║  [2] Parcourir les OUs disponibles                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 3: Jonction au Domaine

```
╔══════════════════════════════════════════════════════════════╗
║           🏢 WIZARD AD JOIN                                  ║
║                Étape 3/4 : Jonction                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📋 RÉSUMÉ:                                                  ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Ordinateur : WORKSTATION-01                             │ ║
║  │ Domaine    : corp.local                                 │ ║
║  │ OU         : OU=Workstations,DC=corp,DC=local           │ ║
║  │ Compte     : admin@corp.local                           │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⚠️ Cette action nécessite un redémarrage                    ║
║                                                              ║
║  [1] Joindre le domaine                                      ║
║  [2] Modifier les paramètres                                 ║
║  [3] Annuler                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Jonction au domaine avec OU spécifique
$Credential = Get-Credential -Message "Compte avec droits de jonction"
$OU = "OU=Workstations,DC=corp,DC=local"

Add-Computer -DomainName "corp.local" -Credential $Credential -OUPath $OU -Force -Restart

# Alternative sans OU spécifique
Add-Computer -DomainName "corp.local" -Credential $Credential -Force -Restart
```

### Étape 4: Post-Jonction

```
╔══════════════════════════════════════════════════════════════╗
║           🏢 WIZARD AD JOIN                                  ║
║              Étape 4/4 : Post-Jonction                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✅ JONCTION RÉUSSIE!                                        ║
║                                                              ║
║  Actions post-jonction recommandées :                        ║
║                                                              ║
║  [x] Ajouter utilisateurs domaine aux admins locaux          ║
║  [x] Configurer stratégies de groupe                         ║
║  [ ] Activer profils itinérants                              ║
║  [ ] Configurer redirection dossiers                         ║
║                                                              ║
║  Utilisateur domaine à ajouter aux admins locaux :           ║
║  CORP\Domain Admins (déjà membre)                            ║
║  CORP\IT-Support____________________________                 ║
║                                                              ║
║  [1] Appliquer et redémarrer                                 ║
║  [2] Redémarrer sans configuration supplémentaire            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes post-jonction:**
```powershell
# Ajouter groupe domaine aux admins locaux
Add-LocalGroupMember -Group "Administrators" -Member "CORP\IT-Support"

# Vérifier la jonction
Get-ComputerInfo | Select-Object CsDomain, CsPartOfDomain

# Forcer mise à jour GPO
gpupdate /force

# Redémarrer
Restart-Computer -Force
```
