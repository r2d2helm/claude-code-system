# Sauvegarde et Restauration

Gestion des sauvegardes et points de restauration Windows.

## Mode d'Utilisation
```
/backup                     → État des sauvegardes et options
/backup create              → Créer un point de restauration
/backup list                → Liste des points de restauration
/backup restore             → Assistant de restauration
/backup config              → Sauvegarder la configuration système
/backup files "chemin"      → Sauvegarder des fichiers/dossiers
/backup registry            → Exporter le registre
```

Arguments: $ARGUMENTS

---

## État des Sauvegardes (défaut)

```
💾 ÉTAT DES SAUVEGARDES
═══════════════════════════════════════════════════════════════

PROTECTION SYSTÈME:
├─ État: ✅ Activée sur C:
├─ Espace alloué: 15 GB (max)
├─ Espace utilisé: 8.2 GB
└─ Points de restauration: 5

DERNIER POINT DE RESTAURATION:
├─ Date: 2026-02-01 14:30
├─ Description: "Maintenance mensuelle"
└─ Type: Manuel

HISTORIQUE DES FICHIERS:
├─ État: ❌ Non configuré
└─ Recommandation: Activer pour sauvegarder Documents, Images, etc.

SAUVEGARDE WINDOWS:
├─ État: ❌ Non configurée
└─ Dernière sauvegarde: Jamais

⚠️ RECOMMANDATIONS:
├─ Créer un point de restauration (> 7 jours depuis le dernier)
├─ Configurer l'Historique des fichiers vers un disque externe
└─ Envisager une sauvegarde complète du système

Actions rapides:
├─ /backup create "Description"
├─ /backup config
└─ /backup files "C:\Users\Jean\Documents"
```

---

## Mode `create`

```
📍 CRÉATION D'UN POINT DE RESTAURATION
═══════════════════════════════════════════════════════════════

Vérification de la protection système... ✅ Activée

Description (optionnelle): $ARGUMENTS
Si vide, utilisera: "Point de restauration manuel - YYYY-MM-DD HH:mm"

Espace requis estimé: ~500 MB - 2 GB
Espace disponible: 6.8 GB sur 15 GB alloués

⚠️ Si l'espace est insuffisant, le plus ancien point sera supprimé.

Créer le point de restauration? [O/N]
```

Après création:
```
✅ Point de restauration créé avec succès!

Détails:
├─ Date: 2026-02-03 10:45:23
├─ Description: "Avant installation pilote graphique"
├─ Numéro de séquence: 48
└─ Taille estimée: 1.2 GB

Commande pour restaurer:
rstrui.exe /restore:"48"
```

---

## Mode `list`

```
📋 POINTS DE RESTAURATION DISPONIBLES
═══════════════════════════════════════════════════════════════

┌─────┬────────────────────┬────────────────────────────────────┬───────────┐
│ Seq │ Date               │ Description                        │ Type      │
├─────┼────────────────────┼────────────────────────────────────┼───────────┤
│ 48  │ 2026-02-03 10:45   │ Avant installation pilote graphique│ Manuel    │
│ 47  │ 2026-02-01 14:30   │ Maintenance mensuelle              │ Manuel    │
│ 46  │ 2026-01-28 03:00   │ Windows Update                     │ Automatique│
│ 45  │ 2026-01-25 11:20   │ Installed 7-Zip 23.01              │ Installation│
│ 44  │ 2026-01-20 09:15   │ Installed Node.js                  │ Installation│
└─────┴────────────────────┴────────────────────────────────────┴───────────┘

Total: 5 points de restauration
Espace utilisé: 8.2 GB / 15 GB

Actions:
├─ Restaurer: /backup restore 47
└─ Supprimer anciens: /backup cleanup (garde les 3 derniers)
```

---

## Mode `restore`

```
🔄 ASSISTANT DE RESTAURATION
═══════════════════════════════════════════════════════════════

⚠️ ATTENTION: La restauration système va:
├─ Restaurer les fichiers système à l'état du point choisi
├─ Désinstaller les programmes installés après ce point
├─ Restaurer les paramètres système
├─ NE PAS affecter vos fichiers personnels (Documents, Images, etc.)
└─ Nécessiter un redémarrage

POINTS DISPONIBLES:
1. 2026-02-03 10:45 - Avant installation pilote graphique
2. 2026-02-01 14:30 - Maintenance mensuelle
3. 2026-01-28 03:00 - Windows Update
4. 2026-01-25 11:20 - Installed 7-Zip 23.01
5. 2026-01-20 09:15 - Installed Node.js

Sélectionner un point (1-5): _

Afficher les programmes affectés? [O/N]
```

