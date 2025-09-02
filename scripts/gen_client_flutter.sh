#!/usr/bin/env bash
set -e
OUT=mobile/lib/api
mkdir -p "$OUT"
docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
  -i /local/docs/openapi.yaml \
  -g dart-dio \
  -o /local/$OUT
echo "Client Dart generato in $OUT"

