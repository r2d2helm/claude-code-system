#Requires -Version 5.1
<#
.SYNOPSIS
    Generation de mots de passe securises via cryptographie.

.DESCRIPTION
    Genere des mots de passe cryptographiquement securises avec controle
    de la longueur, complexite et caracteres speciaux.

.PARAMETER Length
    Longueur du mot de passe (defaut: 24).

.PARAMETER NoSpecial
    Exclure les caracteres speciaux.

.PARAMETER Count
    Nombre de mots de passe a generer.

.NOTES
    Version: 1.0.0
    Author: Claude Code
#>

[CmdletBinding()]
param(
    [int]$Length = 24,
    [switch]$NoSpecial,
    [int]$Count = 1
)

$ErrorActionPreference = "Stop"

function New-SecurePassword {
    param(
        [int]$Len = 24,
        [switch]$ExcludeSpecial
    )

    $lower = 'abcdefghijkmnopqrstuvwxyz'
    $upper = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    $digits = '23456789'
    $special = '!@#$%&*-_=+?'

    if ($ExcludeSpecial) {
        $charset = $lower + $upper + $digits
    } else {
        $charset = $lower + $upper + $digits + $special
    }

    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $bytes = New-Object byte[] $Len
    $password = New-Object char[] $Len

    # Generer les bytes aleatoires
    $rng.GetBytes($bytes)

    for ($i = 0; $i -lt $Len; $i++) {
        $password[$i] = $charset[$bytes[$i] % $charset.Length]
    }

    # Garantir au moins 1 de chaque type requis
    $rng.GetBytes($bytes)
    $positions = @(0, 1, 2)
    if (-not $ExcludeSpecial) { $positions += 3 }

    $idx = 0
    foreach ($pos in $positions) {
        $charSet = switch ($pos) {
            0 { $lower }
            1 { $upper }
            2 { $digits }
            3 { $special }
        }
        $byteVal = $bytes[$idx]
        $targetPos = $bytes[$idx + $positions.Count] % $Len
        $password[$targetPos] = $charSet[$byteVal % $charSet.Length]
        $idx++
    }

    $rng.Dispose()
    return [string]::new($password)
}

function Measure-PasswordStrength {
    param([string]$Password)

    $score = 0
    $details = @()

    # Longueur
    if ($Password.Length -ge 8) { $score += 10; $details += "Length >= 8" }
    if ($Password.Length -ge 16) { $score += 10; $details += "Length >= 16" }
    if ($Password.Length -ge 24) { $score += 5; $details += "Length >= 24" }

    # Complexite
    if ($Password -cmatch '[a-z]') { $score += 10; $details += "Lowercase" }
    if ($Password -cmatch '[A-Z]') { $score += 10; $details += "Uppercase" }
    if ($Password -match '[0-9]') { $score += 10; $details += "Digits" }
    if ($Password -match '[^a-zA-Z0-9]') { $score += 15; $details += "Special chars" }

    # Entropie approximative
    $charsetSize = 0
    if ($Password -cmatch '[a-z]') { $charsetSize += 26 }
    if ($Password -cmatch '[A-Z]') { $charsetSize += 26 }
    if ($Password -match '[0-9]') { $charsetSize += 10 }
    if ($Password -match '[^a-zA-Z0-9]') { $charsetSize += 32 }

    $entropy = [math]::Round($Password.Length * [math]::Log($charsetSize, 2), 1)
    if ($entropy -ge 60) { $score += 10; $details += "Entropy >= 60 bits" }
    if ($entropy -ge 80) { $score += 10; $details += "Entropy >= 80 bits" }
    if ($entropy -ge 100) { $score += 10; $details += "Entropy >= 100 bits" }

    $rating = switch {
        ($score -ge 80) { "Excellent" }
        ($score -ge 60) { "Fort" }
        ($score -ge 40) { "Moyen" }
        default { "Faible" }
    }

    return @{
        Score = $score
        Rating = $rating
        Entropy = $entropy
        Details = $details
    }
}

# Main
for ($i = 0; $i -lt $Count; $i++) {
    $pwd = New-SecurePassword -Len $Length -ExcludeSpecial:$NoSpecial
    $strength = Measure-PasswordStrength -Password $pwd

    Write-Host "Password $($i+1): $pwd" -ForegroundColor Green
    Write-Host "  Strength: $($strength.Rating) ($($strength.Score)/100, ~$($strength.Entropy) bits entropy)" -ForegroundColor Cyan
}
