# Analyse des Logs et Événements Windows

Exploration et diagnostic des journaux d'événements.

## Mode d'Utilisation
```
/logs                       → Résumé des événements importants (24h)
/logs errors                → Erreurs système et applications
/logs security              → Événements de sécurité
/logs boot                  → Problèmes de démarrage
/logs app NomApplication    → Logs d'une application spécifique
/logs search "terme"        → Recherche dans les logs
/logs export                → Exporter les logs en fichier
/logs clear                 → Archiver et nettoyer les logs anciens
```

Arguments: $ARGUMENTS

---

## Résumé (défaut)

```
📋 RÉSUMÉ DES ÉVÉNEMENTS (24 dernières heures)
═══════════════════════════════════════════════════════════════

VUE D'ENSEMBLE:
┌──────────────────┬─────────┬─────────┬─────────┬─────────┐
│ Journal          │ 🔴 Crit │ ❌ Err  │ ⚠️ Warn │ ℹ️ Info │
├──────────────────┼─────────┼─────────┼─────────┼─────────┤
│ System           │ 0       │ 3       │ 12      │ 245     │
│ Application      │ 0       │ 8       │ 25      │ 1,203   │
│ Security         │ 0       │ 0       │ 5       │ 892     │
│ Setup            │ 0       │ 0       │ 0       │ 2       │
└──────────────────┴─────────┴─────────┴─────────┴─────────┘

ÉVÉNEMENTS CRITIQUES RÉCENTS:
└─ Aucun événement critique ✅

TOP 5 DES ERREURS:
┌───────┬────────────────────────────────────┬───────┬──────────────┐
│ ID    │ Source                             │ Count │ Dernier      │
├───────┼────────────────────────────────────┼───────┼──────────────┤
│ 1000  │ Application Error                  │ 5     │ 08:45        │
│ 7023  │ Service Control Manager            │ 2     │ 06:00        │
│ 10016 │ DistributedCOM                     │ 4     │ 09:12        │
│ 36874 │ Schannel                           │ 2     │ 07:30        │
│ 6008  │ EventLog (arrêt imprévu)           │ 1     │ Hier 23:45   │
└───────┴────────────────────────────────────┴───────┴──────────────┘

⚠️ POINTS D'ATTENTION:
├─ 1 arrêt imprévu détecté hier
└─ 5 crashs d'application (voir /logs errors)

Actions suggérées: /logs errors | /logs app "Application Error"
```

---

## Mode `errors`

```
❌ ERREURS SYSTÈME ET APPLICATIONS
═══════════════════════════════════════════════════════════════

ERREURS SYSTÈME (7 derniers jours):
┌──────────────────────────────────────────────────────────────────┐
│ 🕐 2026-02-03 06:00:15 │ Event ID: 7023                         │
│ Source: Service Control Manager                                  │
│ Message: Le service Windows Search s'est terminé avec l'erreur   │
│          Le service n'a pas répondu à temps à la demande.        │
│ Impact: Recherche Windows indisponible temporairement            │
│ Occurrences: 2 fois cette semaine                                │
├──────────────────────────────────────────────────────────────────┤
│ 🕐 2026-02-02 23:45:32 │ Event ID: 6008                         │
│ Source: EventLog                                                 │
│ Message: L'arrêt système précédent était imprévu.                │
│ Impact: Possible perte de données non sauvegardées               │
│ Diagnostic: Vérifier alimentation/température                    │
├──────────────────────────────────────────────────────────────────┤
│ 🕐 2026-02-02 15:30:00 │ Event ID: 10016                        │
│ Source: DistributedCOM                                           │
│ Message: Permissions DCOM incorrectes pour {CLSID}               │
│ Impact: Généralement bénin, bug Windows connu                    │
│ Solution: Ignorable ou corriger via dcomcnfg                     │
└──────────────────────────────────────────────────────────────────┘

ERREURS APPLICATION:
┌──────────────────────────────────────────────────────────────────┐
│ 🕐 2026-02-03 08:45:12 │ Event ID: 1000                         │
│ Source: Application Error                                        │
│ Application: chrome.exe                                          │
│ Version: 122.0.6261.57                                          │
│ Module défaillant: ntdll.dll                                     │
│ Code exception: 0xc0000005 (Access Violation)                    │
│ Occurrences: 5 fois cette semaine                                │
│ Suggestion: Mettre à jour Chrome, vérifier extensions            │
└──────────────────────────────────────────────────────────────────┘

RÉSUMÉ PAR GRAVITÉ:
├─ Critiques: 0
├─ Erreurs: 11
└─ Nécessitant action: 2
```

