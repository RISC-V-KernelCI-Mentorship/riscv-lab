#!/bin/bash

base_dir=$(dirname $0)
selftest_url=$1
disk_image=$2
tests_file="/tmp/kselftest.tar.gz"
tests_dir=/tmp/tests
tests_mount=/mnt/tests_image
if [ "$EUID" -ne 0 ]
then
	echo "Script needs to be run as root"
	exit 1
fi
if [ -z $selftest_url ]
then
	echo "Missing kselftests URL"
	exit 1
fi
if [ -z $disk_image ]
then
	echo "Missing disk image path"
	exit 1
fi
curl -L $selftest_url --output $tests_file &&\
rm -rf $tests_dir
mkdir -p $tests_dir && \
tar xf $tests_file -C $tests_dir &&\
# for now we remove step_after_suspend_test
$base_dir/../scripts/series/remove_unwanted_tests $tests_dir/kselftest-list.txt &&\
modprobe nbd max_part=8 &&\
qemu-nbd --connect=/dev/nbd0 $disk_image &&\
# we add a small delay
sleep 5 &&\
mkdir -p $tests_mount &&\
mount /dev/nbd0p1 $tests_mount &&\
mkdir -p $tests_mount/$tests_dir &&\
cp -r $tests_dir $tests_mount &&\
umount $tests_mount &&\
qemu-nbd --disconnect /dev/nbd0 &&\
sleep 5 &&\
rmmod nbd
