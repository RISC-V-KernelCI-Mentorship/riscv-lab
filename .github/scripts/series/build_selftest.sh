#!/bin/bash
# SPDX-FileCopyrightText: 2024 Rivos Inc.
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

d=$(dirname "${BASH_SOURCE[0]}")
cur_dir=$(pwd)
. ${d}/utils.sh

# E.g. build_selftest.sh rv64 kselftest-bpf plain gcc
 
build_id=$1

install=${ci_root}/${build_id}

mkdir -p ${install}/kselftest_install
cp -r ${cur_dir}/kselftest/* ${install}/kselftest_install
