#!/bin/bash

# This script is meant for local use

base_dir=$(dirname $0)

kernel_image=$1
selftests=$2
build_id=$3
image_dir=/tmp/dqib_riscv64-virt

if [ "$EUID" -eq 0 ]
then
	echo "Do not call this script as root"
	exit 1
fi
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
$base_dir/run_tests.sh $image_dir/ssh_user_rsa_key $build_id &&\
$base_dir/print_tests_results.sh $build_id &&\
pkill qemu-system
