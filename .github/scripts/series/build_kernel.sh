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
if [[ -d ${cur_dir}/modules ]]
then
	cp -r ${cur_dir}/modules/ ${install}
fi
