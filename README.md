# OFM Helper [![Build Status](https://travis-ci.org/WiSchLabs/ofm_helper.svg?branch=master)](https://travis-ci.org/WiSchLabs/ofm_helper) [![Coverage Status](https://coveralls.io/repos/github/WiSchLabs/ofm_helper/badge.svg?branch=master)](https://coveralls.io/github/WiSchLabs/ofm_helper?branch=master) [![](https://images.microbadger.com/badges/image/wischlabs/ofm_helper.svg)](http://microbadger.com/images/wischlabs/ofm_helper "size of the docker image") [![Pinkie Pie Approval Status](http://dosowisko.net/pinkiepieapproved.svg)](https://www.youtube.com/watch?v=FULyN9Ai-A0)

## Features
* Kopieren der aktuellen Spieltagsdaten mittels Knopfdrucks
* Darstellung historischer Spieltagsdaten:
    * Spielerstatistiken
    * Finanzen
    * Ligaspiele
    * Stadiondaten
    * and more to come :=)

## Task board

[![Stories ready](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=backlog&title=Backlog)](http://waffle.io/WiSchLabs/ofm_helper)
[![Stories in progress](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=in%20progress&title=In%20progress)](http://waffle.io/WiSchLabs/ofm_helper)
[![Stories in review](https://badge.waffle.io/WiSchLabs/ofm_helper.png?label=in%20review&title=In%20review)](http://waffle.io/WiSchLabs/ofm_helper)

[![Throughput Graph](https://graphs.waffle.io/WiSchLabs/ofm_helper/throughput.svg)](https://waffle.io/WiSchLabs/ofm_helper/metrics/throughput)

## Installation

### Windows

1. Lade das zip Archiv vom [aktuellen Release](https://github.com/WiSchLabs/ofm_helper/releases/latest)
2. Entapcke das Archiv in ein beliebiges Verzeichnis auf deinem Rechner
3. Installiere Phantomjs nach C:\Program Files (x86)\phantomjs (enthalten im zip Archiv)
4. Eventuell musst du die .exe Datei in deinem Virenscanner zu den Ausnahmen hinzufügen
   - z.B. Avira: Rechtsklibk in der Symbolleiste auf das Logo > Virenschutz verwalten > PC-Sicherheit > Echtzeit-Scanner > Scan > Ausnahmen > Vom Echtzeit-Scanner auszulassende Dateiobjekte
5. Falls du eine bestehende Version on OFM Helper updaten willst, kopiere noch die Datenbank (Ordner `ofm_helper/database`) aus dem alten Verzeichnis in das neue
6. Starte die Anwendung mit dem Doppelklick auf `launchapp.exe`
7. Erstelle einen neuen Account mit deinen OFM Logindaten

### Windows / Linux / OS X (mit Docker)

0. Boote ins BIOS / EFI und aktiviere "Virtualization"
1. Installiere Docker und docker-compose
2. Starte die Container mit: `docker-compose up -d`
3. Migriere die Datenbank zum aktuellen Stand: `docker exec -it ofmhelper_web_1 python manage.py migrate`
4. Öffne die Addresse: 127.0.0.1 in deinem Browser
5. Erstelle einen neuen Account mit deinen OFM Logindaten


