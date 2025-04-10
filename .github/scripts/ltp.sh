#!/bin/bash
# SPDX-FileCopyrightText: 2023 Rivos Inc.
#
# SPDX-License-Identifier: Apache-2.0

set -euox pipefail
d=$(dirname "${BASH_SOURCE[0]}")
. $d/series/utils.sh

logs=$(get_logs_dir)
f=${logs}/ltp.log

KERNEL_PATH=$1
MODULES_PATH=$2
TEST=$3
BUILD_ID=$4
OUT_DIR="/tests/results_json"


# The Docker image comes with a prebuilt python environment with all tuxrun
# dependencies
source /build/.env/bin/activate

# TODO ltp-controllers is too slow for now because of cgroup_fj_stress.sh
# but I haven't found an easy to skip this one from tuxrun
ltp_tests=( "ltp-commands"  "ltp-syscalls" "ltp-mm" "ltp-hugetlb" "ltp-crypto" "ltp-cve" "ltp-containers" "ltp-fs" "ltp-sched" )

mkdir -p $OUT_DIR

/build/tuxrun/run --runtime null --device qemu-riscv64 --kernel $KERNEL_PATH --modules $MODULES_PATH --tests $TEST --results $OUT_DIR/$TEST.json --log-file-text $OUT_DIR/$TEST.log --timeouts $TEST=480


