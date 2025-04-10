#!/bin/bash

set -euo pipefail 

TESTS=($@)

PARSED_TESTS=$( printf '%s\n' "${TESTS[@]}" | jq -R . | jq -cs .)
JSON=$(jq -cn --argjson tests "$PARSED_TESTS" '{test: $tests}')
echo "$JSON"