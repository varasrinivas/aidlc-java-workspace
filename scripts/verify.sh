#!/usr/bin/env bash
# The one verification command for this workspace (approved at Code Generation, run after every unit).
# verify.sh [repo...]   With no repos: every repo whose branch is not its PR base or that has uncommitted changes.
set -uo pipefail
cd "$(dirname "$0")/.."
repos=("$@")
if [ ${#repos[@]} -eq 0 ]; then
  for d in */; do
    r=${d%/}; [ -e "$r/.git" ] || continue
    base=$(git -C "$r" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null); base=${base#origin/}
    if [ "$(git -C "$r" branch --show-current)" != "${base:-main}" ] || [ -n "$(git -C "$r" status --porcelain)" ]; then repos+=("$r"); fi
  done
fi
[ ${#repos[@]} -eq 0 ] && { echo "verify: no repo is off its PR base; nothing to test"; exit 0; }
fail=0
for r in "${repos[@]}"; do
  if   [ -f "$r/pom.xml" ];        then cmd="mvn -q test"
  elif [ -f "$r/package.json" ];   then cmd="npm test --silent"
  elif [ -f "$r/pyproject.toml" ]; then cmd="uv run pytest -q"
  else echo "verify: $r has no test command (no pom.xml, package.json or pyproject.toml)"; continue; fi
  echo "verify: $r: $cmd"
  (cd "$r" && $cmd) || { echo "verify: $r FAILED"; fail=1; }
done
exit $fail
