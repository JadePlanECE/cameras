"""
Read videos
"""

import sys
import os
import subprocess

OUTPUT_DIR = "./outputs"
VIDEO = "gopro_20260612_154006.mp4"
#VIDEO = "integrated_20260612_150018.mp4"
PATH = "/home/hand-e/Documents/cameras/outputs/" + VIDEO

def main():
    if not os.path.exists(PATH):
        sys.exit(f"[Error] File not found {PATH}\n")

    cmd = (
        f"gst-launch-1.0 -e filesrc location={PATH} ! "
        f"qtdemux name=demux demux.video_0 ! "
        f"h264parse ! "
        f"avdec_h264 ! "
        f"videoconvert ! "
        f"autovideosink sync=true"
    )

    try:
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        print("The END")

if __name__ == "__main__":
    main()
