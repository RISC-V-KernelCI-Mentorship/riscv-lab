#!/bin/bash

build_id=$1
if [ -z $build_id ]
then
	echo "Missing build id"
	exit 1
fi
results_dir="/tmp/results_${build_id}"
cat $results_dir/output.log
