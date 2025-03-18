#!/bin/bash

source run_tests.sh

kernel=$1
image=$2
initrd=$3
build_id=$4
if [ -z $kernel ]
then
	echo "Missing kernel image url"
	return 1
fi
if [ -z $image ]
then
	echo "Missing disk image"
	return 1
fi
if [ -z $initrd ]
then
	echo "Missing initrd"
	return 1
fi
if [ -z $build_id ]
then
	echo "Missing build id"
	return 1
fi
kernel_output="/tmp/Image_${build_id}"
curl -L $kernel --output $kernel_output &&\
qemu-system-riscv64 -m 2G -smp 2 \
-kernel $kernel_output \
-bios /usr/lib/riscv64-linux-gnu/opensbi/generic/fw_jump.bin \
-object rng-random,filename=/dev/urandom,id=rng \
-append "root=LABEL=rootfs console=ttyS0 rw" \
-device virtio-blk-device,drive=hd0 \
-initrd $initrd \
-machine virt \
-cpu rv64 \
-drive file=$image,if=none,id=hd0 \
-device virtio-net-device,netdev=net \
-netdev user,id=net,hostfwd=tcp::2222-:22 \
-display none &
QEMU_PROCESS=$!
echo $QUEMU_PROCESS

