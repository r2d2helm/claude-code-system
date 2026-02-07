# /guardian-fix

Auto-correction des problemes courants detectes dans le vault.

## Usage

```
/guardian-fix
```

## Actions automatiques

1. Suppression des notes vides
2. Normalisation status : `captured` -> `seedling`
3. Normalisation tags : majuscules -> minuscules
4. Rapport des corrections appliquees

## Script

```powershell
powershell.exe -ExecutionPolicy Bypass -File "C:\Users\r2d2\.claude\skills\vault-guardian-skill\scripts\Invoke-VaultGuardian.ps1" -Mode fix
```

## Securite

- Ne supprime JAMAIS de notes avec du contenu
- Ne modifie PAS les liens (risque de casse)
- Log toutes les modifications
