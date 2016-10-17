#!/bin/bash

touch .version
echo `git describe --tags --always` | awk '{split($0,a,"-"); print a[1]}' > .version
git add .version
git commit -m '[autocommit] updated version number'
git push

mkdir release
cd release
wget --no-check-certificate https://ofmhelper.de/downloads/ofmhelper2exe.tar.gz
tar -xzf ofmhelper2exe.tar.gz
rm ofmhelper2exe.tar.gz
ls .. | grep -v release | xargs -i cp -r ../{} ofm_helper/.
zip -qdgds 10m -r ofm_helper.zip *
mv ofm_helper.zip ..