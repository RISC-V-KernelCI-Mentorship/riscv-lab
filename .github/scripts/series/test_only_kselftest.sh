#!/bin/bash
# SPDX-FileCopyrightText: 2023 Rivos Inc.
#
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
set -x
d=$(dirname "${BASH_SOURCE[0]}")
. $d/utils.sh

build_id=$1
kselftest_location=$2

$d/unpack_fw.sh
rc=0

kselftest_subtests=($(sed -r 's/^([^:]+):.*$/"kselftest-\1"/g' ${kselftest_location}/kselftest-list.txt | uniq))
parallel_log=$(mktemp -p ${ci_root})
for subtest in "${kselftest_subtests[@]}"; do
    echo "${d}/kernel_tester.sh $build_id ${subtest}"
done | parallel -j$(($(nproc))) --colsep ' ' --joblog ${parallel_log} || true

cat ${parallel_log}
rm ${parallel_log}
