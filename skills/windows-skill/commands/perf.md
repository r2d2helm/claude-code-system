# Analyse des Performances

Diagnostic approfondi des performances système.

## Mode d'Utilisation
```
/perf              → Analyse complète (défaut)
/perf cpu          → Focus sur le CPU
/perf memory       → Focus sur la mémoire
/perf disk         → Focus sur les disques
/perf process      → Analyse des processus
/perf realtime     → Monitoring temps réel (5 min)
/perf bottleneck   → Identification des goulots d'étranglement
```

Arguments: $ARGUMENTS

---

## Analyse Complète (défaut)

### 1. Vue d'Ensemble Instantanée
```
┌─────────────────────────────────────────────┐
│ CPU: ██████████░░░░░░░░░░ 52%              │
│ RAM: ████████████████░░░░ 78% (12.5/16 GB) │
│ Disk C: ██████████████░░░░ 68% utilisé     │
│ Disk D: ████░░░░░░░░░░░░░░ 22% utilisé     │
└─────────────────────────────────────────────┘
```

### 2. Processus Consommateurs
**Top 5 CPU:**
| Processus | PID | CPU % | Threads |
|-----------|-----|-------|---------|

**Top 5 RAM:**
| Processus | PID | RAM (MB) | Working Set |
|-----------|-----|----------|-------------|

**Top 5 I/O Disque:**
| Processus | PID | Read MB/s | Write MB/s |
|-----------|-----|-----------|------------|

### 3. Indicateurs Clés
- Temps processeur moyen (dernière minute)
- Mémoire disponible vs mémoire committée
- Longueur de la file d'attente disque
- Latence disque moyenne
- Interruptions/sec
- Context switches/sec

---

## Mode `cpu`

Analyse détaillée du processeur:
- Modèle et nombre de cœurs/threads
- Fréquence actuelle vs max
- Utilisation par cœur
- Processus utilisant le plus de CPU
- Temps en mode kernel vs user
- Historique sur 1 minute (échantillons 5s)

---

## Mode `memory`

Analyse détaillée de la mémoire:
- RAM physique totale/utilisée/disponible
- Mémoire committée et limite
- Cache système
- Pool paginé et non paginé
- Utilisation du fichier d'échange (pagefile)
- Working Set des processus
- Fuites mémoire potentielles (processus avec croissance anormale)

Alertes:
- ⚠️ si RAM disponible < 10%
- ⚠️ si pagefile très utilisé
- 🔴 si mémoire committée proche de la limite

---

## Mode `disk`

Analyse des performances disque:
- Pour chaque volume:
  - Type (SSD/HDD)
  - Espace total/utilisé/libre
  - Santé SMART si disponible
  - Temps de réponse moyen
  - Files d'attente
- Activité I/O actuelle
- Processus générant le plus d'I/O
- Fragmentation (HDD uniquement)

---

## Mode `process`

Analyse détaillée des processus:
- Nombre total de processus
- Processus avec haute priorité
- Processus consommant des ressources anormales
- Processus zombies ou en attente
- Handles et threads par processus
- Arbre de processus (parent-enfant)

---

## Mode `realtime`

Monitoring en temps réel pendant 5 minutes:
- Échantillonnage toutes les 10 secondes
- Affichage des tendances
- Détection des pics d'utilisation
- Identification des événements corrélés

À la fin, rapport avec:
- Valeurs min/max/moyenne
- Moments de pic
- Anomalies détectées

---

## Mode `bottleneck`

Identification des goulots d'étranglement:

1. **Test CPU-bound**: Le CPU est-il saturé?
2. **Test Memory-bound**: Manque de RAM? Pagination excessive?
3. **Test I/O-bound**: Disque trop sollicité?
4. **Test Network-bound**: Bande passante saturée?

Résultat:
```
🔍 Goulot d'étranglement principal: [DISK I/O]
   Raison: File d'attente disque > 2, latence 45ms
   Impact: Ralentissement général du système
   Solution: Considérer SSD ou réduire I/O des processus X, Y
```

---

## Recommandations Automatiques

Basées sur l'analyse, suggérer:
- Processus à arrêter ou limiter
- Paramètres à ajuster
- Upgrades matériels si nécessaire
- Optimisations Windows possibles