Si affichage des programmes:
```
PROGRAMMES AFFECTÉS (point #2 - 2026-02-01):

Seront DÉSINSTALLÉS (installés après):
├─ Pilote graphique Intel 31.0.101.5122
└─ Mise à jour Chrome 122.0.6273

Seront RESTAURÉS (version précédente):
└─ Aucun

Confirmer la restauration? [O/N]
⚠️ Le système va redémarrer automatiquement.
```

---

## Mode `config`

```
⚙️ SAUVEGARDE DE LA CONFIGURATION SYSTÈME
═══════════════════════════════════════════════════════════════

Cette commande va sauvegarder:

CONFIGURATION RÉSEAU:
├─ Configuration IP de toutes les interfaces
├─ Table de routage
├─ Paramètres DNS
├─ Règles pare-feu
└─ Profils Wi-Fi (avec mot de passe si admin)

CONFIGURATION SYSTÈME:
├─ Variables d'environnement
├─ Services et leur configuration
├─ Tâches planifiées
├─ Stratégies de groupe appliquées
└─ Liste des pilotes installés

APPLICATIONS:
├─ Liste des programmes installés
├─ Programmes au démarrage
└─ Associations de fichiers

Destination: C:\Backups\ConfigBackup-YYYY-MM-DD\
Format: Fichiers texte + exports PowerShell

Lancer la sauvegarde? [O/N]
```

Après sauvegarde:
```
✅ Sauvegarde de configuration terminée!

Fichiers créés:
C:\Backups\ConfigBackup-2026-02-03\
├─ network-config.txt
├─ ip-config.txt
├─ firewall-rules.wfw
├─ wifi-profiles\
│   ├─ MonWifi.xml
│   └─ Bureau.xml
├─ services-list.csv
├─ scheduled-tasks.xml
├─ installed-apps.csv
├─ drivers-list.csv
├─ env-variables.txt
└─ restore-instructions.md

Taille totale: 2.4 MB

Pour restaurer, voir: restore-instructions.md
```

---

## Mode `files "chemin"`

```
📂 SAUVEGARDE DE FICHIERS
═══════════════════════════════════════════════════════════════

Source: C:\Users\Jean\Documents
Destination: [À spécifier]

OPTIONS DE DESTINATION:
1. Disque externe (E:\Backups\)
2. Partage réseau (\\serveur\backup\)
3. Dossier local (C:\Backups\)
4. Spécifier un chemin personnalisé

Choix: _

ANALYSE DE LA SOURCE:
├─ Fichiers: 12,456
├─ Dossiers: 234
├─ Taille totale: 18.5 GB
└─ Fichiers modifiés (7 jours): 156

OPTIONS DE SAUVEGARDE:
[ ] Sauvegarde complète (tous les fichiers)
[x] Sauvegarde incrémentielle (fichiers modifiés depuis dernière sauvegarde)
[ ] Sauvegarde miroir (synchronisation exacte)

[ ] Compresser (ZIP)
[ ] Exclure fichiers temporaires
[x] Conserver les permissions

Lancer la sauvegarde? [O/N]
```

---

## Mode `registry`

```
📋 EXPORT DU REGISTRE
═══════════════════════════════════════════════════════════════

⚠️ L'export complet du registre peut prendre plusieurs minutes
   et générer un fichier volumineux (plusieurs GB).

OPTIONS D'EXPORT:
1. Registre complet (HKLM + HKCU + autres)
2. HKLM uniquement (configuration système)
3. HKCU uniquement (configuration utilisateur)
4. Clé spécifique: _____

Choix: _

Format:
[x] .reg (réimportable via regedit)
[ ] .txt (lecture seule)

Destination: C:\Backups\Registry\

ESTIMATION:
├─ Registre complet: ~500 MB - 2 GB
├─ HKLM: ~300 MB - 1 GB
├─ HKCU: ~50 MB - 200 MB
└─ Durée estimée: 2-10 minutes

Lancer l'export? [O/N]
```

---

## Commandes de Référence

```powershell
# Créer un point de restauration
Checkpoint-Computer -Description "Ma description" -RestorePointType MODIFY_SETTINGS

# Lister les points
Get-ComputerRestorePoint | Select-Object SequenceNumber, CreationTime, Description

# Restaurer (nécessite redémarrage)
Restore-Computer -RestorePoint <SequenceNumber>

# Vérifier la protection système
Get-ComputerRestorePoint | Select-Object -First 1

# Activer la protection système
Enable-ComputerRestore -Drive "C:\"

# Configurer l'espace alloué
vssadmin resize shadowstorage /for=C: /on=C: /maxsize=15GB

# Export registre
reg export HKLM C:\backup\hklm.reg
reg export HKCU C:\backup\hkcu.reg

# Sauvegarde fichiers avec robocopy
robocopy "C:\Source" "D:\Backup" /MIR /R:3 /W:10 /LOG:backup.log

# Export configuration réseau
netsh wlan export profile folder=C:\backup key=clear
netsh advfirewall export C:\backup\firewall.wfw
```
