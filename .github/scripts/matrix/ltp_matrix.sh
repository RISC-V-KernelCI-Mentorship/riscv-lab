#!/bin/bash

set -euo pipefail

d=`dirname ${BASH_SOURCE[0]}`

output=$1
name=${2:-"matrix"}
separator=${3:-"="}
# TODO ltp-controllers is too slow for now because of cgroup_fj_stress.sh
# but I haven't found an easy to skip this one from tuxrun
ltp_tests=( "ltp-commands"  "ltp-syscalls" "ltp-mm" "ltp-hugetlb" "ltp-crypto" "ltp-cve" "ltp-containers" "ltp-fs" "ltp-sched" )
json=$($d/generate_json.sh "${ltp_tests[@]}")
echo $name$separator$json >> $output