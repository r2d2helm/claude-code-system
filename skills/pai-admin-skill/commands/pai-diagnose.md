# /pai-diagnose — Suite de diagnostic automatique

Executer une suite complete de diagnostics PAI.

## Syntaxe

```
/pai-diagnose
```

## Procedure

1. **Systeme** :
   - `uname -a` (OS)
   - `lsb_release -d` (distribution)
   - Espace disque : `df -h ~`

2. **Prerequis** :
   - Bun : `which bun && bun --version`
   - Git : `which git`
   - mpg123 : `which mpg123`
   - notify-send : `which notify-send`
   - curl : `which curl`

3. **Installation PAI** :
   - settings.json existe et JSON valide
   - CORE skill present (skills/PAI/SKILL.md)
   - Hooks presents et comptes
   - MEMORY/ structure

4. **Configuration** :
   - PAI_DIR defini
   - contextFiles pointent vers fichiers existants
   - Hooks pointent vers fichiers existants
   - daidentity.name defini

5. **Services** :
   - Voice server : `curl -s http://localhost:8888/health`
   - Observability : `curl -s http://localhost:4000/`
   - Ports utilises : `ss -tlnp | grep -E "8888|4000"`

6. **Securite** :
   - SecurityValidator enregistre
   - .env permissions
   - Pas de secrets dans settings.json

7. Generer rapport :
   ```
   === PAI Diagnostic Report ===
   Date: 2026-02-09

   [OK] Systeme Ubuntu 24.04
   [OK] Bun 1.1.x
   [WARN] mpg123 absent
   [FAIL] PAI non installe
   ...

   Recommandations :
   1. Installer mpg123 : sudo apt install mpg123
   2. Installer PAI : /pai-install
   ```
