#!/usr/bin/env bash
# The one verification command for this workspace (approved at Code Generation, run after every unit).
set -uo pipefail
cd "$(dirname "$0")/../priorauth-api"
mvn -q test
