# /guardian-report

Genere un rapport de sante complet avec recommandations.

## Usage

```
/guardian-report
```

## Contenu du rapport

1. Score de sante global
2. Metriques detaillees (notes, liens, tags, orphelins)
3. Liste des problemes detectes
4. Recommandations priorisees
5. Comparaison avec le dernier rapport (si disponible)

## Script

```powershell
powershell.exe -ExecutionPolicy Bypass -File "C:\Users\r2d2\.claude\skills\vault-guardian-skill\scripts\Invoke-VaultGuardian.ps1" -Mode report
```