---

## Mode `security`

```
🔐 ÉVÉNEMENTS DE SÉCURITÉ
═══════════════════════════════════════════════════════════════

CONNEXIONS (24h):
┌────────────────────────────────────────────────────────────────┐
│ ✅ CONNEXIONS RÉUSSIES: 45                                     │
├────────────────────────────────────────────────────────────────┤
│ Heure     │ Utilisateur    │ Type        │ Source            │
├───────────┼────────────────┼─────────────┼───────────────────┤
│ 09:15:32  │ Jean.Dupont    │ Interactive │ Console           │
│ 09:00:00  │ SYSTEM         │ Service     │ Localhost         │
│ 08:45:21  │ Jean.Dupont    │ Unlock      │ Console           │
│ ...       │                │             │                   │
└───────────┴────────────────┴─────────────┴───────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ ❌ CONNEXIONS ÉCHOUÉES: 3 ⚠️                                   │
├────────────────────────────────────────────────────────────────┤
│ Heure     │ Utilisateur    │ Raison                │ IP       │
├───────────┼────────────────┼───────────────────────┼──────────┤
│ 03:45:12  │ admin          │ Mot de passe incorrect│ Localhost│
│ 03:44:55  │ administrator  │ Compte désactivé      │ Localhost│
│ 03:44:30  │ root           │ Utilisateur inconnu   │ Localhost│
└───────────┴────────────────┴───────────────────────┴──────────┘

⚠️ ALERTE: Tentatives de connexion suspectes à 03:44-03:45
   Pattern: Tentatives sur comptes admin par défaut
   Recommandation: Vérifier l'origine, renforcer les accès

MODIFICATIONS DE COMPTES:
├─ Aucune modification de compte détectée ✅

ÉVÉNEMENTS D'AUDIT:
├─ Changements de politique: 0
├─ Modifications de groupe: 0
└─ Accès objets sensibles: 12 (normal)

RÉSUMÉ SÉCURITÉ:
├─ Score: 85/100
└─ Alertes actives: 1 (tentatives de connexion)
```

---

## Mode `boot`

```
🚀 DIAGNOSTIC DE DÉMARRAGE
═══════════════════════════════════════════════════════════════

DERNIERS DÉMARRAGES:
┌──────────────────┬──────────────┬─────────────────────────────┐
│ Date             │ Durée Boot   │ Statut                      │
├──────────────────┼──────────────┼─────────────────────────────┤
│ 2026-02-03 09:00 │ 45 sec       │ ✅ Normal                   │
│ 2026-02-02 08:30 │ 48 sec       │ ✅ Normal                   │
│ 2026-02-01 09:15 │ 52 sec       │ ✅ Normal                   │
│ 2026-01-31 07:45 │ 2 min 15 sec │ ⚠️ Lent (vérification chkdsk)│
│ 2026-01-30 08:00 │ 47 sec       │ ✅ Normal                   │
└──────────────────┴──────────────┴─────────────────────────────┘

DERNIER ARRÊT:
├─ Type: ✅ Arrêt propre (shutdown)
├─ Date: 2026-02-02 23:30
└─ Initiateur: Utilisateur

ARRÊT IMPRÉVU DÉTECTÉ:
┌────────────────────────────────────────────────────────────────┐
│ 🕐 2026-02-02 23:45 - Arrêt imprévu                            │
│ Cause probable: Coupure de courant ou BSOD                     │
│ Diagnostic: Aucun dump mémoire trouvé                          │
│ Recommandation: Vérifier onduleur/alimentation                 │
└────────────────────────────────────────────────────────────────┘

ERREURS AU DÉMARRAGE (dernière semaine):
├─ Services en échec au démarrage: 1
│  └─ Windows Search (récupéré après délai)
├─ Pilotes en erreur: 0
└─ Applications au démarrage en échec: 0

TEMPS DE DÉMARRAGE MOYEN: 48 secondes
├─ Temps BIOS/UEFI: ~8 sec
├─ Temps noyau Windows: ~15 sec
└─ Temps services/applications: ~25 sec

PROGRAMMES AU DÉMARRAGE IMPACTANT:
├─ Microsoft OneDrive: +3 sec
├─ Antivirus tiers (si présent): +5 sec
└─ Applications startup: +8 sec total
```

