"""
Record live from from integrated camera
Displays the camera stream directly on Jetson using GStreamer
Then put it into outputs folder
"""

import os
import time
import subprocess

OUTPUT_DIR = "./outputs"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"integrated_{timestamp}.mp4"
    output_path = os.path.join(OUTPUT_DIR, filename)

    record_cmd = (
        f"gst-launch-1.0 -e "
        f"v4l2src device=/dev/video0 ! "
        f"video/x-h264,width=1920,height=1080,framerate=30/1 ! "
        f"h264parse ! "
        f"qtmux ! "
        f"filesink location={output_path}"
    )

    try:
        proc = subprocess.Popen(record_cmd, shell=True)
        proc.wait()
        print(f"Recording complete! Saved to {output_path}")
    except KeyboardInterrupt:
        proc.terminate()
        print("Recording interrupted by user.")
        return

if __name__ == "__main__":
    main()
