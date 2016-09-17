#!/bin/bash

mkdir release
cd release
wget --no-check-certificate https://ofmhelper.de/downloads/ofmhelper2exe.tar.gz
tar -xzf ofmhelper2exe.tar.gz
rm ofmhelper2exe.tar.gz
ls .. | grep -v release | xargs -i cp -r ../{} ofm_helper/.
cd ..
zip -r ofm_helper.zip release/*