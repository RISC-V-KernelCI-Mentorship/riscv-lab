#!/bin/bash

selftest_url=$1
disk_image=$2
tests_file="kselftest.tar.gz"
tests_dir=tests
tests_mount=/mnt/tests_image
set -x
if [ "$EUID" -ne 0 ]
then
	echo "Script needs to be run as root"
	exit 1
fi
if [ -z $selftest_url ]
then
	echo "Missing kselftests URL"
	exit 2
fi
if [ -z $disk_image ]
then
	echo "Missing disk image path"
	exit 2
fi
curl -L $selftest_url --output $tests_file &&\
rm -rf $tests_dir
mkdir -p $tests_dir && \
tar xf $tests_file -C $tests_dir &&\
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
rmmod nbd
