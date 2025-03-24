#!/bin/bash

ssh_key=$1
build_id=$2
output_dir="/tmp/results_${build_id}"
if [ -z $ssh_key ]
then
	echo "Missing required ssh key"
	return 1
fi
if [ -z $build_id ]
then
	echo "Missing build id"
	return 1
fi
mkdir -p $output_dir &&\
ssh -T -o StrictHostKeyChecking=no root@localhost -p 2222 -i $ssh_key \
-t 'export LC_ALL=C.UTF-8;cd /tests; bash run_kselftest.sh -s; exit' &&\
scp -P 2222 -o StrictHostKeyChecking=no -i $ssh_key root@localhost:/tests/output.log "$output_dir/output.log"
