# OFM Helper [![Build Status](https://travis-ci.org/WiSchLabs/ofm_helper.svg?branch=master)](https://travis-ci.org/WiSchLabs/ofm_helper) [![Coverage Status](https://coveralls.io/repos/github/WiSchLabs/ofm_helper/badge.svg?branch=master)](https://coveralls.io/github/WiSchLabs/ofm_helper?branch=master) [![](https://images.microbadger.com/badges/image/wischlabs/ofm_helper.svg)](http://microbadger.com/images/wischlabs/ofm_helper "Get your own image badge on microbadger.com") [![Pinkie Pie Approval Status](http://dosowisko.net/pinkiepieapproved.svg)](https://www.youtube.com/watch?v=FULyN9Ai-A0)

# Features
* Kopieren der aktuellen Spieltagsdaten mittels Knopfdrucks
* Darstellung historischer Spieltagsdaten:
    * Spielerstatistiken
    * Finanzen
    * Ligaspiele
    * Stadiondaten
    * and more to come :=)

# Task board

[![Stories ready](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=backlog&title=Backlog)](http://waffle.io/WiSchLabs/ofm_helper)
[![Stories in progress](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=in%20progress&title=In%20progress)](http://waffle.io/WiSchLabs/ofm_helper)
[![Stories in review](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=in%20review&title=In%20review)](http://waffle.io/WiSchLabs/ofm_helper)

[![Throughput Graph](https://graphs.waffle.io/WiSchLabs/ofm_helper/throughput.svg)](https://waffle.io/WiSchLabs/ofm_helper/metrics/throughput)

# Installation

## Windows

1. Lade das zip Archiv vom [aktuellen Release](https://github.com/WiSchLabs/ofm_helper/releases/latest)
2. Entapcke das Archiv in ein beliebiges Verzeichnis auf deinem Rechner
3. Installiere Phantomjs nach C:\Program Files (x86)\phantomjs (enthalten im zip Archiv)
4. Eventuell musst du die .exe Datei in deinem Virenscanner zu den Ausnahmen hinzufügen
   - z.B. Avira: Rechtsklibk in der Symbolleiste auf das Logo > Virenschutz verwalten > PC-Sicherheit > Echtzeit-Scanner > Scan > Ausnahmen > Vom Echtzeit-Scanner auszulassende Dateiobjekte 
5. Falls du eine bestehende Version on OFM Helper updaten willst, kopiere noch die Datenbank (Ordner `ofm_helper/database`) aus dem alten Verzeichnis in das neue
6. Starte die Anwendung mit dem Doppelklick auf `launchapp.exe`
7. Erstelle einen neuen Account mit deinen OFM Logindaten

## Windows / OS X  mit Docker

0. Boote ins BIOS / EFI und aktiviere "Virtualization"
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

0. Boote ins BIOS / EFI und aktiviere "Virtualization"
1. Installiere Docker
2. `docker pull wischlabs/ofm_helper`
3. `docker create -v /code/database --name dbstore noumia/data /bin/true`
4. `docker run -d --name ofm_helper --volumes-from dbstore --restart=unless-stopped wischlabs/ofm_helper`
5. Finde die IP-Addresse des Containers heraus: 

    `OFM_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' ofm_helper)`
6. Öffne die IP auf dem Port 8000 (`$OFM_IP:8000`) in deinem Browser
7. Erstelle einen neuen Account mit deinen OFM Logindaten


