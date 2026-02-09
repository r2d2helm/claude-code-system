# /pai-observability — Gestion dashboard observability

Gerer le dashboard d'observabilite PAI.

## Syntaxe

```
/pai-observability <action>
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `action` | `start`, `stop`, `status`, `restart`, `open` | `status` |

## Procedure

### status
1. Tester endpoint : `curl -s http://localhost:4000/ > /dev/null`
2. Verifier port : `ss -tlnp | grep 4000`
3. Afficher etat

### start
1. Verifier prerequis (Bun, node_modules installes)
2. Utiliser manage.sh :
   ```bash
   ~/.claude/observability/manage.sh start
   ```
3. Attendre 3s et verifier

### stop
```bash
~/.claude/observability/manage.sh stop
```

### restart
```bash
~/.claude/observability/manage.sh restart
```

### open
1. Verifier que le serveur tourne
2. Ouvrir dans le navigateur :
   ```bash
   xdg-open http://localhost:4000
   ```
