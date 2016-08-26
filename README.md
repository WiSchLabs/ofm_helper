# OFM Helper [![Build Status](https://travis-ci.org/WiSchLabs/ofm_helper.svg?branch=master)](https://travis-ci.org/WiSchLabs/ofm_helper) [![Coverage Status](https://coveralls.io/repos/github/WiSchLabs/ofm_helper/badge.svg?branch=master)](https://coveralls.io/github/WiSchLabs/ofm_helper?branch=master)

# Task board

[![Stories ready](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=backlog&title=Backlog)](http://waffle.io/WiSchLabs/ofm_helper)
[![Stories in progress](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=in%20progress&title=In%20progress)](http://waffle.io/WiSchLabs/ofm_helper)
[![Stories in review](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=in%20review&title=In%20review)](http://waffle.io/WiSchLabs/ofm_helper)

[![Throughput Graph](https://graphs.waffle.io/WiSchLabs/ofm_helper/throughput.svg)](https://waffle.io/WiSchLabs/ofm_helper/metrics/throughput)

# Installation

0. Boote ins BIOS / EFI und aktiviere "Virtualization"

## Windows / OS X 

1. Installiere Kitematic (https://kitematic.com/)
2. Downloade das ofm_helper Docker image "wischlabs/ofm_helper" (Es startet automatisch einen neuen Container)
3. Stoppe den laufenden Container
4. Erstelle auf deinem System innerhalb deines Benutzerordners einen Ordner für die Datenbank (z.B. C:\Users\DeinNutzername\OFM_Helper_Datenbank)
5. Innerhalb von Kitematic gehe zu Settings -> Volumes
6. Ändere das Volume zu deinem neu erstellten Datenbankordner
7. Starte den Container erneut
8. Klicke auf das Voschaufenster in Kitematic um OFMHelper in deinem Standardbrowser zu öffnen
9. Erstelle einen neuen Account mit deinen OFM Logindaten

## Linux / OS X

1. Installiere Docker
2. `docker pull wischlabs/ofm_helper`
3. `docker create -v /code/database --name dbstore noumia/data /bin/true`
4. `docker run -d --name ofm_helper --volumes-from dbstore --restart=unless-stopped wischlabs/ofm_helper`
5. Finde die IP-Addresse des Containers heraus: 

    `OFM_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' ofm_helper)`
6. Öffne die IP auf dem Port 8000 (`$OFM_IP:8000`) in deinem Browser
7. Erstelle einen neuen Account mit deinen OFM Logindaten