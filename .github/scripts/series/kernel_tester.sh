#!/bin/bash
# SPDX-FileCopyrightText: 2023 Rivos Inc.
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

d=$(dirname "${BASH_SOURCE[0]}")
. $d/utils.sh

build_id=$1
tst=$2
rootfs="ubuntu"

test_name=$(sed 's/[\\/\r\n*?|:><"]/./g' <<< $tst)

tm=$(mktemp -p ${ci_root})
n=$build_id
logs=$(get_logs_dir)
log="test_kernel___${n}___${rootfs}___${test_name}.log"
rc=0
allrc=0
\time --quiet -o $tm -f "took %es" \
    $d/test_kernel.sh "${build_id}" "${tst}" &> "${logs}/${log}" || rc=$?
if (( $rc )); then
allrc=1
echo "::error::FAIL Test kernel ${n} ${rootfs} ${tst} \"${log}\" $(cat $tm)"
else
echo "::notice::OK Test kernel ${n} ${rootfs} ${tst} $(cat $tm)"
fi
rm $tm
exit $allrc

