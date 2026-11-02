# Called by verify.cmd. verify.ps1 [repo...]   With no repos: every repo whose branch is not its PR base or that has uncommitted changes.
Set-Location (Join-Path $PSScriptRoot '..')
$repos = @($args)
if ($repos.Count -eq 0) {
  foreach ($d in Get-ChildItem -Directory) {
    if (-not (Test-Path (Join-Path $d.Name '.git'))) { continue }
    $base = (git -C $d.Name symbolic-ref --short refs/remotes/origin/HEAD 2>$null) -replace '^origin/', ''
    if (-not $base) { $base = 'main' }
    if ((git -C $d.Name branch --show-current) -ne $base -or (git -C $d.Name status --porcelain)) { $repos += $d.Name }
  }
}
if ($repos.Count -eq 0) { 'verify: no repo is off its PR base; nothing to test'; exit 0 }
$fail = 0
foreach ($r in $repos) {
  if     (Test-Path "$r/pom.xml")        { $exe = 'mvn'; $a = @('-q', 'test') }
  elseif (Test-Path "$r/package.json")   { $exe = 'npm'; $a = @('test', '--silent') }
  elseif (Test-Path "$r/pyproject.toml") { $exe = 'uv';  $a = @('run', 'pytest', '-q') }
  else { "verify: $r has no test command (no pom.xml, package.json or pyproject.toml)"; continue }
  "verify: ${r}: $exe $($a -join ' ')"
  Push-Location $r; & $exe @a; $code = $LASTEXITCODE; Pop-Location
  if ($code -ne 0) { "verify: $r FAILED"; $fail = 1 }
}
exit $fail
