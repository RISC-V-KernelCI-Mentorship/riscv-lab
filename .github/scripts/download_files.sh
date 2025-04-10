#!/bin/bash

set -x
d=`dirname ${BASH_SOURCE[0]}`
kernel=$1
modules=$2
selftests=$3
no_decompress=${4:-""}
output_dir=/build/my-linux
modules_dir=${output_dir}/modules
kselftest_dir=${output_dir}/kselftest

mkdir -p ${kselftest_dir}
mkdir -p ${modules_dir}

curl -L $kernel -o ${output_dir}/Image
if [[ -n $modules ]]
then
	curl -L $modules -o ${modules_dir}/modules.tar.xz
	if [[ $no_decompress != "--nodecompress" ]]
	then
		tar xvf ${modules_dir}/modules.tar.xz -C ${modules_dir}
	fi
fi
if [[ -n $selftests ]]
then
	curl -L $selftests -o selftests.tar.gz &&\
	tar xvf selftests.tar.gz -C ${kselftest_dir}
fi
