#!/bin/bash
# SPDX-FileCopyrightText: 2023 Rivos Inc.
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

d=$(dirname "${BASH_SOURCE[0]}")
cur_dir=$(pwd)
. ${d}/utils.sh

build_id=$1

install=${ci_root}/${build_id}
output=${install}_build

rm -rf ${install}
mkdir -p ${install}

cp ${cur_dir}/Image ${install}
cp -r ${cur_dir}/modules/* ${install}

