# /pai-verify-hooks — Verifier hooks

Verifier l'integrite du systeme de hooks PAI.

## Syntaxe

```
/pai-verify-hooks
```

## Procedure

1. Verifier le repertoire hooks/ existe : `ls ~/.claude/hooks/`
2. Compter les fichiers .hook.ts : `ls ~/.claude/hooks/*.hook.ts | wc -l` (attendu: 15)
3. Verifier chaque hook attendu existe :
   - SecurityValidator.hook.ts, LoadContext.hook.ts, StartupGreeting.hook.ts
   - CheckVersion.hook.ts, UpdateTabTitle.hook.ts, SetQuestionTab.hook.ts
   - ExplicitRatingCapture.hook.ts, FormatEnforcer.hook.ts (ou FormatReminder)
   - StopOrchestrator.hook.ts, SessionSummary.hook.ts, QuestionAnswered.hook.ts
   - AutoWorkCreation.hook.ts, WorkCompletionLearning.hook.ts
   - ImplicitSentimentCapture.hook.ts, AgentOutputCapture.hook.ts
4. Verifier lib/ (12 fichiers) : `ls ~/.claude/hooks/lib/ | wc -l`
5. Verifier handlers/ (4 fichiers) : `ls ~/.claude/hooks/handlers/ | wc -l`
6. Verifier enregistrement dans settings.json : `cat ~/.claude/settings.json | jq '.hooks | keys'`
7. Afficher tableau resultats
