"""
Record live from GoPro HERO13 Black using GStreamer
Put the camera stream into outputs folder
"""

import os
import time
import asyncio
import argparse
import subprocess
from open_gopro import WiredGoPro, constants

async def main(output_dir, width, height, fps):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"gopro_{timestamp}.mp4"
    output_path = os.path.join(output_dir, filename)

    SUPPORTED = {
        1080: [30, 60],
        720: [30, 60, 120],
        480: [30, 60, 120],
    }

    if fps not in SUPPORTED.get(height, []):
        print(f"Warning: {fps}fps not guaranteed for {height}p webcam mode")

    async with WiredGoPro() as gopro:
        print("Connecting to GoPro...")

        match height:
            case 1080: res = constants.WebcamResolution.RES_1080
            case 720: res = constants.WebcamResolution.RES_720
            case 480: res = constants.WebcamResolution.RES_480
            case _: raise ValueError("Unsupported resolution") #res = constants.WebcamResolution.NOT_APPLICABLE

        #resp = await gopro.http_command.webcam_start()
        resp = await gopro.http_command.webcam_start(
            resolution=res,
            fov=constants.WebcamFOV.LINEAR,
            port=8554,
            protocol=constants.WebcamProtocol.TS
        )
        if not resp.ok:
            print("Failed to start webcam")
            return

        cmd = (
            f"gst-launch-1.0 -e "
            f"udpsrc port=8554 caps=\"video/mpegts\" ! "
            f"tsdemux ! "
            f"h264parse ! "
            f"video/x-h264,fps={fps}/1 ! " # constrain framerate if necessary
            f"mp4mux ! "
            f"filesink location={output_path}"
        )

        proc = subprocess.Popen(cmd, shell=True)
        print("Press Ctrl+C to STOP recording\n")

        try:
            while proc.poll() is None:
                await asyncio.sleep(0.5)

        except KeyboardInterrupt:
            print("\nInterrupted by user. Stopping recording...")
        except asyncio.CancelledError:
            print("\nStopping recording...")
        finally:
            if proc.poll() is None:
                proc.terminate()
                proc.wait()

            print(f"Recording complete! Saved to {output_path}")
            print("Exiting webcam mode on GoPro...")
            await gopro.http_command.webcam_exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("--output", type=str, default="./outputs", help="Outut directory")
    parser.add_argument("--width", type=int, default=1920, help="Width of resolution")
    parser.add_argument("--height", type=int, default=1080, help="Height of resolution")
    parser.add_argument("--fps", type=int, default=60, help="Framerate per second")
    args = parser.parse_args()

    try:
        asyncio.run(main(args.output, args.width, args.height, args.fps))
    except KeyboardInterrupt:
        pass
