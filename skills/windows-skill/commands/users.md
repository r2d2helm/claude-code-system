# Gestion des Utilisateurs Windows

Administration des comptes utilisateurs locaux.

## Mode d'Utilisation
```
/users                      → Liste des utilisateurs et leur statut
/users info NomUtilisateur  → Détails d'un utilisateur
/users create               → Assistant création d'utilisateur
/users groups               → Liste des groupes locaux
/users sessions             → Sessions actives
/users audit                → Audit des accès et connexions
/users lockout              → Comptes verrouillés
```

Arguments: $ARGUMENTS

---

## Liste des Utilisateurs (défaut)

```
👥 UTILISATEURS LOCAUX
═══════════════════════════════════════════════════════════════
Nom             │ Type      │ Statut   │ Dernière Connexion
────────────────┼───────────┼──────────┼────────────────────
Administrateur  │ 👑 Admin  │ Désactivé│ Jamais
DefaultAccount  │ 👤 System │ Désactivé│ Jamais
Invité          │ 👤 Invité │ Désactivé│ Jamais
Jean.Dupont     │ 👑 Admin  │ ✅ Actif │ 2026-02-03 09:15
Marie.Martin    │ 👤 User   │ ✅ Actif │ 2026-02-02 18:30
ServiceAccount  │ 🔧 Svc    │ ✅ Actif │ N/A
═══════════════════════════════════════════════════════════════

Résumé:
├─ Total: X utilisateurs
├─ Actifs: X
├─ Administrateurs: X
└─ Sans mot de passe: X (⚠️ si > 0)
```

---

## Mode `info NomUtilisateur`

Informations détaillées:

```
👤 DÉTAILS: Jean.Dupont
═══════════════════════════════════════
Nom complet       : Jean Dupont
SID               : S-1-5-21-...
Statut            : ✅ Actif
Créé le           : 2025-06-15
Dernière connexion: 2026-02-03 09:15

Groupes:
├─ Administrateurs
├─ Utilisateurs
└─ Remote Desktop Users

Mot de passe:
├─ Dernière modification: 2026-01-15
├─ Expire: Jamais / 2026-04-15
├─ Peut changer: Oui
└─ Requis: Oui

Profil:
├─ Chemin: C:\Users\Jean.Dupont
├─ Taille: 15.2 GB
└─ Dernier accès: 2026-02-03

Sessions actives: 1
└─ Console, depuis 09:15
```

---

## Mode `create`

Assistant interactif de création (avec confirmation):

```
📝 CRÉATION D'UN NOUVEL UTILISATEUR

1. Nom d'utilisateur: _____
   (lettres, chiffres, tirets uniquement)

2. Nom complet (optionnel): _____

3. Description (optionnel): _____

4. Mot de passe: _____
   ⚠️ Requis: 8+ caractères, majuscule, minuscule, chiffre

5. Type de compte:
   [1] Utilisateur standard
   [2] Administrateur

6. Options:
   [ ] L'utilisateur doit changer le mot de passe à la prochaine connexion
   [ ] L'utilisateur ne peut pas changer le mot de passe
   [ ] Le mot de passe n'expire jamais
   [ ] Compte désactivé

Confirmer la création? [O/N]
```

Commande générée:
```powershell
$Password = ConvertTo-SecureString "***" -AsPlainText -Force
New-LocalUser -Name "NomUser" -Password $Password -FullName "Nom Complet" -Description "Description"
Add-LocalGroupMember -Group "Utilisateurs" -Member "NomUser"
```

---

## Mode `groups`

```
👥 GROUPES LOCAUX
═══════════════════════════════════════════════════════════════
Groupe                    │ Membres │ Description
──────────────────────────┼─────────┼───────────────────────────
Administrateurs           │ 2       │ Accès complet au système
Utilisateurs              │ 4       │ Utilisateurs standard
Remote Desktop Users      │ 1       │ Accès Bureau à distance
Opérateurs de sauvegarde  │ 0       │ Droits de sauvegarde
Utilisateurs du journal..│ 0       │ Accès aux journaux
═══════════════════════════════════════════════════════════════
```

Pour voir les membres d'un groupe:
```
/users groups Administrateurs
```

---

## Mode `sessions`

```
🖥️ SESSIONS ACTIVES
═══════════════════════════════════════════════════════════════
ID  │ Utilisateur    │ Type      │ État      │ Depuis    │ Idle
────┼────────────────┼───────────┼───────────┼───────────┼──────
1   │ Jean.Dupont    │ Console   │ Actif     │ 09:15     │ 0m
2   │ Marie.Martin   │ RDP       │ Déconnecté│ Hier 18:30│ 14h
3   │ Admin          │ RDP       │ Actif     │ 10:45     │ 5m
═══════════════════════════════════════════════════════════════

Actions possibles (avec confirmation):
- Déconnecter une session
- Envoyer un message à un utilisateur
- Fermer une session (logoff)
```

---

## Mode `audit`

```
🔐 AUDIT DES CONNEXIONS (7 derniers jours)
═══════════════════════════════════════════════════════════════

Connexions réussies: 45
Connexions échouées: 3

Par utilisateur:
├─ Jean.Dupont: 30 réussies, 1 échouée
├─ Marie.Martin: 12 réussies, 0 échouée
└─ Inconnu: 3 échouées (⚠️ tentatives sur compte inexistant)

Dernières connexions échouées:
┌──────────────────┬────────────────┬───────────────────────────┐
│ Date             │ Utilisateur    │ Raison                    │
├──────────────────┼────────────────┼───────────────────────────┤
│ 2026-02-03 03:45 │ admin          │ Mot de passe incorrect    │
│ 2026-02-02 22:10 │ administrator  │ Compte désactivé          │
│ 2026-02-02 22:08 │ root           │ Utilisateur inconnu       │
└──────────────────┴────────────────┴───────────────────────────┘

⚠️ ALERTE: Tentatives de connexion suspectes détectées
   IP source: Vérifier les logs pour plus de détails
```

---

## Mode `lockout`

```
🔒 COMPTES VERROUILLÉS
═══════════════════════════════════════════════════════════════
Utilisateur     │ Verrouillé depuis │ Tentatives │ Action
────────────────┼───────────────────┼────────────┼──────────
TestUser        │ 2026-02-03 08:30  │ 5          │ [Déverrouiller?]
═══════════════════════════════════════════════════════════════

Politique de verrouillage actuelle:
├─ Seuil de verrouillage: 5 tentatives
├─ Durée de verrouillage: 30 minutes
└─ Réinitialisation du compteur: 30 minutes
```

Pour déverrouiller (avec confirmation):
```powershell
Enable-LocalUser -Name "TestUser"
# ou
net user TestUser /active:yes
```

---

## Commandes de Référence

```powershell
# Lister utilisateurs
Get-LocalUser | Select-Object Name, Enabled, LastLogon

# Créer utilisateur
New-LocalUser -Name "Nom" -Password (ConvertTo-SecureString "Pass" -AsPlainText -Force)

# Ajouter à un groupe
Add-LocalGroupMember -Group "Administrateurs" -Member "Nom"

# Sessions actives
query user

# Événements de connexion
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4624,4625} -MaxEvents 50

# Politique de verrouillage
net accounts
```
