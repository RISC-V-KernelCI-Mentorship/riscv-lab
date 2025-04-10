#!/bin/bash

set -euo pipefail
d=`dirname ${BASH_SOURCE[0]}`
. $d/../series/utils.sh
selftests=$1
output=$2
name=${3:-"matrix"}
separator=${4:-"="}

curl -L $selftests -o selftests.tar.gz &&\
tar xvf selftests.tar.gz

parse_tests_array .
json=$($d/generate_json.sh "${kselftest_subtests[@]}")
echo $name$separator$json >> $output
