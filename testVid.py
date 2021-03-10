import cv2
import numpy as np
import os

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

#IP address from Onvif live stream
#rtsp://169.254.161.100:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream
vcap = cv2.VideoCapture("rtsp://169.254.161.100:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream", cv2.CAP_FFMPEG)
#set frame height and width
vcap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

while(1):
    ret, frame = vcap.read()
    if ret == False:
        print("Frame is empty")
        break
    else:
        cv2.imshow('VIDEO', frame)
        cv2.waitKey(1)