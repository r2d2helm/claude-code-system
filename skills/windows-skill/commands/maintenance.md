# Maintenance Système Windows

Routine de maintenance préventive et corrective.

## Mode d'Utilisation
```
/maintenance              → Maintenance standard avec confirmation
/maintenance quick        → Maintenance rapide (nettoyage seulement)
/maintenance full         → Maintenance complète (tout)
/maintenance check        → Vérification seulement, aucune modification
/maintenance scheduled    → Créer une tâche planifiée de maintenance
```

Arguments: $ARGUMENTS

---

## ⚠️ RÈGLE IMPORTANTE
TOUJOURS demander confirmation avant chaque étape qui modifie le système.
Afficher ce qui sera fait AVANT de le faire.

---

## Maintenance Standard (défaut)

### Étape 1: Point de Restauration
```
📍 Création d'un point de restauration...
   Nom: "Maintenance-YYYY-MM-DD-HHmm"
```
Confirmer avant de continuer.

### Étape 2: Nettoyage des Fichiers Temporaires

Fichiers à nettoyer (afficher la taille récupérable):
- `%TEMP%` (fichiers > 7 jours)
- `C:\Windows\Temp` (fichiers > 7 jours)
- Cache navigateurs (Chrome, Edge, Firefox)
- Corbeille
- Fichiers de crash dumps anciens
- Logs anciens Windows (> 30 jours)

```
🧹 Espace récupérable estimé: X.XX GB
   Continuer avec le nettoyage? [O/N]
```

### Étape 3: Nettoyage Windows Update

```
🔄 Nettoyage du cache Windows Update...
   - Arrêt du service wuauserv
   - Suppression de SoftwareDistribution\Download
   - Redémarrage du service
```

### Étape 4: Vérification de l'Intégrité

```
🔍 Vérification des fichiers système (sfc /scannow)...
   ⏱️ Durée estimée: 10-15 minutes
```

Reporter les résultats:
- Aucune violation trouvée ✅
- Violations réparées ✅
- Violations non réparables ⚠️ (suggérer DISM)

### Étape 5: Optimisation des Disques

Pour SSD: `Optimize-Volume -DriveLetter C -ReTrim`
Pour HDD: `Optimize-Volume -DriveLetter C -Defrag`

### Étape 6: Rapport Final

```
📊 RAPPORT DE MAINTENANCE
═══════════════════════════════════════
Date: YYYY-MM-DD HH:mm
Durée totale: XX minutes

✅ Point de restauration créé
✅ Espace libéré: X.XX GB  
✅ Fichiers système: OK
✅ Disques optimisés

Prochaine maintenance recommandée: dans 30 jours
```

---

## Maintenance Quick

Uniquement:
1. Nettoyage fichiers temporaires utilisateur
2. Vidage corbeille
3. Nettoyage cache navigateurs

Pas de point de restauration, pas de vérification système.

---

## Maintenance Full

Tout ce qui est dans Standard, plus:

### Étape supplémentaire: DISM
```
🔧 Réparation de l'image Windows (DISM)...
   DISM /Online /Cleanup-Image /RestoreHealth
   ⏱️ Durée estimée: 15-30 minutes
```

### Étape supplémentaire: Vérification du Disque
```
💾 Planification de chkdsk au prochain redémarrage...
   Le système vérifiera le disque C: lors du prochain démarrage.
```

### Étape supplémentaire: Nettoyage Avancé
- Anciens profils utilisateurs inutilisés (> 90 jours)
- Installeurs obsolètes dans Windows\Installer
- Caches d'applications diverses
- Nettoyage des logs événements anciens

### Étape supplémentaire: Mises à Jour
```
🔄 Recherche de mises à jour Windows...
   X mise(s) à jour disponible(s)
   Installer maintenant? [O/N]
```

---

## Mode Check (Lecture Seule)

Exécute toutes les vérifications SANS aucune modification:
- Calcul de l'espace récupérable
- Scan SFC en mode vérification
- État des disques
- Mises à jour disponibles
- Santé générale

Génère un rapport avec les actions recommandées.

---

## Mode Scheduled

Crée une tâche planifiée pour la maintenance automatique:

```
📅 Configuration de la maintenance planifiée

Fréquence: [Hebdomadaire/Mensuel]
Jour: [Dimanche]
Heure: [03:00]
Type: [Quick/Standard]

La tâche exécutera automatiquement la maintenance.
Les logs seront enregistrés dans C:\Logs\ClaudeAdmin\maintenance\
```

Script PowerShell généré et enregistré dans `C:\Scripts\MaintenanceAuto.ps1`

---

## Commandes de Référence

```powershell
# Point de restauration
Checkpoint-Computer -Description "Maintenance" -RestorePointType MODIFY_SETTINGS

# Nettoyage disque silencieux
cleanmgr /d C /VERYLOWDISK /AUTOCLEAN

# SFC
sfc /scannow

# DISM
DISM /Online /Cleanup-Image /RestoreHealth

# Optimisation SSD
Optimize-Volume -DriveLetter C -ReTrim -Verbose

# Taille d'un dossier
(Get-ChildItem -Path $env:TEMP -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
```