---

## Mode `app NomApplication`

```
📱 LOGS APPLICATION: Chrome
═══════════════════════════════════════════════════════════════

Recherche dans: Application, System
Application: *chrome*

ÉVÉNEMENTS TROUVÉS (30 derniers jours):
┌──────────────────┬──────────┬───────────────────────────────────┐
│ Date             │ Type     │ Message                           │
├──────────────────┼──────────┼───────────────────────────────────┤
│ 2026-02-03 08:45 │ ❌ Error │ Application Error - chrome.exe    │
│                  │          │ Exception: 0xc0000005             │
│ 2026-02-02 14:30 │ ❌ Error │ Application Error - chrome.exe    │
│ 2026-02-01 09:15 │ ⚠️ Warn  │ Chrome update available           │
│ 2026-01-28 11:00 │ ℹ️ Info  │ Chrome installed successfully     │
└──────────────────┴──────────┴───────────────────────────────────┘

ANALYSE:
├─ Crashs cette semaine: 5
├─ Tendance: En augmentation ⚠️
├─ Module commun: ntdll.dll
└─ Cause probable: Extension défectueuse ou profil corrompu

SUGGESTIONS:
1. Désactiver les extensions une par une
2. Créer un nouveau profil Chrome
3. Réinstaller Chrome si persistant
```

---

## Mode `search "terme"`

```
🔍 RECHERCHE: "erreur"
═══════════════════════════════════════════════════════════════

Recherche dans tous les journaux (7 derniers jours)...
Résultats: 47 événements trouvés

[1] System - Event 7023 - 2026-02-03 06:00
    "Le service... s'est terminé avec l'erreur..."

[2] Application - Event 1000 - 2026-02-03 08:45
    "Nom de l'application défaillante: erreur application..."

[3] Application - Event 1001 - 2026-02-02 15:30
    "Rapport d'erreur Windows..."

... (44 autres résultats)

Afficher plus? [O/N] | Filtrer par journal? [System/Application/Security]
```

---

## Mode `export`

```
📤 EXPORT DES LOGS
═══════════════════════════════════════════════════════════════

Options d'export:
1. Dernières 24h - Tous les journaux
2. Derniers 7 jours - Erreurs uniquement
3. Dernier mois - Événements de sécurité
4. Personnalisé

Format:
[ ] CSV (tableur)
[x] EVTX (natif Windows)
[ ] HTML (rapport lisible)
[ ] JSON (traitement automatisé)

Destination: C:\Logs\ClaudeAdmin\exports\

Exporter? [O/N]
```

---

## Commandes de Référence

```powershell
# Erreurs système 24h
Get-WinEvent -FilterHashtable @{LogName='System'; Level=2; StartTime=(Get-Date).AddDays(-1)} -MaxEvents 50

# Erreurs application
Get-WinEvent -FilterHashtable @{LogName='Application'; Level=2} -MaxEvents 50

# Connexions réussies/échouées
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624,4625} -MaxEvents 100

# Événements de démarrage
Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Microsoft-Windows-Kernel-Boot'}

# Recherche texte
Get-WinEvent -LogName Application | Where-Object {$_.Message -like "*erreur*"} | Select-Object -First 20

# Export
wevtutil epl System C:\export\system.evtx
```
