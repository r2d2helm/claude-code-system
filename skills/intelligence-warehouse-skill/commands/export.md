---
name: intel-export
description: Exporter vers R2D2 Agent
---

# /intel-export - Export vers R2D2 Agent

## Cible : $ARGUMENTS

Exporte des donnees du warehouse en JSON structure pour le bot Telegram R2D2 Agent.

## Actions

### Exporter une Opportunity Card

```
/intel-export opportunity <id>
```

1. Lire l'opportunity depuis SQLite
2. Recuperer les findings sources
3. Formater en JSON :

```json
{
  "type": "opportunity_card",
  "id": 7,
  "title": "Pack Migration VMware PME Wallonie",
  "category": "IT_Tech",
  "urgency": 4,
  "potential_value": "15-25k EUR par client",
  "pitch": "Les PME wallonnes utilisant VMware font face a des hausses de 300-500% suite au rachat Broadcom. Proxmox offre une alternative open source mature. Le cheque cybersecurite wallon couvre 75% des frais (jusqu'a 60k EUR).",
  "required_skills": ["proxmox-skill", "backup-skill", "security-skill"],
  "financial_levers": ["Cheque Cybersecurite Wallonie 75%"],
  "findings_count": 4,
  "status": "detected",
  "created_at": "2026-03-25",
  "expires_at": "2026-06-30"
}
```

4. Afficher le JSON et le copier dans le clipboard si possible

### Exporter un brief

```
/intel-export brief <id>
```

1. Lire le brief depuis la note vault correspondante
2. Formater en JSON resume :

```json
{
  "type": "intelligence_brief",
  "date": "2026-03-25",
  "period": "2026-03-18 - 2026-03-25",
  "findings_count": 18,
  "top_findings": [...],
  "active_opportunities": [...],
  "active_threats": [...],
  "recommendations": [...]
}
```

### Exporter les stats

```
/intel-export stats
```

Exporte le dashboard en JSON compact pour affichage bot.

## Integration R2D2 Agent

Le JSON exporte est concu pour etre consomme par :
- Le bot Telegram `@mpr2d2_bot` (container r2d2-bot, VM 105)
- Un eventuel endpoint API
- Le MCP server taskyn (pour tracking des actions)

## Format de sortie console

```
## Export genere

Type : opportunity_card
ID : OPP-7
Taille : 847 bytes

JSON :
{...}

Copie dans le clipboard : OK
```

## Exemples

```
/intel-export opportunity 7
/intel-export brief 2026-03-25
/intel-export stats
```
