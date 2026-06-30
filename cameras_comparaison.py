"""
Launch both live_recording.py scripts (GoPro + integrated) simultaneously and compare them with the same parameters.
"""

import sys
import os
import asyncio
import argparse

INTEGRATED_SCRIPT = os.path.join(os.path.dirname(__file__), "integrated", "live_recording.py")
GOPRO_SCRIPT = os.path.join(os.path.dirname(__file__), "gopro", "live_recording.py")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")

WIDTH_CHOICES = [3840, 2560, 1920, 1280, 640]
HEIGHT_CHOICES = [2160, 1440, 1080, 720, 480]
FPS_CHOICES = [24, 30, 60, 120, 240]
FOV_CHOICES = ["wide", "narrow", "superview", "linear"]
SPEED_PRESET_CHOICES = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "veryslow"]

def verify_path(path:str):
    if not os.path.exists(path):
        sys.exit(f"[Error] File not found {path}\n")

async def run_script(label:str, script:str, args:list[str]):
    """Run a Python script as an async subprocess"""
    print(f"[{label}] Starting {script}")

    cmd = [
        sys.executable, script,
        "--output", OUTPUT_DIR
    ] + args

    process = await asyncio.create_subprocess_exec(*cmd)

    return_code = await process.wait()
    print(f"[{label}] Finished (exit code {return_code})")

async def main(args:argparse.Namespace):
    verify_path(GOPRO_SCRIPT)
    verify_path(INTEGRATED_SCRIPT)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    args_cam = [
        "--width", str(args.width),
        "--height", str(args.height),
        "--fps", str(args.fps),
        "--bitrate", str(args.bitrate),
        "--fov", str(args.fov),
        "--speed-preset", str(args.speed_preset)
    ]

    await asyncio.gather(
        run_script("Gopro", GOPRO_SCRIPT, args_cam),
        run_script("Integrated", INTEGRATED_SCRIPT, args_cam)
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launching script to compare cameras (GoPro and built-in camera)")
    parser.add_argument("--width", type=list, default=1280, choices=WIDTH_CHOICES, help="Frame width of the cameras")
    parser.add_argument("--height", type=list, default=720, choices=HEIGHT_CHOICES, help="Frame height of the cameras")
    parser.add_argument("--fps", type=int, default=120, choices=FPS_CHOICES, help="Frame Per Second (fps) of the cameras")
    parser.add_argument("--bitrate", type=int, default=5000, help="Bitrate of the cameras")
    parser.add_argument("--fov", type=str, default="linear", choices=FOV_CHOICES, help="Field of View of the GoPro")
    parser.add_argument("--speed-preset", type=str, default="veryfast", choices=SPEED_PRESET_CHOICES, help="Speed Preset of the built-in camera")
    args = parser.parse_args()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\n[Main] Interrupted - both recording stopped")

"""
Optimal parameters for GoPro:
- resolution: 5.3K [5312,4648]
- fps: 50 ??
- lens: linear
- stabilisation: off
- shutter speed: 1/480
- white balance: auto
- iso min: 100
- aspect ratio: 16:9
- ev: 0
- iso max: 1600
"""