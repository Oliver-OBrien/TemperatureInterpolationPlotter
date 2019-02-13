#This file was used to get data from a particular day.

cat data/lincoln_11.csv | grep -e 2016-$1 -e STATION
