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

FOV_CHOICES = ["wide", "narrow", "superview", "linear"]
FOV_MAP = {
    "wide":      WebcamFOV.WIDE,
    "narrow":    WebcamFOV.NARROW,
    "superview": WebcamFOV.SUPERVIEW,
    "linear":    WebcamFOV.LINEAR,
}

GOPRO_STREAMING_PORT = 8554

async def main(output_dir:str, width:int, height:int, fps:int, bitrate:int, fov:str):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"gopro_{timestamp}.mp4"
    output_path = os.path.join(output_dir, filename)

    async with WiredGoPro() as gopro:
        print("[GoPro] Connecting to GoPro...")

        resp = await gopro.http_command.webcam_start(
            resolution=HEIGHT_RESOLUTION[height],
            fov=FOV_MAP[fov],
            port=GOPRO_STREAMING_PORT,
            protocol=WebcamProtocol.TS
        )
        if not resp.ok:
            print("[GoPro] Failed to start webcam")
            return
        print("[GoPro] Webcam started - Launching GStreamer")

        cmd = (
            f"gst-launch-1.0 -e "
            f"udpsrc port={GOPRO_STREAMING_PORT} "
            f'caps="video/mpegts,systemstream=true" ! '
            f"tsdemux ! "
            f"h264parse ! "
            f"avdec_h264 ! "
            f"videorate ! "
            f"video/x-raw,framerate={fps}/1 ! "
            f"x264enc tune=zerolatency speed-preset=veryfast bitrate={bitrate} ! "
            f"h264parse ! "
            f"mp4mux ! "
            f"filesink location={output_path}"
        )

        proc = subprocess.Popen(cmd, shell=True)
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
    parser.add_argument("--fps", type=int, default=60, help="Framerate per second")
    parser.add_argument("--bitrate", type=int, default=5000, help="Bitrate")
    parser.add_argument("--fov", type=str, default="linear", choices=FOV_CHOICES, help="Field of View of the GoPro")
    parser.add_argument("--speed-preset", type=bool, default=False, help=".")
    args = parser.parse_args()

    try:
        asyncio.run(main(args.output, args.width, args.height, args.fps, args.bitrate, args.fov))
    except KeyboardInterrupt:
        pass
