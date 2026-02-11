$SkillPath = 'C:\Users\r2d2\.claude\skills\knowledge-watcher-skill'
Import-Module (Join-Path $SkillPath 'scripts\KnowledgeWatcher.psm1') -Force
. (Join-Path $SkillPath 'sources\GenericFileSource.ps1')
. (Join-Path $SkillPath 'sources\BrowserBookmarksSource.ps1')

$sources = Get-KWSources | Where-Object { $_.tier -eq 3 -and $_.enabled }
foreach ($source in $sources) {
    if ($source.type -eq 'directory') {
        Invoke-DirectoryScan -SourceConfig $source
    }
    elseif ($source.type -eq 'browser-bookmarks') {
        Invoke-BookmarksCapture
    }
}

$state = Get-KWState
$state.lastTier3Run = (Get-Date).ToString('o')
Save-KWState -State $state

& (Join-Path $SkillPath 'scripts\Invoke-QueueProcessor.ps1') -BatchSize 20