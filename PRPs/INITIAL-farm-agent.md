# Feature Request : Farm Agent — Agent IA Agricole Autonome Local

## Contexte

MultiPass Eco-Systemes est une plateforme pour producteurs locaux (Madeira, Congo, Wallonie). Le POC d'un assistant IA offline via llamafile (Qwen3-4B, 2.7 Go, interface web) a ete valide le 7 avril 2026 — reponse en 30-120 secondes sur CPU, multilingue (FR/PT/ES/NL/SW).

L'etape suivante est de transformer ce chatbot passif en un **agent autonome local** deploye sur du hardware low-cost (PC reconditionne i3 + petit GPU NVIDIA/AMD, ~300-350 EUR) pour chaque cooperative agricole.

## Le probleme

Les fermiers dans les pays en developpement (et meme en Wallonie rurale) n'ont pas :
- D'acces Internet fiable
- D'expert agricole a proximite
- D'outil de gestion adapte a leur realite
- De moyen de capitaliser sur leurs observations et savoirs locaux

Les solutions cloud (ChatGPT, Gemini) sont inaccessibles offline, couteuses, et les donnees partent aux USA.

## La solution : Farm Agent

Un agent IA local complet qui tourne sur un PC a 300 EUR, alimente par panneau solaire si necessaire, avec :

### 1. LLM local avec GPU offload
- Llamafile ou llama.cpp avec Qwen3-4B/7B en GGUF
- GPU offload via CUDA (NVIDIA) ou Vulkan (AMD) = 10-25 tokens/sec
- Interface web chat accessible via WiFi local (telephone, tablette)
- System prompt agricole specialise

### 2. Base de donnees PostgreSQL locale
- Tables : parcelles, recoltes, rotations, cooperateurs, finances, inventaire, journal
- L'agent peut query la DB pour des reponses personnalisees
- Historique de la ferme = memoire persistante

### 3. Vault Obsidian de connaissances agricoles
- Fiches cultures, maladies, traitements bio, recettes (compost, purins)
- Enrichi par le fermier + synchro depuis le reseau Eco-Systemes
- L'agent cherche dans le vault pour ses reponses

### 4. Boucle agent avec tool calling
- 6+ outils : query_database, search_vault, write_journal, check_sensors, calculate, notify
- Le fermier pose une question, l'agent combine LLM + DB + vault pour une reponse contextualisee
- Pattern identique a Claude Code mais en local (llama.cpp function calling)

### 5. Capteurs terrain via mesh LoRa (Meshtastic/Reticulum)
- Modules ESP32 + capteurs (humidite sol, temperature, niveau d'eau) a 25 EUR/piece
- Reseau mesh decentralise, zero infrastructure
- L'agent integre les donnees capteurs dans ses reponses

### 6. Synchronisation opportuniste
- Quand Internet dispo (1x/semaine, cybercafe, 4G ponctuel) :
  - Push observations vers Eco-Systemes (forum, marketplace)
  - Push donnees anonymisees vers la cooperative
  - Pull nouvelles fiches, prix marche, alertes sanitaires

## Hardware cible

### Config minimale (USB stick, 0 EUR d'infra)
- N'importe quel PC avec 4 Go RAM
- Llamafile CPU only, Qwen3-4B
- Pas de DB, pas de vault, juste le chat
- 30-120 sec/reponse

### Config recommandee (cooperative, ~350 EUR)
- i3-10100/12100 + 16 Go RAM + SSD 256 Go
- GPU : GTX 1650 (4 Go VRAM) ou RX 6600 (8 Go VRAM)
- PostgreSQL + Obsidian vault + boucle agent
- 5-15 sec/reponse
- WiFi local pour acces multi-utilisateurs

### Config solaire (zone sans electricite, ~500 EUR)
- Config recommandee + panneau solaire 100W + batterie 50Ah
- 6-8 heures d'autonomie/jour sous soleil tropical

## Marches cibles

1. **Wallonie F(2)** : 60 fermes WWOOF, Ferme des Arondes, Paysans-Artisans
2. **Congo** : Cooperatives cafe Kivu (SOPACDI), maraichage Kinshasa
3. **Madeira** : Producteurs banana, miel, peche, artisanat
4. **UNDP pitch 27 avril** : Demo agent + mesh LoRa

## Stack technique envisagee

- **LLM :** llamafile ou llama.cpp + Qwen3-4B/7B GGUF + CUDA/Vulkan
- **DB :** PostgreSQL (ou SQLite pour la version legere)
- **Vault :** Obsidian-compatible Markdown files
- **Agent loop :** TypeScript ou Python, inspire de la boucle Gemma Gem (5 fichiers TS decouples)
- **Capteurs :** ESP32 + Meshtastic/Reticulum
- **Interface :** Web UI llamafile built-in + interface custom React/Svelte optionnelle
- **Sync :** API REST vers Eco-Systemes quand Internet dispo
- **OS :** Linux (Debian/Ubuntu minimal) ou Windows

## Contraintes

- Budget : 100 EUR/mois max pour le dev (contrainte Mike)
- Hardware cible : PC reconditionnes, pas de serveurs
- Doit fonctionner 100% offline
- Multilingue : FR, PT, ES, NL, SW minimum
- Open source (Apache 2.0 ou MIT)
- Distribution virale : le setup doit etre copiable de cooperative en cooperative

## Documents de reference

- POC llamafile : `C:\Users\r2d2\Projects\farm-assistant\`
- Veille Korben : `Knowledge/References/2026-04-07_Veille-Korben-42j.md`
- Eco-Systemes : `http://108.61.198.204`
- LivestockAI (FarmSystem) : `C:\Users\r2d2\Projects\multipass-farmsystems\`
- Meshtastic : https://meshtastic.org/
- Reticulum : https://github.com/markqvist/Reticulum
- Gemma Gem agent loop : https://github.com/kessler/gemma-gem
- Llamafile : https://github.com/mozilla-ai/llamafile
- EuroLLM : https://huggingface.co/utter-project/EuroLLM-9B
- Promptfoo (test LLM) : https://promptfoo.dev
