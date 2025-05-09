#!/bin/bash
# SPDX-FileCopyrightText: 2024 Rivos Inc.
#
# SPDX-License-Identifier: Apache-2.0

ci_root=${CI_ROOT:-"/build"}
ci_triple=${CI_TRIPLE:-"riscv64-linux"}
ci_patches=${CI_PATCHES:-"$d/patches"}
ci_fw_root=${CI_FW_ROOT:-"/firmware"}
ci_rootfs_root=${CI_ROOTFS_ROOT:-"/rootfs"}

ci_test_selftests=1

apply_patches() {
    if [[ -d ${ci_patches} ]]; then
	if ls ${ci_patches}/*.patch &> /dev/null; then
	    for i in ${ci_patches}/*.patch; do
		if git apply --check -q $i; then
		    git apply --index -q $i
		fi
	    done
	fi
    fi
    git commit --allow-empty -m "OOT" 
}

unapply_patches() {
    git reset --hard HEAD^
}

gen_kernel_name() {
    local xlen=$1
    local config=$2
    local fragment=$3
    local toolchain=$4

    if [[ "$config" =~ ^kselftest ]]; then
        config="kselftest"
    fi

    echo "${xlen}__${config}__$(basename $fragment)__${toolchain}"
}

get_logs_dir() {
    logs=${ci_root}/logs
    mkdir -p ${logs}
    echo ${logs}
}

get_parsed_name() {
    local name=$1
    echo $(sed "s/:/_/g" <<< $name)
}
kselftest_subtests=()
parse_tests_array() {
    local d=$(dirname "${BASH_SOURCE[0]}")
    local kselftest_location=$1
    ${d}/remove_unwanted_tests ${kselftest_location}/kselftest-list.txt
    kselftest_subtests=($(sed -r 's/^([^:]+):.*$/kselftest-\1/g' ${kselftest_location}/kselftest-list.txt | uniq))

}
