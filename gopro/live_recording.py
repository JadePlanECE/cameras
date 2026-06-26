"""
Record live preview from GoPro HERO13 Black from from integrated camera
Displays the camera stream directly on Jetson using GStreamer
Then put it into outputs folder
"""

import os
import time
import asyncio
import argparse
import subprocess
from open_gopro import WiredGoPro

async def main(output_dir, width, height, fps):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"gopro_{timestamp}.mp4"
    output_path = os.path.join(output_dir, filename)

    async with WiredGoPro() as gopro:
        print("Connecting to GoPro...")
        
        preview = await gopro.http_command.webcam_preview()

        if not preview.ok:
            print("Failed to start preview stream")
            return

        print("Preview stream started!")

        # GStreamer pipeline to capture UDP stream, parse it, containerize it, and save to disk
        # -e flag ensures files are closed properly on exit so the MP4 isn't corrupted
        gst_cmd = (
            f"gst-launch-1.0 -e "
            f"udpsrc port=8554 buffer-size=524288 ! "
            f"queue ! "
            f"tsdemux ! "
            f"h264parse ! "
            f"video/x-h264,width={width},height={height},framerate={fps}/1 ! "
            f"qtmux ! "
            f"filesink location={output_path}"
        )

        print(f"\nRecording started. Saving to: {output_path}")
        print("Press Ctrl+C to STOP recording.\n")

        proc = subprocess.Popen(gst_cmd, shell=True)

        try:
            while proc.poll() is None:
                await asyncio.sleep(0.5)
                
        except asyncio.CancelledError:
            print("\nStopping recording...")
        except KeyboardInterrupt:
            print("\nInterrupted by user. Stopping recording...")
        finally:
            if proc.poll() is None:
                proc.terminate()
                proc.wait()
            
            print(f"Recording complete! Saved to {output_path}")
            print("Exiting webcam mode on GoPro...")
            await gopro.http_command.webcam_exit()
            print("GoPro released successfully.")

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
