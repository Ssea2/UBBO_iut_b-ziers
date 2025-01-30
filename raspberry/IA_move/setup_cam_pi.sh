#!/bin/bash 

sudo apt update
sudo apt install adb
sudo apt install v4l2loopback-utils
sudo apt install v4l-utils

adb forward tcp:4747 tcp:4747
sudo modprobe v4l2loopback devices=1 video_nr=0 card_label="DroidCam"
