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

# GoPro: 1080 (1920x1080), 2.7k (2704x1520), 4k (3840x2160), 5.3k (5312x2988)
# Integrated: 640x360, 640x480, 960x540, 1024x576, 1280x720, 1920x1080, 2560x1440, 3840x2160
WIDTH_CHOICES = [1920, 3840]
HEIGHT_CHOICES = [1080, 2160]
# GoPro: 24, 30, 60, 120, 240
# Integrated: 15, 20, 30
FPS_CHOICES = [30]

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
        "--fps", str(args.fps)
    ]

    await asyncio.gather(
        run_script("Gopro", GOPRO_SCRIPT, args_cam),
        run_script("Integrated", INTEGRATED_SCRIPT, args_cam)
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launching script to compare cameras (GoPro and built-in camera)")
    parser.add_argument("--width", type=int, default=1920, choices=WIDTH_CHOICES, help="Width of the cameras")
    parser.add_argument("--height", type=int, default=1080, choices=HEIGHT_CHOICES, help="Height of the cameras")
    parser.add_argument("--fps", type=int, default=30, choices=FPS_CHOICES, help="Frame Per Second (fps) of the cameras")
    args = parser.parse_args()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\n[Main] Interrupted - both recording stopped")
