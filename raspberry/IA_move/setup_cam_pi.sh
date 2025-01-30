#!/bin/bash 

apt update
apt install adb
apt install v4l2loopback-utils
apt install v4l-utils

adb forward tcp:4747 tcp:4747
modprobe v4l2loopback devices=1 video_nr=0 card_label="DroidCam"
