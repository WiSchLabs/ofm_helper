
# OFM Helper [![Build Status](https://travis-ci.org/Sh4kE/ofm_helper.svg?branch=master)](https://travis-ci.org/Sh4kE/ofm_helper) [![Coverage Status](https://coveralls.io/repos/github/Sh4kE/ofm_helper/badge.svg?branch=master)](https://coveralls.io/github/Sh4kE/ofm_helper?branch=master)

# Task board

[![Stories ready](https://badge.waffle.io/Sh4kE/ofm_helper.png?label=backlog&title=Backlog)](http://waffle.io/Sh4kE/ofm_helper)
[![Stories in progress](https://badge.waffle.io/Sh4kE/ofm_helper.png?label=in%20progress&title=In%20progress)](http://waffle.io/Sh4kE/ofm_helper)
[![Stories in review](https://badge.waffle.io/Sh4kE/ofm_helper.png?label=in%20review&title=In%20review)](http://waffle.io/Sh4kE/ofm_helper)

[![Throughput Graph](https://graphs.waffle.io/Sh4kE/ofm_helper/throughput.svg)](https://waffle.io/Sh4kE/ofm_helper/metrics/throughput)



# Usage in Windows

0. boot into BIOS / EFI and enable Virtualization
1. Install Kitematic (https://kitematic.com/)
2. Download ofm_helper docker image (sh4ke/ofm_helper)
3. overwrite environment variables (OFM_USERNAME and OFM_PASSWORD)
4. run the container
5. look in Kitematic for the external ip address of the container and open your browser with this ip on port 8000.

# Usage in Linux

0. boot into BIOS / EFI and enable Virtualization
1. install docker
2. docker pull sh4ke/ofm_helper
3. docker run -d --name ofm_helper -e "OFM_USERNAME=<your ofm username>" -e "OFM_PASSWORD=<your ofm password>" sh4ke/ofm_helper
4. docker inspect ofm_helper | grep IPAddress
5. open your browser with this ip on port 8000
