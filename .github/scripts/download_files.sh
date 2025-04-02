#!/bin/bash


d=`dirname ${BASH_SOURCE[0]}`
kernel=$1
modules=$2
selftests=$3
output_dir=/build/my-linux
modules_dir=${output_dir}/modules
kselftest_dir=${output_dir}/kselftest
mkdir -p ${kselftest_dir}
mkdir -p ${modules_dir}

curl -L $kernel -o ${output_dir}/Image &&\
curl -L $modules -o modules.tar.xz &&\
tar xvf modules.tar.xz -C ${modules_dir} &&\
curl -L $selftests -o selftests.tar.gz &&\
tar xvf selftests.tar.gz -C ${kselftest_dir}
