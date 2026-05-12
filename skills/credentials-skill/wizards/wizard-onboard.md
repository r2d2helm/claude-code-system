---
name: wizard-onboard
description: Onboarding d un nouveau service avec decouverte et enregistrement des credentials
---

# Wizard Onboard - Nouveau Service

## Questions

1. **Service** : Quel service ajouter au registre ?
   - Nom du service
   - VM ou machine hote
   - Type (container Docker, service systemd, application web, base de donnees)

2. **Decouverte** : Scanner la VM pour trouver les credentials automatiquement ?
   - Oui (via SSH + grep .env + docker inspect)
   - Non (saisie manuelle)

3. **Rotation** : Configurer la rotation automatique ?
   - Oui, interval personnalise
   - Oui, interval par defaut (90 jours)
   - Non, pas de rotation

## Processus

### Etape 1 : Decouverte
Si decouverte auto :
1. SSH vers la VM cible
2. Localiser les fichiers de configuration du service
3. Extraire les credentials trouves (.env, docker-compose, config files)
4. Presenter les resultats pour validation

### Etape 2 : Collecte
Pour chaque credential identifie :
1. Confirmer le service name et slug
2. Determiner la category et auth_type
3. Renseigner host, port, protocol
4. Saisir ou confirmer username/password
5. Definir la criticality
6. Ajouter le compose path et rotation notes

### Etape 3 : Creation
1. Creer `data/registry/{slug}.md` via `/cred-add`
2. Mettre a jour l'index

### Etape 4 : Validation
1. Tester la connexion via `/cred-validate {slug}`
2. Si OK : marquer validation_status = ok
3. Si FAIL : diagnostiquer et corriger

### Etape 5 : Scheduling
1. Ajouter au calendrier de rotation
2. Definir les alertes

## Format de sortie

```
# Onboard Complete : {service}

## Credentials enregistres
| Slug | Auth Type | Validated | Rotation |
|------|-----------|-----------|----------|
| {slug} | password | OK | 90 days |

## Fichiers crees
- data/registry/{slug}.md

## Prochaine rotation
- {date}
```
