#!/usr/bin/env bash
set -e
OUT=web-admin/src/api
mkdir -p "$OUT"
npx @openapitools/openapi-generator-cli generate \
  -i ./docs/openapi.yaml \
  -g typescript-fetch \
  -o "$OUT"
echo "Client TS generato in $OUT"

