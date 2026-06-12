"""
File to launch both python files "combine.py" (of gopro and integrated cameras)
"""

import sys
import os
import asyncio

GOPRO_PATH = "./gopro/combine.py"
INTEGRATED_PATH = "./integrated/combine.py"

async def run_script(script_path):
    """Launches a python script as an asynchronous subprocess."""
    print(f"[Starting] {script_path}...")
    
    process = await asyncio.create_subprocess_exec(
        sys.executable, script_path,
        stdout=None,  # Streams output on current terminal
        stderr=None
    )

    return_code = await process.wait()
    print(f"[Finished] {script_path} with exit code {return_code}")

async def main():
    if not os.path.exists(GOPRO_PATH):
        sys.exit(f"[Error] File not found {GOPRO_PATH}\n")
    if not os.path.exists(INTEGRATED_PATH):
        sys.exit(f"[Error] File not found {INTEGRATED_PATH}\n")

    await asyncio.gather(
        run_script(GOPRO_PATH),
        run_script(INTEGRATED_PATH)
    )

if __name__ == "__main__":
    asyncio.run(main())
