---
name: cred-validate
description: Tester la connectivite d un ou tous les credentials
---

# /cred-validate - Valider les Credentials

## Comportement

1. **Determiner le scope** :
   - `/cred-validate beszel` : un seul credential
   - `/cred-validate all` : tous les credentials
   - `/cred-validate --category monitoring` : par categorie

2. **Pour chaque credential**, utiliser `Test-Credential.ps1` :
   ```
   powershell.exe -File scripts/Test-Credential.ps1 -Slug "{slug}"
   ```

3. **Methodes de test par auth_type** :
   - `password` (HTTP) : curl/Invoke-WebRequest vers l'URL, verifier HTTP 200/302
   - `password` (SSH) : `ssh -o BatchMode=yes -o ConnectTimeout=5 {user}@{host} echo ok`
   - `password` (DB) : `ssh {vm} "psql -U {user} -c 'SELECT 1'"` via SSH tunnel
   - `apikey` : requete API avec header Authorization
   - `token` (Telegram) : `https://api.telegram.org/bot{token}/getMe`
   - `ssh-key` : `ssh -o BatchMode=yes -o ConnectTimeout=5 {host} echo ok`

4. **Mettre a jour** le frontmatter : `last_validated` et `validation_status`

5. **Afficher** les resultats

## Format de sortie

```
# Validation Results

| Service | Slug | Auth Type | Result | Response Time |
|---------|------|-----------|--------|---------------|
| Beszel Hub | beszel | password | OK | 120ms |
| PostgreSQL | postgres-shared | password | OK | 85ms |
| ... | ... | ... | ... | ... |

## Summary
- Tested: X
- Passed: X
- Failed: X

## Failed Details
- {slug}: {error_message}
```
