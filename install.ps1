# Install every skill in this repo (dirs containing SKILL.md) into a skills folder.
# Usage: ./install.ps1 [-Dest <target-dir>]   (default: ~/.claude/skills)
param([string]$Dest = (Join-Path $HOME '.claude/skills'))
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $Dest | Out-Null
Get-ChildItem -Path $PSScriptRoot -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } | ForEach-Object {
  $target = Join-Path $Dest $_.Name
  New-Item -ItemType Directory -Force -Path $target | Out-Null
  Copy-Item -Path (Join-Path $_.FullName '*') -Destination $target -Recurse -Force
  Write-Host "installed $($_.Name) -> $target"
}
