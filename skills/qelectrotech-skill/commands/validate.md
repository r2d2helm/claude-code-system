# Valider l'integrite d'un projet QET

Verifie la coherence XML, les references, les UUIDs et les liaisons d'un projet.

## Modes de validation

| Mode | Description |
|------|-------------|
| `quick` | Validation XML basique + references embed:// |
| `full` | Quick + UUIDs + orphelins + cross-references |
| `strict` | Full + conducteurs + coherence complete |

## Verifications effectuees

### 1. Validation XML

- Fichier XML bien forme (parsing sans erreur)
- Noeud racine `<project>` present
- Attributs `title` et `version` definis
- Encodage UTF-8 verifie

### 2. References embed://

- Chaque `embed://import/...` pointe vers un element existant dans `<collection>`
- Pas de chemins casses ou mal formes
- Detection des prefixes invalides (ni `embed://`, ni `common://`, ni `custom://`)

### 3. Unicite des UUIDs

- Tous les UUIDs d'elements sont uniques dans le projet
- Tous les UUIDs de terminaux sont uniques dans le projet
- Format UUID valide : `{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}`
- Detection des UUIDs vides ou mal formes

### 4. Elements orphelins

- Elements presents dans `<collection>` mais non references par aucun `<element>` dans les diagrammes
- Signaler comme warning (pas bloquant, mais gonfle la taille du fichier)

### 5. Elements manquants

- Elements references par `embed://` mais absents de `<collection>`
- Signaler comme erreur (le projet ne s'ouvrira pas correctement)

### 6. References croisees

- Chaque element `slave` pointe vers un `master` existant
- Les types de xref (coil/protection/commutator) sont coherents
- Les formules de labels sont valides

### 7. Conducteurs (mode strict)

- Chaque conducteur a `terminal1` et `terminal2` valides
- Les terminaux references existent dans les elements du meme diagramme
- Pas de conducteurs orphelins (connectes a un seul terminal)
- Coherence des attributs (section, couleur, cable)

## Format de sortie

```
# Validation - projet.qet

## Resume
- Mode : full
- Statut : 3 erreurs, 5 warnings

## Erreurs
[ERR-01] Element manquant : embed://import/10_electric/.../missing.elmt (Folio 3)
[ERR-02] UUID duplique : {abc-123...} sur 2 elements (Folio 1 et 4)
[ERR-03] Slave orphelin : -K3 n'a pas de master correspondant (Folio 5)

## Warnings
[WARN-01] Element orphelin dans collection : custom_element.elmt (non utilise)
[WARN-02] UUID vide sur terminal (element K1, Folio 2)
[WARN-03] Conducteur sans numerotation (Folio 1, 12 conducteurs)
[WARN-04] Conducteur sans section definie (Folio 3, W15)
[WARN-05] Formule auto-numerotation vide (conductors_autonums)

## Statistiques
- Folios : 8
- Elements : 156 (dont 4 orphelins)
- Conducteurs : 234 (dont 12 sans num)
- UUIDs : 390 uniques / 392 total (2 doublons)
- Cross-refs : 8 master / 14 slave
```

## Actions PowerShell

### Validation rapide

```powershell
try {
    [xml]$project = [System.IO.File]::ReadAllText($projectPath)
    Write-Host "XML valide"
} catch {
    Write-Host "ERREUR XML: $_"
}

# Verifier les references embed://
$refs = $project.SelectNodes('//element/@type') | ForEach-Object { $_.'#text' }
$collection = $project.SelectNodes('//collection//element/@name') | ForEach-Object { $_.'#text' }
$missing = $refs | Where-Object { $_ -match 'embed://' } | Where-Object {
    $name = ($_ -split '/')[-1]
    $name -notin $collection
}
```

## Exemple

```
/qet-validate "projet.qet"
/qet-validate "projet.qet" --mode strict
/qet-validate "projet.qet" --mode quick --fix
```

$ARGUMENTS
