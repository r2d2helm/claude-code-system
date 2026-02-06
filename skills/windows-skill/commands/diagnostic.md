# Diagnostic Système Complet

Effectue un diagnostic approfondi de cette machine Windows en analysant:

## 1. Informations Système
- Version Windows exacte et build
- Uptime du système
- Date de dernière mise à jour installée
- Informations matérielles (CPU, RAM totale)

## 2. Ressources et Performance
- Utilisation CPU actuelle et moyenne
- Utilisation RAM (utilisée/disponible)
- Espace disque sur tous les volumes (⚠️ alerter si < 15%)
- Processus les plus gourmands (top 5 CPU, top 5 RAM)

## 3. Services Windows
- Services critiques arrêtés qui devraient tourner (Automatic mais Stopped)
- Services en erreur
- État des services essentiels: Windows Update, Defender, BITS, DNS Client

## 4. Réseau
- Configuration IP de toutes les interfaces actives
- Test de connectivité Internet (ping + DNS)
- Passerelle par défaut accessible
- Serveurs DNS configurés et fonctionnels

## 5. Sécurité
- État de Windows Defender (protection temps réel)
- Date dernière mise à jour des signatures
- Date dernière analyse complète
- État du pare-feu Windows

## 6. Événements Critiques
- Erreurs système des dernières 24h
- Crashs d'applications récents
- Avertissements importants

## Format de Sortie

Utilise ce format pour chaque section:
```
📊 [NOM SECTION]
├─ Item 1: valeur [✅|⚠️|❌]
├─ Item 2: valeur [✅|⚠️|❌]
└─ Item 3: valeur [✅|⚠️|❌]
```

## Résumé Final

Termine par un résumé avec:
- Score de santé global (0-100%)
- Top 3 des problèmes à résoudre en priorité
- Recommandations d'actions

$ARGUMENTS
