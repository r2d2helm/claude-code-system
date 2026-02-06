# Gestion des Services Windows

Outil de diagnostic et gestion des services Windows.

## Mode d'Utilisation
```
/services                    → Liste les services problématiques
/services status NomService  → État détaillé d'un service
/services restart NomService → Redémarre un service (avec confirmation)
/services list critical      → Liste des services critiques
/services list all           → Liste complète des services
/services dependencies Nom   → Affiche les dépendances
```

Arguments: $ARGUMENTS

---

## Sans Arguments: Diagnostic des Services

### 1. Services en Anomalie
Lister tous les services avec StartType=Automatic mais Status=Stopped:
- Nom du service
- Nom d'affichage
- Compte d'exécution
- Dernière erreur si disponible

### 2. Services Critiques Windows
Vérifier l'état de ces services essentiels:

| Service | Nom Affiché | État Attendu |
|---------|-------------|--------------|
| wuauserv | Windows Update | Running |
| WinDefend | Windows Defender | Running |
| BITS | Background Intelligent Transfer | Running |
| Dnscache | DNS Client | Running |
| EventLog | Windows Event Log | Running |
| Schedule | Task Scheduler | Running |
| W32Time | Windows Time | Running |
| LanmanWorkstation | Workstation | Running |
| LanmanServer | Server | Running |
| Netlogon | Netlogon | Running (si domaine) |
| PlugPlay | Plug and Play | Running |
| Spooler | Print Spooler | Running (si impression) |

### 3. Services Récemment Échoués
Consulter les événements Service Control Manager (Event ID 7000-7045) des dernières 24h.

---

## Mode `status NomService`

Afficher pour le service demandé:
- Nom et description
- État actuel
- Type de démarrage
- Compte d'exécution
- PID du processus
- Chemin de l'exécutable
- Dépendances (services dont il dépend)
- Dépendants (services qui dépendent de lui)
- Paramètres de récupération (actions en cas d'échec)
- Derniers événements liés

---

## Mode `restart NomService`

⚠️ DEMANDER CONFIRMATION avant d'agir.

1. Vérifier que le service existe
2. Lister les services dépendants qui seront impactés
3. Afficher l'avertissement si service critique
4. Après confirmation:
   - Arrêter le service proprement
   - Attendre l'arrêt complet (timeout 30s)
   - Redémarrer le service
   - Vérifier le démarrage
   - Reporter le résultat

---

## Mode `dependencies NomService`

Créer un arbre de dépendances:
```
NomService
├─ Dépend de:
│  ├─ Service1 [Running]
│  └─ Service2 [Running]
└─ Requis par:
   ├─ Service3 [Running]
   └─ Service4 [Stopped]
```

---

## Commandes PowerShell de Référence

```powershell
# Lister services arrêtés qui devraient tourner
Get-Service | Where-Object {$_.StartType -eq 'Automatic' -and $_.Status -ne 'Running'}

# État détaillé
Get-Service -Name "ServiceName" | Select-Object *

# Dépendances
Get-Service -Name "ServiceName" | Select-Object -ExpandProperty DependentServices
Get-Service -Name "ServiceName" | Select-Object -ExpandProperty ServicesDependedOn

# Événements
Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Service Control Manager'} -MaxEvents 20
```
