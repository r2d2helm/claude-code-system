# Audit de Sécurité Windows

Analyse complète de la posture de sécurité du système.

## Mode d'Utilisation
```
/security                 → Audit standard
/security quick           → Vérifications essentielles uniquement
/security deep            → Audit approfondi
/security defender        → Focus Windows Defender
/security firewall        → Focus Pare-feu
/security accounts        → Focus Comptes utilisateurs
/security network         → Audit sécurité réseau
/security report          → Générer un rapport complet
```

Arguments: $ARGUMENTS

---

## Audit Standard (défaut)

### 1. Windows Defender
```
🛡️ WINDOWS DEFENDER
├─ Protection temps réel: ✅ Activée / ❌ Désactivée
├─ Signatures antivirus: YYYY-MM-DD (⚠️ si > 3 jours)
├─ Dernière analyse rapide: YYYY-MM-DD
├─ Dernière analyse complète: YYYY-MM-DD (⚠️ si > 30 jours)
├─ Protection cloud: ✅/❌
├─ Soumission échantillons: ✅/❌
└─ Menaces détectées: X (détail si > 0)
```

### 2. Pare-feu Windows
```
🔥 PARE-FEU WINDOWS
├─ Profil actif: Domain/Private/Public
├─ État:
│  ├─ Domain: ✅ Activé / ❌ Désactivé
│  ├─ Private: ✅ Activé / ❌ Désactivé
│  └─ Public: ✅ Activé / ❌ Désactivé
├─ Règles entrantes actives: XXX
└─ Ports ouverts suspects: [liste]
```

### 3. Comptes Utilisateurs
```
👤 COMPTES UTILISATEURS
├─ Comptes administrateurs locaux: X
│  └─ [liste des comptes admin]
├─ Compte Administrateur intégré: ✅ Désactivé / ⚠️ Activé
├─ Compte Invité: ✅ Désactivé / ⚠️ Activé
├─ Comptes sans mot de passe: X (⚠️ si > 0)
└─ Dernière connexion par compte
```

### 4. Mises à Jour
```
🔄 MISES À JOUR WINDOWS
├─ Dernière vérification: YYYY-MM-DD
├─ Dernière installation: YYYY-MM-DD
├─ Mises à jour en attente: X
│  └─ Dont critiques: X (🔴 si > 0)
└─ Redémarrage requis: Oui/Non
```

### 5. Configuration de Sécurité
```
⚙️ CONFIGURATION
├─ UAC (User Account Control): ✅ Activé (niveau X/4)
├─ BitLocker: ✅ Activé / ❌ Non configuré
├─ Secure Boot: ✅ Activé / ❌ Désactivé
├─ Credential Guard: ✅/❌
└─ Windows Hello: Configuré/Non configuré
```

### 6. Connexions Récentes
```
🔐 ACTIVITÉ DE CONNEXION (24h)
├─ Connexions réussies: X
├─ Connexions échouées: X (⚠️ si > 10)
└─ Comptes avec échecs multiples: [liste]
```

---

## Mode Deep (Approfondi)

Tout ce qui est dans Standard, plus:

### 7. Programmes au Démarrage
Analyser et signaler les entrées suspectes dans:
- HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
- HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
- Dossiers Startup
- Tâches planifiées au démarrage

### 8. Services Suspects
- Services avec chemin d'exécution inhabituel
- Services non signés
- Services récemment ajoutés

### 9. Ports et Connexions
- Ports en écoute non standard
- Connexions sortantes suspectes
- Processus avec connexions réseau

### 10. Intégrité des Fichiers Système
- Vérification rapide avec `sfc /verifyonly`
- Fichiers système modifiés récemment

### 11. Certificats
- Certificats root inhabituels
- Certificats expirés

### 12. Politiques de Sécurité
- Politique de mot de passe
- Politique de verrouillage de compte
- Audit des événements activé

---

## Mode Defender

Focus détaillé sur Windows Defender:
- État complet de toutes les protections
- Exclusions configurées (signaler si sensible)
- Historique des détections
- Quarantaine
- Configuration ASR (Attack Surface Reduction)
- État du bac à sable

### Actions Suggérées
- Lancer une analyse rapide si > 7 jours
- Mettre à jour les signatures si obsolètes
- Recommandations d'activation des protections

---

## Mode Firewall

Focus détaillé sur le pare-feu:
- État de chaque profil
- Règles entrantes par port/application
- Règles sortantes
- Règles personnalisées vs par défaut
- Règles potentiellement risquées (Any/Any)
- Logs du pare-feu (si activés)

### Ports Surveillés
| Port | Service | État | Risque |
|------|---------|------|--------|
| 3389 | RDP | Ouvert/Fermé | Élevé si ouvert au public |
| 22 | SSH | Ouvert/Fermé | Modéré |
| 445 | SMB | Ouvert/Fermé | Élevé si externe |
| 135 | RPC | Ouvert/Fermé | Élevé |

---

## Mode Accounts

Focus sur les comptes:
- Liste complète des utilisateurs locaux
- Groupes et appartenances
- Comptes de service
- Historique des changements de mot de passe
- Stratégie de mot de passe locale
- Sessions actives

---

## Score de Sécurité

À la fin de chaque audit, calculer un score:

```
📊 SCORE DE SÉCURITÉ: XX/100

Composants:
├─ Antivirus: XX/20
├─ Pare-feu: XX/20
├─ Mises à jour: XX/20
├─ Comptes: XX/20
└─ Configuration: XX/20

Priorités:
1. 🔴 [Action critique]
2. 🟠 [Action importante]
3. 🟡 [Amélioration suggérée]
```

---

## Mode Report

Génère un rapport HTML complet exportable:
- Toutes les sections de l'audit deep
- Graphiques visuels
- Historique si disponible
- Recommandations détaillées
- Format imprimable

Fichier: `C:\Logs\ClaudeAdmin\SecurityReport-YYYY-MM-DD.html`
