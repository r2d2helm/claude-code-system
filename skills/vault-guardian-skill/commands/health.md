# /guardian-health

Effectue un diagnostic complet du vault Obsidian Knowledge.

## Usage

```
/guardian-health
/guardian-health --quick
```

## Actions

1. Scanner toutes les notes du vault
2. Verifier : frontmatter, liens, tags, status, fichiers vides
3. Calculer le score de sante (0-10)
4. Afficher rapport detaille

## Script

```powershell
powershell.exe -ExecutionPolicy Bypass -File "C:\Users\r2d2\.claude\skills\vault-guardian-skill\scripts\Invoke-VaultGuardian.ps1" -Mode health
```

## Quick mode

Pour un check rapide (notes vides + liens casses uniquement) :

```powershell
powershell.exe -ExecutionPolicy Bypass -File "C:\Users\r2d2\.claude\skills\vault-guardian-skill\scripts\Invoke-VaultGuardian.ps1" -Mode quick
```
