# R2D2 Departement Trevize - Agents Thematiques Quotidiens
# Schedule: Lundi-Vendredi 12h00 via Task Scheduler
# But: Lancer les 4 agents thematiques P1 pour enrichir les dossiers de recherche
# "Les patterns emergent AVANT que la realite les confirme."

$ErrorActionPreference = "SilentlyContinue"
$LogFile = "$env:USERPROFILE\.claude\automation\logs\trevize-agents-$(Get-Date -Format 'yyyy-MM-dd').log"
$LogDir = Split-Path $LogFile
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts | $msg" | Tee-Object -FilePath $LogFile -Append
}

Log "=== Departement Trevize - Agents Thematiques START ==="

$agents = @(
    @{
        Name = "agent-souverainete"
        Prompt = "Tu es l'Agent Souverainete du Departement Trevize. Recherche les dernieres actualites sur : CLOUD Act, alternatives europeennes a Microsoft, migrations vers des solutions souveraines (OVHcloud, Scaleway, OpenDesk, Nextcloud), mouvements politiques pro-souverainete en EU. Score chaque finding avec le scoring Seldon. Genere un rapport court avec les 3-5 findings les plus pertinents."
    },
    @{
        Name = "agent-nis2"
        Prompt = "Tu es l'Agent NIS2 du Departement Trevize. URGENCE : deadline 18 avril 2026. Recherche : evolution conformite NIS2 en Belgique, nouveaux guides CCB/Safeonweb, amendes infligees, impact supply chain, prestataires certifies. Score chaque finding. Genere rapport court."
    },
    @{
        Name = "agent-ia"
        Prompt = "Tu es l'Agent IA Agentique du Departement Trevize. Recherche : nouvelles stats adoption agents IA en entreprise, cas de ROI mesure, echecs documentes, architectures multi-agents, small models/world models, IA souveraine/locale. Compare avec le modele R2D2 (23 skills multi-agents). Rapport court."
    },
    @{
        Name = "agent-saaspocalypse"
        Prompt = "Tu es l'Agent SaaSpocalypse du Departement Trevize. Recherche : evolution cours ETF IGV, annonces de migration self-hosted, comparatifs TCO cloud vs on-premise, nouvelles alternatives open source aux SaaS US, impact IA agentique sur modele licence. Identifie opportunites pour R2D2. Rapport court."
    }
)

foreach ($agent in $agents) {
    Log "Launching: $($agent.Name)"
    try {
        $result = claude --print $agent.Prompt 2>&1
        $outputFile = "$LogDir\$($agent.Name)-$(Get-Date -Format 'yyyy-MM-dd').txt"
        $result | Out-File -FilePath $outputFile -Encoding utf8
        Log "  Completed: $($agent.Name) ($($result.Length) chars)"
    } catch {
        Log "  ERROR: $($agent.Name) failed: $_"
    }
}

Log "=== Departement Trevize - Agents Thematiques END ==="
