# IEC 81346 - Designation de Reference

> Reference extraite du skill QElectroTech - conventions de designation IEC 81346

## Prefixes de designation

| Prefixe | Signification | Exemple |
|---------|--------------|---------|
| `=` | Fonction | `=A1` (Alimentation principale) |
| `+` | Localisation | `+S1.G2` (Armoire 1, Rack 2) |
| `-` | Composant | `-K1` (Contacteur 1) |

## Convention de nommage des bornes

```
BlockName:TerminalNumber
```

Exemples : `X1:1`, `X1:2`, `X2:PE`

## Tags metadata qet_tb_generator

| Tag | Description |
|-----|-------------|
| `%p` | Plant / Installation |
| `%t` | Type de borne |
| `%h` | Hierarchie |
| `%n` | Numero de borne |
| `%b` | Nom du bornier (block) |
| `%r` | Reference croisee |
| `%z` | Zone |
| `%s` | Section |
