# /pai-install — Dispatch installation interactive

Lancer l'installation de PAI avec choix interactif de la methode.

## Syntaxe

```
/pai-install [methode]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `methode` | `release`, `bundle`, `pack` | Interactif (demander) |

## Procedure

1. Verifier les prerequis avec `/pai-prereqs`
2. Si prerequis manquants, proposer de les installer
3. Demander la methode d'installation via AskUserQuestion :
   - **Full Release v2.5** (Recommande) — Systeme complet en 5 minutes
   - **Bundle + Packs manuels** — Construire en comprenant chaque piece
   - **Pack individuel** — Ajouter une capacite specifique
4. Selon le choix :
   - Release → Lancer wizard `wizard-fresh-install.md`
   - Bundle → Lancer `/pai-bundle-install`
   - Pack → Lancer `/pai-pack-install`
5. Apres installation, executer `/pai-verify` pour confirmer
