
# [OFM Helper](https://ofmhelper.de) [![Build Status](https://travis-ci.org/WiSchLabs/ofm_helper.svg?branch=master)](https://travis-ci.org/WiSchLabs/ofm_helper) [![Coverage Status](https://coveralls.io/repos/github/WiSchLabs/ofm_helper/badge.svg?branch=master)](https://coveralls.io/github/WiSchLabs/ofm_helper?branch=master)

# Task board

[![Stories ready](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=backlog&title=Backlog)](http://waffle.io/WiSchLabs/ofm_helper)
[![Stories in progress](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=in%20progress&title=In%20progress)](http://waffle.io/WiSchLabs/ofm_helper)
[![Stories in review](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=in%20review&title=In%20review)](http://waffle.io/WiSchLabs/ofm_helper)

[![Throughput Graph](https://graphs.waffle.io/WiSchLabs/ofm_helper/throughput.svg)](https://waffle.io/WiSchLabs/ofm_helper/metrics/throughput)

# Install

## Deutsch

0. Boote ins BIOS / EFI und aktiviere "Virtualization"

### Windows / OS X 

1. Installiere Kitematic (https://kitematic.com/)
2. Downloade das ofm_helper Docker image "wischlabs/ofm_helper" (Es startet automatisch einen neuen Container)
3. Stoppe den laufenden Container
4. Erstelle auf deinem System einen Ordner für die Datenbank
5. Innerhalb von Kitematic gehe zu Settings -> Volumes
6. Ändere das Volume zu deinem neu erstellen Datenbankordner
7. Starte den Container erneut
8. Klicke auf das Voschaufenster um OFMHelper in deinem Standardbrowser zu öffnen
9. Erstelle einen neuen Account mit deinen OFM Logindaten

### Linux / OS X

1. Installiere Docker
2. docker pull wischlabs/ofm_helper
3. docker create -v /code/database --name dbstore noumia/data /bin/true
4. docker run -d --name ofm_helper --volumes-from dbstore --restart=unless-stopped wischlabs/ofm_helper
5. Finde die IP-Addresse des Containers heraus: `docker inspect ofm_helper| grep -i IPAddress | awk '{print $2}'`
6. Erstelle einen neuen Account mit deinen OFM Logindaten

## English

0. Boot into BIOS / EFI and enable Virtualization

### Usage in Windows

1. Install Kitematic (https://kitematic.com/)
2. Download ofm_helper docker image "wischlabs/ofm_helper" (It will automatically start a new container)
3. Stop the running container
4. Create a new directory on your local system, which will be holding the database
5. In Kitematic goto Settings -> Volumes
6. Change the Volume to your newly created directory
7. Restart the container
8. Click on the preview picture to access the webapp in your browser.
9. Create a new account with your ofm credentials

### Usage in Linux

1. Install docker
2. docker pull wischlabs/ofm_helper
3. docker create -v /code/database --name dbstore noumia/data /bin/true
4. docker run -d --name ofm_helper --volumes-from dbstore --restart=unless-stopped wischlabs/ofm_helper
5. Finde die IP-Addresse des Containers heraus: `docker inspect ofm_helper| grep -i IPAddress | awk '{print $2}'`
6. Create a new account with your ofm credentials
