# /pai-verify-observability — Verifier observability dashboard

Verifier le dashboard d'observabilite PAI.

## Syntaxe

```
/pai-verify-observability
```

## Procedure

1. Verifier repertoire : `ls ~/.claude/observability/`
2. Verifier manage.sh : `ls ~/.claude/observability/manage.sh`
3. Verifier apps/server/ : `ls ~/.claude/observability/apps/server/`
4. Verifier apps/client/ : `ls ~/.claude/observability/apps/client/`
5. Verifier dependances server : `ls ~/.claude/observability/apps/server/node_modules/`
6. Verifier dependances client : `ls ~/.claude/observability/apps/client/node_modules/`
7. Tester endpoint : `curl -s http://localhost:4000/`
8. Verifier port 4000 : `ss -tlnp | grep 4000`
9. Afficher tableau resultats
