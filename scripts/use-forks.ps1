# Point repos.json at your forks: .\scripts\use-forks.ps1 <your GitHub user or org>. Run once, before workspace-sync.
param([Parameter(Mandatory = $true)][string]$User)
Set-Location (Join-Path $PSScriptRoot '..')
$text = [IO.File]::ReadAllText("$PWD\repos.json")
$text = $text -replace 'https://github.com/[^/]+/(aidlc-priorauth-[a-z-]+\.git)', "https://github.com/$User/`$1"
[IO.File]::WriteAllText("$PWD\repos.json", $text)
[regex]::Matches($text, 'https://github.com/[^"]*') | ForEach-Object { $_.Value }
