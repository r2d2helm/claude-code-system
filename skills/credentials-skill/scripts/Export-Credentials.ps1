#Requires -Version 5.1
<#
.SYNOPSIS
    Export du registre vers Bitwarden CSV, KeePass XML, JSON ou CSV.

.PARAMETER Format
    Format d'export : bitwarden, keepass, json, csv

.NOTES
    Version: 1.0.0
    Author: Claude Code
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateSet('bitwarden', 'keepass', 'json', 'csv')]
    [string]$Format
)

$ErrorActionPreference = "Stop"
$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\CredentialRegistry.psm1") -Force

$exportDir = Join-Path $SkillPath "data\exports"
if (-not (Test-Path $exportDir)) {
    New-Item -ItemType Directory -Path $exportDir -Force | Out-Null
}

$timestamp = (Get-Date).ToString("yyyyMMdd-HHmmss")
$entries = Get-AllCredentialEntries

function Extract-Password {
    param([string]$Body)
    if ($Body -match 'Password[:\s]*\*?\*?\s*([^\r\n]+)') {
        return $Matches[1].Trim()
    }
    if ($Body -match 'Token[:\s]*\*?\*?\s*([^\r\n]+)') {
        return $Matches[1].Trim()
    }
    if ($Body -match 'Key[:\s]*\*?\*?\s*([^\r\n]+)') {
        return $Matches[1].Trim()
    }
    return ""
}

function Extract-Username {
    param([string]$Body)
    if ($Body -match '(Username|Email|User)[:\s]*\*?\*?\s*([^\r\n]+)') {
        return $Matches[2].Trim()
    }
    return ""
}

switch ($Format) {
    'bitwarden' {
        $fileName = "bitwarden_${timestamp}.csv"
        $filePath = Join-Path $exportDir $fileName
        $lines = @("folder,favorite,type,name,notes,fields,reprompt,login_uri,login_username,login_password,login_totp")

        foreach ($entry in $entries) {
            $fm = $entry.Frontmatter
            $url = "$($fm['protocol'])://$($fm['host']):$($fm['port'])"
            $username = Extract-Username -Body $entry.Body
            $password = Extract-Password -Body $entry.Body
            $folder = "homelab/$($fm['category'])"
            $name = $fm['service']
            $notes = "VM: $($fm['vm']) | Criticality: $($fm['criticality'])"

            $line = "$folder,,$([int]1),$name,$notes,,,`"$url`",$username,$password,"
            $lines += $line
        }

        $content = $lines -join "`n"
        Write-Utf8File -Path $filePath -Content $content
    }

    'keepass' {
        $fileName = "keepass_${timestamp}.xml"
        $filePath = Join-Path $exportDir $fileName

        $xml = @"
<?xml version="1.0" encoding="utf-8"?>
<KeePassFile>
    <Root>
        <Group>
            <Name>Homelab</Name>
"@

        $groups = @{}
        foreach ($entry in $entries) {
            $cat = $entry.Frontmatter['category']
            if (-not $groups.ContainsKey($cat)) { $groups[$cat] = @() }
            $groups[$cat] += $entry
        }

        foreach ($groupName in $groups.Keys) {
            $xml += "`n            <Group>`n                <Name>$groupName</Name>"
            foreach ($entry in $groups[$groupName]) {
                $fm = $entry.Frontmatter
                $username = Extract-Username -Body $entry.Body
                $password = Extract-Password -Body $entry.Body
                $url = "$($fm['protocol'])://$($fm['host']):$($fm['port'])"

                $xml += @"

                <Entry>
                    <String><Key>Title</Key><Value>$($fm['service'])</Value></String>
                    <String><Key>UserName</Key><Value>$username</Value></String>
                    <String><Key>Password</Key><Value Protected="False">$password</Value></String>
                    <String><Key>URL</Key><Value>$url</Value></String>
                    <String><Key>Notes</Key><Value>VM: $($fm['vm']) | Category: $($fm['category'])</Value></String>
                </Entry>
"@
            }
            $xml += "`n            </Group>"
        }

        $xml += @"

        </Group>
    </Root>
</KeePassFile>
"@
        Write-Utf8File -Path $filePath -Content $xml
    }

    'json' {
        $fileName = "credentials_${timestamp}.json"
        $filePath = Join-Path $exportDir $fileName
        $data = @()
        foreach ($entry in $entries) {
            $fm = $entry.Frontmatter
            $data += @{
                service = $fm['service']
                slug = $entry.Slug
                category = $fm['category']
                host = $fm['host']
                port = $fm['port']
                vm = $fm['vm']
                username = Extract-Username -Body $entry.Body
                password = Extract-Password -Body $entry.Body
                auth_type = $fm['auth_type']
                criticality = $fm['criticality']
            }
        }
        $json = $data | ConvertTo-Json -Depth 5
        Write-Utf8File -Path $filePath -Content $json
    }

    'csv' {
        $fileName = "credentials_${timestamp}.csv"
        $filePath = Join-Path $exportDir $fileName
        $lines = @("service,slug,category,host,port,vm,username,password,auth_type,criticality")
        foreach ($entry in $entries) {
            $fm = $entry.Frontmatter
            $username = Extract-Username -Body $entry.Body
            $password = Extract-Password -Body $entry.Body
            $lines += "$($fm['service']),$($entry.Slug),$($fm['category']),$($fm['host']),$($fm['port']),$($fm['vm']),$username,$password,$($fm['auth_type']),$($fm['criticality'])"
        }
        $content = $lines -join "`n"
        Write-Utf8File -Path $filePath -Content $content
    }
}

Write-Host "Exported $($entries.Count) credentials to $filePath" -ForegroundColor Green
Write-Host "Format: $Format" -ForegroundColor Cyan
