"""
File to launch both python files "live_recording.py" (of gopro and integrated cameras)
"""

import sys
import os
import asyncio
import argparse

GOPRO_PATH = "./gopro/live_recording.py"
INTEGRATED_PATH = "./integrated/live_recording.py"
OUTPUT_DIR = "./outputs"

def verify_path(path):
    if not os.path.exists(path):
        sys.exit(f"[Error] File not found {path}\n")

async def run_script(script_path, resolution, fps):
    """Launches a python script as an asynchronous subprocess."""
    print(f"[Starting] {script_path}...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    process = await asyncio.create_subprocess_exec(
        sys.executable, script_path,
        "--output", OUTPUT_DIR,
        "--width", str(resolution[0]),
        "--height", str(resolution[1]),
        "--fps", str(fps),
        stdout=None,
        stderr=None,
    )

    return_code = await process.wait()
    print(f"[Finished] {script_path} with exit code {return_code}")

async def main(resolution, fps):
    verify_path(GOPRO_PATH)
    verify_path(INTEGRATED_PATH)

    await asyncio.gather(
        run_script(GOPRO_PATH, resolution, fps),
        run_script(INTEGRATED_PATH, resolution, fps)
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("--resolution", type=list, default=[1920, 1080], help="Resolution of the camera")
    parser.add_argument("--fps", type=int, default=30, help="Frame Per Second (fps) of the camera")
    args = parser.parse_args()

    asyncio.run(main(args.resolution, args.fps))
