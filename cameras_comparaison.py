"""
File to launch both python files "live_recording.py" (of gopro and integrated cameras)
"""

import sys
import os
import asyncio
import json
import argparse

GOPRO_PATH = "./gopro/live_recording.py"
INTEGRATED_PATH = "./integrated/live_recording.py"
CONFIGS_PATH = "./configs.json"
OUTPUT_DIR = "./outputs"

def verify_path(path):
    if not os.path.exists(path):
        sys.exit(f"[Error] File not found {path}\n")

def load_configs():
    with open(CONFIGS_PATH) as f:
        return json.load(f)

async def run_script(script_path, configs):
    """Launches a python script as an asynchronous subprocess."""
    print(f"[Starting] {script_path}...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    process = await asyncio.create_subprocess_exec(
        sys.executable, script_path,
        "--output", OUTPUT_DIR,
        "--width", str(configs["resolution"][0]),
        "--height", str(configs["resolution"][1]),
        "--fps", str(configs["fps"]),
        stdout=None,
        stderr=None,
    )

    return_code = await process.wait()
    print(f"[Finished] {script_path} with exit code {return_code}")

async def main(name):
    verify_path(GOPRO_PATH)
    verify_path(INTEGRATED_PATH)
    verify_path(CONFIGS_PATH)

    configs = load_configs()

    await asyncio.gather(
        run_script(GOPRO_PATH, configs[name]),
        run_script(INTEGRATED_PATH, configs[name])
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("--name", type=str, default="1080p60", help="Name of the config wanted")
    args = parser.parse_args()

    asyncio.run(main(args.name))
