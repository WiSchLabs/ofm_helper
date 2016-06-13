
# OFM Helper [![Build Status](https://travis-ci.org/Sh4kE/ofm_helper.svg?branch=master)](https://travis-ci.org/Sh4kE/ofm_helper) [![Coverage Status](https://coveralls.io/repos/github/Sh4kE/ofm_helper/badge.svg?branch=master)](https://coveralls.io/github/Sh4kE/ofm_helper?branch=master)

# Task board

[![Stories ready](https://badge.waffle.io/Sh4kE/ofm_helper.png?label=ready&title=Ready)](http://waffle.io/Autostew/autostew)
[![Stories in progress](https://badge.waffle.io/Sh4kE/ofm_helper.png?label=in%20progress&title=In%20progress)](http://waffle.io/Autostew/autostew)
[![Stories in review](https://badge.waffle.io/Sh4kE/ofm_helper.png?label=in%20review&title=In%20review)](http://waffle.io/Autostew/autostew)

[![Throughput Graph](https://graphs.waffle.io/Sh4kE/ofm_helper/throughput.svg)](https://waffle.io/Sh4kE/ofm_helper/metrics/throughput)



# Usage in Windows

1. Install Kitematic (https://kitematic.com/)
2. Download ofm_helper docker image (sh4ke/ofm_helper)
3. overwrite environment variables (OFM_USERNAME and OFM_PASSWORD)
4. run the container

# Usage in Linux

1. install docker
2. docker pull sh4ke/ofm_helper
3. docker run -d --name ofm_helper -e "OFM_USERNAME=<your ofm username>" -e "OFM_PASSWORD=<your ofm password>" sh4ke/ofm_helper