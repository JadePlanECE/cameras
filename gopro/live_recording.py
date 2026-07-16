"""
Record live from GoPro HERO13 Black using GStreamer
Save stream to outputs folder
"""

import os
import time
import asyncio
import argparse
import subprocess
from open_gopro import WiredGoPro
from open_gopro.constants import WebcamResolution, WebcamFOV, WebcamProtocol
#from open_gopro.models.streaming import WebcamResolution, WebcamFOV, WebcamProtocol

HEIGHT_RESOLUTION = {
    1080: WebcamResolution.RES_1080,
    720: WebcamResolution.RES_720,
    480: WebcamResolution.RES_480,
}

GOPRO_STREAMING_PORT = 8554

async def main(output_dir:str, width:int, height:int, fps:int):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"gopro_{timestamp}.mp4"
    output_path = os.path.join(output_dir, filename)

    async with WiredGoPro() as gopro:
        print("[GoPro] Connecting to GoPro...")

        resp = await gopro.http_command.webcam_start(
            resolution=HEIGHT_RESOLUTION[height],
            fov=WebcamFOV.LINEAR,
            port=GOPRO_STREAMING_PORT,
            protocol=WebcamProtocol.TS
        )
        if not resp.ok:
            print("[GoPro] Failed to start webcam")
            return
        print("[GoPro] Webcam started - Launching GStreamer")

        cmd_ = (
            f"gst-launch-1.0 -e "
            f"udpsrc port={GOPRO_STREAMING_PORT} "
            f'caps="video/mpegts" ! '
            f"tsdemux ! "
            f"h264parse ! "
            f"video/x-h264,fps={fps}/1 ! "
            f"mp4mux ! "
            f"filesink location={output_path}"
        )

        proc = subprocess.Popen(cmd_, shell=True)
        print("[GoPro] Press Ctrl+C to STOP recording\n")

        try:
            while proc.poll() is None:
                await asyncio.sleep(0.5)

        except (asyncio.CancelledError, KeyboardInterrupt):
            print("\n[GoPro] Stopping recording...")
        finally:
            if proc.poll() is None:
                proc.terminate()
                proc.wait()

            print(f"[GoPro] Saved to {output_path}")
            await gopro.http_command.webcam_exit()
            print("[GoPro] Webcam exit succefully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GoPro HERO13 live recording")
    parser.add_argument("--output", type=str, default="./outputs", help="Outut directory")
    parser.add_argument("--width", type=int, default=1920, help="Width of resolution")
    parser.add_argument("--height", type=int, default=1080, help="Height of resolution")
    parser.add_argument("--fps", type=int, default=30, help="Framerate per second")
    args = parser.parse_args()

    try:
        asyncio.run(main(args.output, args.width, args.height, args.fps))
    except KeyboardInterrupt:
        pass
