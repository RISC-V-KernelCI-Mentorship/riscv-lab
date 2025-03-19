#!/bin/bash

# This script is meant for local use

base_dir=$(dirname $0)
source $base_dir/run_tests.sh

kernel_image=$1
selftests=$2
build_id=$3
image_dir=/tmp/dqib_riscv64-virt

if [ -z $kernel_image ]
then
	echo "Missing kernel image url"
	exit 1
fi
if [ -z $selftests ]
then
	echo "Missing selftests url"
	exit 1
fi
if [ -z $build_id ]
then
	echo "Missing build id"
	exit 1
fi
$base_dir/download_image.sh &&\
sudo $base_dir/copy_selftests.sh $selftests $image_dir/image.qcow2 &&\
$base_dir/run_qemu.sh $kernel_image $image_dir/image.qcow2 $image_dir/initrd $build_id &&\
run_tests $image_dir/ssh_user_rsa_key $build_id &&\
pkill qemu-system
