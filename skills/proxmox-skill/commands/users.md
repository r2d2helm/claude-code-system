# 👥 /pve-users - Utilisateurs & Permissions

## Description
Gestion des utilisateurs, groupes, rôles et permissions Proxmox VE 9+.

## Syntaxe
```
/pve-users [action] [options]
```

## Architecture RBAC

```
┌─────────────────────────────────────────────────────┐
│                    RBAC Proxmox                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  REALM (pam, pve, ldap, ad, openid)                │
│      │                                              │
│      └── USER (user@realm)                         │
│              │                                      │
│              ├── GROUP (membership)                │
│              │                                      │
│              └── TOKEN (API access)                │
│                                                     │
│  ROLE (permissions set)                            │
│      │                                              │
│      └── PRIVILEGES (individual permissions)       │
│                                                     │
│  ACL (role assignment)                             │
│      path + user/group + role → permission         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Gestion Utilisateurs

### `list` - Lister utilisateurs
```bash
# Tous les utilisateurs
pveum user list

# Format JSON
pveum user list --output-format json-pretty

# Via API
pvesh get /access/users
```

### `add` - Créer utilisateur
```bash
# Utilisateur PAM (système)
pveum user add admin@pam --comment "Admin User"

# Utilisateur PVE (interne)
pveum user add developer@pve \
  --comment "Developer" \
  --email "dev@example.com" \
  --firstname "John" \
  --lastname "Doe"

# Avec expiration
pveum user add temp@pve --expire 1735689600  # Timestamp Unix
```

### `modify` - Modifier utilisateur
```bash
# Changer email
pveum user modify developer@pve --email "newmail@example.com"

# Désactiver utilisateur
pveum user modify developer@pve --enable 0

# Réactiver
pveum user modify developer@pve --enable 1
```

### `delete` - Supprimer utilisateur
```bash
pveum user delete developer@pve
```

### `passwd` - Changer mot de passe
```bash
# Interactif
pveum passwd developer@pve

# Via script (non recommandé)
echo -e "newpassword\nnewpassword" | pveum passwd developer@pve
```

## Gestion Groupes

### Créer et gérer groupes
```bash
# Créer groupe
pveum group add admins --comment "Administrators"
pveum group add developers --comment "Development Team"
pveum group add readonly --comment "Read-Only Users"

# Lister groupes
pveum group list

# Ajouter membre
pveum user modify developer@pve --group developers

# Supprimer groupe
pveum group delete developers
```

## Gestion Rôles

### Rôles prédéfinis
| Rôle | Description |
|------|-------------|
| `Administrator` | Tous les privilèges |
| `NoAccess` | Aucun accès |
| `PVEAdmin` | Admin sans gestion users |
| `PVEAuditor` | Lecture seule |
| `PVEDatastoreAdmin` | Admin stockage |
| `PVEDatastoreUser` | Usage stockage |
| `PVEPoolAdmin` | Admin pools |
| `PVEPoolUser` | Usage pools |
| `PVESysAdmin` | Admin système |
| `PVETemplateUser` | Usage templates |
| `PVEUserAdmin` | Admin utilisateurs |
| `PVEVMAdmin` | Admin VMs/CTs |
| `PVEVMUser` | Usage VMs/CTs |

### Créer rôle personnalisé
```bash
# Rôle backup operator
pveum role add BackupOperator \
  --privs "Datastore.Allocate,Datastore.AllocateSpace,VM.Backup"

# Rôle VM viewer
pveum role add VMViewer \
  --privs "VM.Audit,VM.Console"

# Lister privilèges disponibles
pveum privilege list

# Modifier rôle
pveum role modify BackupOperator \
  --privs "Datastore.Allocate,Datastore.AllocateSpace,VM.Backup,VM.Snapshot"

# Supprimer rôle
pveum role delete BackupOperator
```

## Gestion ACLs

### Syntax ACL
```bash
# pveum aclmod <path> -user|-group <name> -role <role> [-propagate 0|1]
```

### Chemins ACL
| Chemin | Scope |
|--------|-------|
| `/` | Racine (tout) |
| `/vms/{vmid}` | VM spécifique |
| `/pool/{pool}` | Pool |
| `/storage/{storage}` | Storage |
| `/nodes/{node}` | Node |
| `/sdn/{zone}` | Zone SDN |

### Exemples ACLs
```bash
# Admin global
pveum aclmod / -user admin@pam -role Administrator

