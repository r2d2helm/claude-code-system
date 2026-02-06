# Diagnostic Réseau Avancé

Analyse complète de la configuration et de la connectivité réseau.

## Niveau d'Analyse
- `basic` : Configuration IP et test de connectivité
- `standard` : + DNS, ports, routes (par défaut)
- `deep` : + Analyse du trafic, latence, qualité de connexion

Niveau demandé: $ARGUMENTS (défaut: standard)

---

## 1. Configuration des Interfaces
Pour chaque interface réseau active:
- Nom et type (Ethernet, Wi-Fi, VPN)
- Adresse IP, masque, passerelle
- Serveurs DNS configurés
- État DHCP (activé/statique)
- Adresse MAC
- Vitesse de liaison

## 2. Tests de Connectivité
```
Test              | Cible              | Résultat
------------------|--------------------|---------
Passerelle        | Default Gateway    | ✅/❌ + latence
DNS interne       | DNS primaire       | ✅/❌ + latence
DNS externe       | 8.8.8.8, 1.1.1.1   | ✅/❌ + latence
Internet HTTP     | google.com:80      | ✅/❌ + latence
Internet HTTPS    | google.com:443     | ✅/❌ + latence
```

## 3. Résolution DNS
- Test de résolution sur plusieurs domaines
- Temps de réponse DNS
- Vérification cache DNS local
- Comparaison DNS configuré vs DNS publics

## 4. Table de Routage
- Routes actives
- Route par défaut
- Routes persistantes
- Détection de routes conflictuelles

## 5. Ports et Connexions (niveau standard+)
- Ports en écoute (LISTENING)
- Connexions établies (ESTABLISHED) 
- Processus associés à chaque port
- Ports suspects ou non standards

## 6. Analyse Avancée (niveau deep)
- Traceroute vers destinations clés
- Test de bande passante estimée
- Détection de perte de paquets
- Analyse de la latence sur 10 pings
- Vérification MTU

## 7. Pare-feu Windows
- Profil actif (Domain/Private/Public)
- Règles entrantes actives
- Ports bloqués potentiellement problématiques

## Problèmes Détectés

Liste les problèmes trouvés avec:
- Gravité (🔴 Critique | 🟠 Important | 🟡 Mineur)
- Description du problème
- Cause probable
- Solution recommandée

## Commandes Utiles

Fournis les commandes PowerShell pour:
- Renouveler l'IP DHCP
- Vider le cache DNS
- Réinitialiser la stack TCP/IP (si problème grave)
