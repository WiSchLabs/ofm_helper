
# [OFM Helper](https://ofmhelper.de) [![Build Status](https://travis-ci.org/WiSchLabs/ofm_helper.svg?branch=master)](https://travis-ci.org/WiSchLabs/ofm_helper) [![Coverage Status](https://coveralls.io/repos/github/WiSchLabs/ofm_helper/badge.svg?branch=master)](https://coveralls.io/github/WiSchLabs/ofm_helper?branch=master)

# Task board

[![Stories ready](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=backlog&title=Backlog)](http://waffle.io/WiSchLabs/ofm_helper)
[![Stories in progress](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=in%20progress&title=In%20progress)](http://waffle.io/WiSchLabs/ofm_helper)
[![Stories in review](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=in%20review&title=In%20review)](http://waffle.io/WiSchLabs/ofm_helper)

[![Throughput Graph](https://graphs.waffle.io/WiSchLabs/ofm_helper/throughput.svg)](https://waffle.io/WiSchLabs/ofm_helper/metrics/throughput)



# Usage in Windows

0. Boot into BIOS / EFI and enable Virtualization
1. Install Kitematic (https://kitematic.com/)
2. Download ofm_helper docker image "wischlabs/ofm_helper" (It will automatically start a new container)
3. Click on the preview picture to access the webapp in your browser.
4. Create a new account with your ofm credentials
5. Profit!

# Usage in Linux

0. Boot into BIOS / EFI and enable Virtualization
1. Install docker
2. docker pull wischlabs/ofm_helper
3. docker run -d --name ofm_helper wischlabs/ofm_helper
4. Open 127.0.0.1:8000 in your default browser
5. Create a new account with your ofm credentials
6. Profit!