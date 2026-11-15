# Install every skill in this repo (dirs containing SKILL.md).
# Usage: ./install.ps1 [claude|codex|opencode|all|<dir>] ...   (default: all)
#   claude   -> ~/.claude/skills
#   codex    -> ~/.agents/skills
#   opencode -> ~/.config/opencode/skills
param([Parameter(ValueFromRemainingArguments)][string[]]$Target = @('all'))
$ErrorActionPreference = 'Stop'

function Install-To([string]$Dest) {
  New-Item -ItemType Directory -Force -Path $Dest | Out-Null
  Get-ChildItem -Path $PSScriptRoot -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } | ForEach-Object {
    $t = Join-Path $Dest $_.Name
    New-Item -ItemType Directory -Force -Path $t | Out-Null
    Copy-Item -Path (Join-Path $_.FullName '*') -Destination $t -Recurse -Force
    Write-Host "installed $($_.Name) -> $t"
  }
}

if ($Target -contains 'all') { $Target = 'claude', 'codex', 'opencode' }
foreach ($t in $Target) {
  switch ($t) {
    'claude'   { Install-To (Join-Path $HOME '.claude/skills') }
    'codex'    { Install-To (Join-Path $HOME '.agents/skills') }
    'opencode' { Install-To (Join-Path $HOME '.config/opencode/skills') }
    default    { Install-To $t }
  }
}
