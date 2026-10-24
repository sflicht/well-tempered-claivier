#!/bin/bash
# usage: norm.sh name   (in ../renders/v5)
cd ../renders/v5
n=$1
raw=$(ffmpeg -hide_banner -nostats -i $n.wav -af ebur128=peak=true -f null - 2>&1 | grep -A1 "Integrated loudness" | grep " I:" | awk '{print $2}')
g=$(python3 -c "print(round(-19.3-($raw),2))")
ffmpeg -hide_banner -loglevel error -y -i $n.wav -af volume=${g}dB -codec:a libmp3lame -b:a 192k $n.mp3
after=$(ffmpeg -hide_banner -nostats -i $n.mp3 -af ebur128=peak=true -f null - 2>&1 | grep -A1 "Integrated loudness" | grep " I:" | awk '{print $2}')
pk=$(ffmpeg -hide_banner -nostats -i $n.mp3 -af ebur128=peak=true -f null - 2>&1 | grep -A1 "True peak" | grep " Peak:" | awk '{print $2}')
echo "$n raw=$raw gain=${g}dB after_mp3=$after LUFS, true peak $pk dBFS" | tee -a gains.txt
ffprobe -v error -show_entries format=duration -of csv=p=0 $n.mp3
