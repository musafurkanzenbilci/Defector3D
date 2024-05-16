#!/bin/bash
mkdir -p /tmp/stream
while true; do
    gst-launch-1.0 nvarguscamerasrc ! 'video/x-raw(memory:NVMM),width=640,height=480,framerate=30/1' ! nvvidconv ! 'video/x-raw,format=I420' ! jpegenc ! multifilesink location=/tmp/stream/pic.jpg
    sudo systemctl restart nvargus-daemon.service
done

