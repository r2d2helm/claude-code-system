> Partie avancee de [[ha]]. Commandes essentielles dans le fichier principal.

# /pve-ha - Haute Disponibilite (Avancee)

## Description
Wizard de configuration HA, best practices et recommandations production.

## Wizard : Configuration HA

```
/pve-wizard ha
```

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧙 WIZARD: CONFIGURATION HAUTE DISPONIBILITÉ                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Étape 1/5: VÉRIFICATION PRÉREQUIS                                           ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  ✅ Cluster configuré: production-cluster (3 nodes)                          ║
║  ✅ Quorum: 3/3 nodes online                                                 ║
║  ✅ Stockage partagé: ceph-pool, nfs-data détectés                           ║
║  ✅ Watchdog: actif sur tous les nodes                                       ║
║  ⚠️  IPMI fencing: non configuré                                             ║
║                                                                              ║
║  Configurer IPMI fencing maintenant?                                         ║
║    [1] Oui (recommandé production)                                           ║
║    [2] Non, continuer avec watchdog seul                                     ║
║  Choix:              > 2                                                     ║
║                                                                              ║
║  Étape 2/5: CRÉER GROUPES HA                                                 ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Nom du groupe:      > production                                            ║
║  Nodes (ordre priorité):                                                     ║
║    [x] pve01 - Priority: > 1                                                 ║
║    [x] pve02 - Priority: > 2                                                 ║
║    [x] pve03 - Priority: > 3                                                 ║
║  Restricted (VMs uniquement sur ces nodes): [y/N] > N                        ║
║  No failback (pas de retour auto): [y/N] > N                                 ║
║                                                                              ║
║  Créer un autre groupe? [y/N] > Y                                            ║
║                                                                              ║
║  Nom du groupe:      > database                                              ║
║  Nodes:                                                                      ║
║    [x] pve03 - Priority: > 1                                                 ║
║    [x] pve01 - Priority: > 2                                                 ║
║    [ ] pve02                                                                 ║
║  Restricted: [Y/n] > Y                                                       ║
║                                                                              ║
║  Étape 3/5: AJOUTER RESSOURCES HA                                            ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  VMs/CTs disponibles (stockage partagé):                                     ║
║    [ ] vm:100 - dc01-windows (pve01)                                         ║
║    [ ] vm:101 - dc02-windows (pve02)                                         ║
║    [x] vm:104 - db-postgres-master (pve03)     → Groupe: database            ║
║    [x] vm:105 - db-postgres-replica (pve01)    → Groupe: database            ║
║    [x] ct:1001 - proxy-nginx (pve01)           → Groupe: production          ║
║    [x] ct:1002 - monitoring (pve02)            → Groupe: production          ║
║                                                                              ║
║  Étape 4/5: AFFINITY RULES (PVE 9+)                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Créer règle anti-affinity pour DB master/replica?                           ║
║    [Y/n] > Y                                                                 ║
║  ➜ Règle: vm:104 et vm:105 sur nodes différents (strict)                     ║
║                                                                              ║
║  Étape 5/5: RÉSUMÉ ET ACTIVATION                                             ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Groupes créés:                                                              ║
║    - production: pve01(1), pve02(2), pve03(3)                                ║
║    - database: pve03(1), pve01(2) [restricted]                               ║
║                                                                              ║
║  Ressources HA:                                                              ║
║    - vm:104 → database                                                       ║
║    - vm:105 → database                                                       ║
║    - ct:1001 → production                                                    ║
║    - ct:1002 → production                                                    ║
║                                                                              ║
║  Règles:                                                                     ║
║    - db-separate: anti-affinity vm:104,vm:105 (strict)                       ║
║                                                                              ║
║  Activer la configuration? [Y/n] > Y                                         ║
║                                                                              ║
║  ✅ Groupe production créé                                                   ║
║  ✅ Groupe database créé                                                     ║
║  ✅ 4 ressources HA ajoutées                                                 ║
║  ✅ Règle anti-affinity créée                                                ║
║  ✅ Configuration HA active!                                                 ║
║                                                                              ║
║  💡 Conseil: Tester avec 'ha-manager status'                                 ║
║  💡 Conseil: Simuler failover en arrêtant un node                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Best Practices HA

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  📋 BEST PRACTICES HA 2025-2026                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  INFRASTRUCTURE                                                              ║
║  • Minimum 3 nodes pour quorum automatique                                   ║
║  • QDevice obligatoire si cluster 2 nodes                                    ║
║  • Stockage partagé (Ceph, NFS, iSCSI) pour toutes les VMs HA               ║
║  • Réseau dédié pour Corosync (VLAN isolé)                                  ║
║                                                                              ║
║  FENCING                                                                     ║
║  • IPMI/iLO/DRAC: Obligatoire en production                                  ║
║  • Watchdog: Toujours activer comme backup                                   ║
║  • Tester fencing régulièrement!                                             ║
║                                                                              ║
║  GROUPES                                                                     ║
║  • Créer groupes par type de workload                                        ║
║  • Priorités: distribuer charge                                              ║
║  • Restricted: pour VMs sensibles (licensing, GPU)                           ║
║                                                                              ║
║  AFFINITY RULES (PVE 9+)                                                     ║
║  • Anti-affinity: DB master/replica, DC1/DC2                                 ║
║  • strict=1: Uniquement si vraiment critique                                 ║
║  • Location rules: Pour préférences node                                     ║
║                                                                              ║
║  MAINTENANCE                                                                 ║
║  • Toujours activer mode maintenance avant travaux                           ║
║  • Tester failover régulièrement                                             ║
║  • Monitorer logs HA: journalctl -u pve-ha-crm                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Voir Aussi
- `/pve-cluster` - Gestion cluster Corosync
- `/pve-storage` - Stockage partagé
- `/pve-migrate` - Migration VMs
