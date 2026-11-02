# Bring every code repo up to date. workspace-sync only clones missing repos; it never pulls.
# On its PR base and clean: fast-forward. Anything else (a work branch, local changes): fetch only, and say so.
Set-Location (Join-Path $PSScriptRoot '..')
foreach ($d in Get-ChildItem -Directory) {
  $r = $d.Name; if (-not (Test-Path (Join-Path $r '.git'))) { continue }
  $base = (git -C $r symbolic-ref --short refs/remotes/origin/HEAD 2>$null) -replace '^origin/', ''
  if (-not $base) { $base = 'main' }
  $branch = git -C $r branch --show-current
  if ($branch -eq $base -and -not (git -C $r status --porcelain)) {
    git -C $r pull -q --ff-only
    if ($LASTEXITCODE -eq 0) { "  pulled   $r ($base)" } else { "  FAILED   ${r}: pull --ff-only refused" }
  } else {
    git -C $r fetch -q
    "  fetched  ${r}: on $branch, not $base, or has changes; left as it is"
  }
}
