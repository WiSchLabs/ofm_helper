#!/bin/bash

shopt -s nullglob
set -- *.xls
if [ "$#" -gt 0 ]; then
    for FILE in *.xls; do
        FILENAME=$(echo $FILE | awk '{split($0,a,"."); print a[1]}')
        if [ -e "$FILENAME.csv" ]
        then
            echo "File already exists: $FILENAME.csv"
        else
            # convert to csv
            libreoffice --headless --convert-to csv $FILE

            # get start index of header line
            START=$(grep -n Nr\\.,Spieltag $FILENAME.csv | awk '{split($0,a,":"); print a[1]}')

            # drop first lines until start of header line
            tail -n +$START "$FILENAME.csv" > "$FILENAME.tmp"

            # remove csv in order to append to it later
            rm -f "$FILENAME.csv"

            # convert from windows encoding to utf-8
            iconv -f cp1252 -t utf-8  "$FILENAME.tmp" > "$FILENAME.csv"

            # delete stuffz
            rm -f "$FILENAME.tmp"
            rm -f $FILE
        fi
    done
fi
