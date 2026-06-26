"""
Record live from from integrated camera
Displays the camera stream directly on Jetson using GStreamer
Then put it into outputs folder
"""

import os
import time
import argparse
import subprocess

def main(output_dir, width, height, fps):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"integrated_{timestamp}.mp4"
    output_path = os.path.join(output_dir, filename)

    record_cmd = (
        f"gst-launch-1.0 -e "
        f"v4l2src device=/dev/video0 ! "
        f"video/x-h264,width={width},height={height},framerate={fps}/1 ! "
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
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("--output", type=str, default="./outputs", help="Outut directory")
    parser.add_argument("--width", type=int, default=1920, help="Width of resolution")
    parser.add_argument("--height", type=int, default=1080, help="Height of resolution")
    parser.add_argument("--fps", type=int, default=60, help="Framerate per second")
    args = parser.parse_args()

    try:
        main(args.output, args.width, args.height, args.fps)
    except KeyboardInterrupt:
        pass
