#!/usr/bin/bash

cat renamePET_leftovers_log2.txt | grep Renaming | while read line ; do
old=$(echo $line | cut -f 2 -d " " )
new=$(echo $line | cut -f 5 -d " " )
echo $old,$new >> renamePetPairs.csv
done