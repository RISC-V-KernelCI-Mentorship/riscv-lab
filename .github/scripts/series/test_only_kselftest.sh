#!/bin/bash
# SPDX-FileCopyrightText: 2023 Rivos Inc.
#
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
d=$(dirname "${BASH_SOURCE[0]}")
. $d/utils.sh

build_id=$1
test_collection=$2

$d/unpack_fw.sh
rc=0

kselftest_subtests=($test_collection)
parallel_log=$(mktemp -p ${ci_root})
for subtest in "${kselftest_subtests[@]}"; do
    echo "${d}/kernel_tester.sh $build_id ${subtest}"
done | parallel -j$(($(nproc))) --colsep ' ' --joblog ${parallel_log} || true

cat ${parallel_log}
rm ${parallel_log}
