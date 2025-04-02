#!/bin/bash
# SPDX-FileCopyrightText: 2023 Rivos Inc.
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail
d=$(dirname "${BASH_SOURCE[0]}")
build_id=$1
. $d/series/utils.sh

logs=$(get_logs_dir)
f=${logs}/kselftest.log

date -Iseconds | tee -a ${f}
echo "Run kselftests" | tee -a ${f}

parsed_build=$(get_parsed_name $build_id)

${d}/series/build_only_kselftest.sh $parsed_build | tee -a ${f}

${d}/series/test_only_kselftest.sh $parsed_build "${ci_root}/${parsed_build}/kselftest_install" | tee -a ${f}
