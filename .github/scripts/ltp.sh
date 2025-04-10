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


mkdir -p $OUT_DIR

/build/tuxrun/run --runtime null --device qemu-riscv64 --kernel $KERNEL_PATH --modules $MODULES_PATH --tests $TEST --results $OUT_DIR/$TEST.json --log-file-text $OUT_DIR/$TEST.log --timeouts $TEST=480


