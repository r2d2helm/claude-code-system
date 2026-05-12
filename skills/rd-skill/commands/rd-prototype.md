# /rd-prototype — Guide de prototypage rapide

Lance un prototypage rapide d'une technologie evaluee sur VM105 (r2d2-lab) ou en local.

## Usage

```
/rd-prototype {technologie}
/rd-prototype zclaw ESP32
/rd-prototype ollama qwen3-30b
/rd-prototype ros2 simulation
```

## Processus

### 1. Pre-requis
- Verifier que la technologie est dans le catalogue (score >= 4)
- Identifier les ressources necessaires (VM105, hardware, packages)
- Estimer le temps et le budget

### 2. Environnement
- **Software** : VM105 r2d2-lab (192.168.1.161, SSH r2d2helm)
- **Hardware** : ESP32/Arduino a commander si necessaire
- **Docker** : Containeriser le prototype si possible
- **Isolation** : Ne pas impacter les services de production (VM103, VM104)

### 3. Etapes de prototypage

1. **Setup** : installer les dependances, cloner le repo
2. **Hello World** : faire tourner l'exemple minimal
3. **Integration** : connecter au stack R2D2 (Telegram, MCP, API)
4. **Test** : valider le fonctionnement sur un cas d'usage reel
5. **Documenter** : noter les resultats, problemes, performances

### 4. Output
- Note vault : `Knowledge/References/YYYY-MM-DD_RD-Prototype-{Technologie}.md`
- Verdict : VIABLE / PROMETTEUR / ABANDONNE
- Si VIABLE : proposer integration dans le systeme principal

## Budget prototypage

| Categorie | Budget max |
|-----------|-----------|
| Hardware (ESP32, capteurs) | 50 EUR |
| Logiciel | 0 EUR (open source) |
| Cloud/API (tests) | 0 EUR (LiteLLM existant) |
| Impression 3D | A evaluer |
