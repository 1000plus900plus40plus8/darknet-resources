#!/bin/bash -e

cd /home/user/nn/shapes_neural_network

# Warning: this file is automatically created/updated by DarkMark v1.5.30-1!
# Created on Tue 2021-12-28 23:13:28 EST by user@pop-os.

rm -f output.log
rm -f chart.png

echo "creating new log file" > output.log
date >> output.log

ts1=$(date)
ts2=$(date +%s)
echo "initial ts1: ${ts1}" >> output.log
echo "initial ts2: ${ts2}" >> output.log
echo "cmd: /home/user/darknet/darknet detector -map  train /home/user/nn/shapes_neural_network/shapes_neural_network.data /home/user/nn/shapes_neural_network/shapes_neural_network.cfg" >> output.log

/usr/bin/time --verbose /home/user/darknet/darknet detector -map  train /home/user/nn/shapes_neural_network/shapes_neural_network.data /home/user/nn/shapes_neural_network/shapes_neural_network.cfg 2>&1 | tee --append output.log

ts3=$(date)
ts4=$(date +%s)
echo "ts1: ${ts1}" >> output.log
echo "ts2: ${ts2}" >> output.log
echo "ts3: ${ts3}" >> output.log
echo "ts4: ${ts4}" >> output.log

find /home/user/nn/shapes_neural_network -maxdepth 1 -regex ".+_[0-9]+\.weights" -print -delete >> output.log

