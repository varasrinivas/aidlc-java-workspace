#!/usr/bin/env bash
# Bring every code repo up to date. workspace-sync only clones missing repos; it never pulls.
# On its PR base and clean: fast-forward. Anything else (a work branch, local changes): fetch only, and say so.
cd "$(dirname "$0")/.."
for d in */; do
  r=${d%/}; [ -e "$r/.git" ] || continue
  base=$(git -C "$r" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null); base=${base#origin/}; base=${base:-main}
  branch=$(git -C "$r" branch --show-current)
  if [ "$branch" = "$base" ] && [ -z "$(git -C "$r" status --porcelain)" ]; then
    git -C "$r" pull -q --ff-only && echo "  pulled   $r ($base)" || echo "  FAILED   $r: pull --ff-only refused"
  else
    git -C "$r" fetch -q && echo "  fetched  $r: on $branch, not $base, or has changes; left as it is"
  fi
done
