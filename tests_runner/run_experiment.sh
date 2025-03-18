#!/bin/bash

source run_tests.sh

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
./download_image.sh &&\
sudo ./copy_selftests.sh $selftests $image_dir/image.qcow2 &&\
./run_qemu.sh $kernel_image $image_dir/image.qcow2 $image_dir/initrd $build_id &&\
sleep 20 &&\
run_tests $image_dir/ssh_user_rsa_key $build_id &&\
pkill qemu-system
