"""
Live preview from GoPro HERO13 Black without recording.
Displays the camera stream directly on Jetson using GStreamer.
"""

import os
import asyncio
from open_gopro import WiredGoPro

async def main():

    async with WiredGoPro() as gopro:

        print("Connecting to GoPro...")

        # Open GoPro preview stream
        # This does NOT start recording
        preview = await gopro.http_command.webcam_preview()

        if not preview.ok:
            print("Failed to start preview stream")
            return

        print("Preview stream started!")

        # GoPro live stream URL
        stream_url = "udp://127.0.0.1:8554"

        # GStreamer pipeline for Jetson hardware decoding
        gst_cmd = (
            "gst-launch-1.0 "
            "udpsrc port=8554 buffer-size=2097152 ! "
            "queue ! "
            "tsdemux ! "
            "h264parse ! "
            "nvv4l2decoder ! "
            "nv3dsink sync=false"
        )

        print("\nRunning GStreamer preview pipeline:\n")
        print(gst_cmd)

        os.system(gst_cmd)

        # Stop preview when exiting
        await gopro.http_command.stop_preview()

        print("Preview stopped.")


if __name__ == "__main__":
    asyncio.run(main())
