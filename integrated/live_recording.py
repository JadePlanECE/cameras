"""
Record live from integrated (built-in) webcam using GStreamer
Save stream to outputs folder
"""

import os
import time
import argparse
import subprocess

SPEED_PRESET_CHOICES = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "veryslow"]

def main(output_dir:str, width:int, height:int, fps:int, bitrate:int, speed_preset:str):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"integrated_{timestamp}.mp4"
    output_path = os.path.join(output_dir, filename)

    cmd = (
        f"gst-launch-1.0 -e "
        f"v4l2src device=/dev/video0 ! "
        f"videoconvert ! "
        f"videoscale ! "
        f"videorate ! "
        f"video/x-raw,width={width},height={height},framerate={fps}/1 ! "
        f"x264enc tune=zerolatency speed-preset={speed_preset} bitrate={bitrate} ! "
        f"mp4mux ! "
        f'filesink location="{output_path}"'
    )

    print("[Integrated] Press Ctrl+C to STOP recording\n")

    try:
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()
        print(f"[Integrated] Saved to {output_path}")
    except KeyboardInterrupt:
        proc.terminate()
        print("[Integrated] Recording interrupted by user")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Built-in webcam live recording")
    parser.add_argument("--output", type=str, default="./outputs", help="Outut directory")
    parser.add_argument("--width", type=int, default=1920, help="Width of resolution")
    parser.add_argument("--height", type=int, default=1080, help="Height of resolution")
    parser.add_argument("--fps", type=int, default=60, help="Framerate per second")
    parser.add_argument("--bitrate", type=int, default=8000, help="Bitrate")
    parser.add_argument("--speed-preset", type=str, default="veryfast", choices=SPEED_PRESET_CHOICES, help="Speed Preset of the built-in camera")
    parser.add_argument("--fov", type=bool, default=False, help=".")
    args = parser.parse_args()

    try:
        main(args.output, args.width, args.height, args.fps, args.bitrate, args.speed_preset)
    except KeyboardInterrupt:
        pass
