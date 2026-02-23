$SkillPath = 'C:\Users\r2d2\.claude\skills\knowledge-watcher-skill'
Import-Module (Join-Path $SkillPath 'scripts\KnowledgeWatcher.psm1') -Force
. (Join-Path $SkillPath 'sources\GenericFileSource.ps1')

$sources = Get-KWSources | Where-Object { $_.tier -eq 4 -and $_.enabled }
foreach ($source in $sources) {
    Invoke-DirectoryScan -SourceConfig $source
}

$state = Get-KWState
$state.lastTier4Run = (Get-Date).ToString('o')
Save-KWState -State $state

& (Join-Path $SkillPath 'scripts\Invoke-QueueProcessor.ps1') -BatchSize 50