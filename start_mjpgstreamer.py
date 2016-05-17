import os
os.chdir('/usr/src/mjpg-streamer-code-182/mjpg-streamer')
os.system('./mjpg_streamer -i "./input_uvc.so -d /dev/video0 -r 320*240 -f 12 -yuv" -o "./output_http.so -p 8080 -w ./www"')
