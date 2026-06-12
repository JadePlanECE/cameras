"""
SV-USB4KCAM01H-H120 4K USB Camera.
Maybe it is a Sony IMX415 sensor.
Trying to get the data from a jetson.
"""

import cv2

gst_pipeline = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=3840, height=2160, "
    "format=NV12, framerate=30/1 ! "
    "nvvidconv ! "
    "video/x-raw, format=BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=BGR ! "
    "appsink"
)

cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("IMX415", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
