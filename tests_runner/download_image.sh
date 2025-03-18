#!/bin/bash

zip_name="/tmp/riscv-deb.zip"
image_url="https://gitlab.com/api/v4/projects/giomasce%2Fdqib/jobs/artifacts/master/download?job=convert_riscv64-virt"
curl -L $image_url --output $zip_name &&\
unzip -o $zip_name -d /tmp/ &&\
chmod 400 /tmp/dqib_riscv64-virt/ssh_user_rsa_key

