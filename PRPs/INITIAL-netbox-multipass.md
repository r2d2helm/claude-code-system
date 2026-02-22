## FEATURE:

Intégration de NetBox comme composant infrastructure dans le stack MultiPass Agency.

NetBox (v4.5.2) sera déployé comme 15ème container Docker sur la VM Proxmox (VMID 100, 192.168.1.161) pour servir de **source de vérité unique** de l'infrastructure réseau et des déploiements clients.

### Objectifs principaux :
1. **Déployer NetBox** en container Docker (netbox-docker) intégré au docker-compose existant de MultiPass
2. **Modéliser l'infrastructure actuelle** : VM Proxmox, 14 containers, plan IP 192.168.1.x, services/ports
3. **Exposer l'API via Kong** : Proxy NetBox REST API à travers Kong API Gateway pour les agents IA
4. **Connecter l'Agent Technique** : Créer un LangChain tool NetBox pour que l'agent technique puisse interroger/modifier l'infra
5. **Multi-tenancy** : Configurer les Tenants NetBox pour isoler l'infra de chaque client Enterprise
6. **Dashboard Analytics** : Alimenter l'Agent Analytics avec les données infra NetBox
7. **Webhooks automation** : Connecter les EventRules NetBox aux pipelines d'événements MultiPass

### Phases d'implémentation :
- **Phase 1** : Déploiement NetBox + modélisation infra existante
- **Phase 2** : Intégration API (Kong + LangChain tool pour agents)
- **Phase 3** : Multi-tenancy clients Enterprise
- **Phase 4** : Analytics infra + webhooks + automation

## CONTEXTE EXISTANT:

### Stack MultiPass actuel (14 containers Docker) :
- Next.js frontend (:3000)
- Supabase Studio (:3001)
- Langfuse observabilité (:3002)
- LiteLLM proxy (:4000)
- Kong API Gateway (:8000, :8443)
- PostgreSQL 16 avec pgvector (:5432)
- Redis 7 (:6379)
- 6 services Supabase internes (auth, storage, realtime, etc.)

### Infrastructure :
- **VM** : r2d2automaker (VMID 100) sur Proxmox, Ubuntu 24.04.3 LTS
- **IP** : 192.168.1.161
- **RAM** : ~5.9 GB / 60.5 GB (9.7% utilisé)
- **Docker Compose** : Orchestration existante

### Architecture agents MultiPass :
```
🐙 Orchestrateur
    ├── 💼 Agent Commercial
    ├── 🔧 Agent Technique (→ Ubuntu SysAdmin, Docker Manager, Database Admin, GitHub Ops, Voice/API)
    ├── 🎓 Agent Formation
    ├── 📞 Agent Support
    └── 📊 Agent Analytics
```

### Technologies pertinentes :
- LangChain / LangGraph (orchestration agents)
- FastAPI (backend agents autonomes)
- Kong API Gateway (routing, rate limiting)
- Langfuse (observabilité LLM)

### Notes vault à consulter :
- [[MultiPass]] - Documentation projet
- [[C_MultiPass-Stack]] - Architecture technique
- [[MULTIPASS-RECAP]] - Récapitulatif UI/UX
- Dossier : `Knowledge/Projets/MultiPass/`

### Repo NetBox cloné :
- `C:\Users\r2d2\Documents\Repos\netbox\` - Code source NetBox v4.5.2

## DOCUMENTATION:

### NetBox :
- Documentation officielle : https://docs.netbox.dev/en/stable/
- NetBox Docker : https://github.com/netbox-community/netbox-docker
- REST API : https://docs.netbox.dev/en/stable/integrations/rest-api/
- GraphQL API : https://docs.netbox.dev/en/stable/integrations/graphql-api/
- Plugin development : https://docs.netbox.dev/en/stable/plugins/
- Webhooks : https://docs.netbox.dev/en/stable/integrations/webhooks/
- Data model : https://docs.netbox.dev/en/stable/models/

### NetBox Docker compose reference :
- PostgreSQL 16 (peut partager l'instance existante ou dédié)
- Redis (peut partager l'instance existante ou dédié)
- Gunicorn (WSGI server)
- RQ Worker (background tasks)
- Nginx (optionnel si Kong fait le proxy)

### Intégration LangChain :
- LangChain custom tools : https://python.langchain.com/docs/how_to/custom_tools/
- API REST NetBox comme tool source

## CONSIDERATIONS:

### Infrastructure :
- **PostgreSQL** : Décider si NetBox utilise l'instance PostgreSQL existante (port 5432) ou une instance dédiée. Recommandation : instance dédiée pour isolation des données.
- **Redis** : Même question. NetBox a besoin de 2 DBs Redis (tasks + cache). Peut partager le Redis existant avec des DB numbers différents (ex: DB 2 et DB 3).
- **RAM** : NetBox + worker + PostgreSQL dédié ≈ 1-2 GB supplémentaires. Largement dans le budget (54 GB libres).
- **Ports** : Allouer un port pour NetBox UI (ex: :8080) et exposer via Kong.

### Sécurité :
- **API Token v2** : Configurer API_TOKEN_PEPPERS pour les tokens sécurisés
- **LOGIN_REQUIRED** : Activer (défaut) - pas d'accès anonyme
- **Kong** : Rate limiting sur les endpoints NetBox API
- **CORS** : Configurer pour permettre les appels depuis le frontend MultiPass

### Réseau :
- NetBox doit être dans le même réseau Docker que les autres services
- Kong route `/api/netbox/*` vers le container NetBox
- Les agents accèdent via Kong (pas directement)

### Migration :
- Inventaire initial de l'infra à faire manuellement ou via script
- Utiliser l'API bulk import de NetBox pour les données existantes
- Documenter les 14 containers, leurs ports, IPs, rôles

### Compatibilité :
- NetBox requiert Python 3.12+ (dans le container, pas sur l'hôte)
- PostgreSQL 13+ (on a 16, OK)
- Redis 6+ (on a 7, OK)

### Risques :
- Complexité accrue du docker-compose (5+ containers supplémentaires)
- Maintenance NetBox (mises à jour, migrations DB)
- Courbe d'apprentissage pour l'équipe
- Dépendance à un outil supplémentaire dans le stack
