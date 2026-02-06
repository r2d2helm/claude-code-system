# KnowledgeWatcher-Tier4-Weekly.ps1
$skillPath = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Import-Module (Join-Path $skillPath "scripts\KnowledgeWatcher.psm1") -Force
Write-KWLog "Tier 4 (Weekly) - DÃ©marrage"
# TODO: ImplÃ©menter traitement Archives
Write-KWLog "Tier 4 (Weekly) - TerminÃ©"