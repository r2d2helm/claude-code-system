# KnowledgeWatcher-Tier3-Daily.ps1
$skillPath = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Import-Module (Join-Path $skillPath "scripts\KnowledgeWatcher.psm1") -Force
Write-KWLog "Tier 3 (Daily) - DÃ©marrage"
# TODO: ImplÃ©menter traitement Bookmarks, Scripts
Write-KWLog "Tier 3 (Daily) - TerminÃ©"