# Admin VMs seulement
pveum aclmod / -user vmadmin@pve -role PVEVMAdmin

# Accès à une VM spécifique
pveum aclmod /vms/100 -user user@pve -role PVEVMUser

# Accès à un pool
pveum aclmod /pool/dev-pool -group developers -role PVEVMAdmin

# Accès storage
pveum aclmod /storage/backup-store -user backup@pve -role PVEDatastoreUser

# Sans propagation (ne s'applique pas aux enfants)
pveum aclmod /pool/production -user junior@pve -role PVEAuditor -propagate 0

# Lister ACLs
pveum acl list
```

## API Tokens

### Créer token
```bash
# Token avec tous les privilèges de l'utilisateur
pveum user token add automation@pve terraform-token --privsep 0
# IMPORTANT: Sauvegarder le secret affiché !

# Token avec privilèges séparés (plus sécurisé)
pveum user token add monitoring@pve grafana-token --privsep 1
pveum aclmod / -token 'monitoring@pve!grafana-token' -role PVEAuditor
```

### Lister tokens
```bash
pveum user token list automation@pve
```

### Supprimer token
```bash
pveum user token remove automation@pve terraform-token
```

## 2FA/TOTP

### Activer 2FA
```bash
# Via Web UI: Datacenter > Permissions > Two Factor

# Ajouter TOTP
pveum user tfa add admin@pam totp --description "Admin Phone"
# Scanner le QR code affiché

# Vérifier status
pveum user tfa-status admin@pam
```

### Recovery keys
```bash
# Générer recovery keys
pveum user tfa add admin@pam recovery --description "Recovery Codes"
# Sauvegarder les codes affichés !
```

## Realms (Authentification)

### Realm PAM (système Linux)
```bash
# Utilisateurs Linux existants
# Utiliser user@pam
```

### Realm PVE (interne)
```bash
# Base par défaut pour utilisateurs Proxmox
# Stocké dans /etc/pve/user.cfg
```

### Realm LDAP
```bash
pveum realm add myldap --type ldap \
  --server ldap.example.com \
  --base-dn "dc=example,dc=com" \
  --user-attr uid \
  --bind-dn "cn=admin,dc=example,dc=com" \
  --default 0
```

### Realm Active Directory
```bash
pveum realm add myad --type ad \
  --server dc.example.com \
  --domain example.com \
  --default 0
```

### Realm OpenID Connect
```bash
pveum realm add keycloak --type openid \
  --issuer-url "https://keycloak.example.com/realms/myrealm" \
  --client-id "proxmox" \
  --client-key "secret" \
  --username-claim "preferred_username" \
  --autocreate 1
```

## Pools

### Créer pool
```bash
# Pool pour projet
pveum pool add production --comment "Production VMs"
pveum pool add development --comment "Dev Environment"
```

### Ajouter ressources au pool
```bash
# Ajouter VM
pveum pool add production --vms 100,101,102

# Via qm
qm set 100 --pool production
```

### Permissions pool
```bash
pveum aclmod /pool/production -group admins -role PVEAdmin
pveum aclmod /pool/development -group developers -role PVEVMAdmin
```

## Exemples Scénarios

### Setup équipe développement
```bash
# Créer groupe
pveum group add dev-team --comment "Development Team"

# Créer pool
pveum pool add dev-env --comment "Development Environment"

# Créer utilisateurs
for user in alice bob charlie; do
    pveum user add ${user}@pve --group dev-team
done

# Permissions
pveum aclmod /pool/dev-env -group dev-team -role PVEVMAdmin
pveum aclmod /storage/iso -group dev-team -role PVEDatastoreUser
```

### Setup backup operator
```bash
# Créer rôle
pveum role add BackupOps --privs "Datastore.Audit,Datastore.AllocateSpace,VM.Backup,VM.Audit,VM.Snapshot"

# Créer utilisateur
pveum user add backup@pve --comment "Backup Operator"

# Token pour automation
pveum user token add backup@pve vzdump-token --privsep 0

# Permissions
pveum aclmod / -user backup@pve -role BackupOps
```

## Best Practices

1. **Principe du moindre privilège**: Donner uniquement les permissions nécessaires
2. **Groupes**: Toujours utiliser des groupes plutôt que des ACLs utilisateur
3. **Pools**: Organiser les ressources en pools
4. **API Tokens**: Pour toute automation, jamais de passwords
5. **2FA**: Obligatoire pour les admins
6. **Audit**: Vérifier régulièrement les permissions
