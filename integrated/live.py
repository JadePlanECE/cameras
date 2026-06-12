"""
Live from from integrated camera without recording
Displays the camera stream directly on Jetson using GStreamer
"""

import subprocess

def main():
    cmd = (
        "gst-launch-1.0 "
        "v4l2src device=/dev/video0 ! "
        "video/x-h264,width=1920,height=1080,framerate=30/1 ! "
        "h264parse ! "
        "avdec_h264 ! "
        "videoconvert ! "
        "autovideosink"
    )
    try:
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        print("The END")

if __name__ == "__main__":
    main()
