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

def calculate_bitrate(width:int, height:int, fps:int):
    """
    Estimate a suitable H.264 bitrate in kbps based on resolution, and fps
    bitrate = width x height x fps x bits_per_pixel x compression_ratio
    """
    bpp = 0.06

    # Base bitrate from formula (in kbps)
    bitrate = int(width * height * fps * bpp / 1000)

    # High fps costs less per-frame (temporal redundancy is higher),
    # so apply a mild discount above 60 fps
    if fps > 60:
        bitrate = int(bitrate * 0.85)

    # Clamp to sane min/max
    bitrate = max(1000, min(bitrate, 60_000))

    return round(bitrate, -2)

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

    if args.bitrate is None:
        bitrate = calculate_bitrate(args.width, args.height, args.fps)
        print(f"[Main] Bitrate calculated: {bitrate}")
    else:
        bitrate = args.bitrate
        print(f"[Main] Bitrate taken: {bitrate}")

    args_cam = [
        "--width", str(args.width),
        "--height", str(args.height),
        "--fps", str(args.fps),
        "--bitrate", str(bitrate),
        "--fov", str(args.fov),
        "--speed-preset", str(args.speed_preset)
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
    parser.add_argument("--bitrate", type=int, default=None, help="Bitrate of the cameras (if None then calculated automatically)")
    parser.add_argument("--speed-preset", type=str, default="veryfast", choices=SPEED_PRESET_CHOICES, help="Speed Preset of the camera")
    parser.add_argument("--fov", type=str, default="linear", choices=FOV_CHOICES, help="Field Of View (fov) of the GoPro")
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