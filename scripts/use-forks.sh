#!/usr/bin/env bash
# Point repos.json at your forks: scripts/use-forks.sh <your GitHub user or org>. Run once, before workspace-sync.
set -euo pipefail
cd "$(dirname "$0")/.."
[ $# -eq 1 ] || { echo "usage: scripts/use-forks.sh <github-user>"; exit 2; }
sed -i.bak -E "s#https://github.com/[^/]+/(aidlc-priorauth-[a-z-]+\.git)#https://github.com/$1/\1#g" repos.json && rm -f repos.json.bak
grep -o 'https://github.com/[^"]*' repos.json
