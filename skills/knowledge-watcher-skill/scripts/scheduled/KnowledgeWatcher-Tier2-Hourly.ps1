# KnowledgeWatcher-Tier2-Hourly.ps1
$skillPath = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Import-Module (Join-Path $skillPath "scripts\KnowledgeWatcher.psm1") -Force
Write-KWLog "Tier 2 (Hourly) - DÃ©marrage"
# TODO: ImplÃ©menter traitement Downloads, Formations
Write-KWLog "Tier 2 (Hourly) - TerminÃ©"