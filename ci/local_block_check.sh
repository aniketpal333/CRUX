#!/usr/bin/env bash
set -e
NOTEBOOK="${1:-samples/02_messy.ipynb}"
echo "🔍 CRUX gate check on $NOTEBOOK"
if crux audit "$NOTEBOOK" --strict; then
    echo "✅ Merge allowed"
    exit 0
else
    echo "❌ MERGE BLOCKED"
    exit 1
fi