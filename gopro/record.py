"""
Record video of a preselected time, and put it into the outputs folder
Need to turn on the cam first (click on buttons of cam if not detected)
"""

import os
import asyncio
from open_gopro import WiredGoPro, constants
import httpx

OUTPUT_DIR = "./outputs"
TIME = 10

async def main():
    async with WiredGoPro() as gopro:
        print(f"Connecting to GoPro...")

        # To change parameters
        #gopro.http_setting.x.set(constants.X.Y)
        
        # Example: Set the shutter to ON (Start recording / Take photo) via HTTP
        # This completely bypasses BLE and WiFi.
        response = await gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)

        if response.ok:
            print(f"Successfully started GoPro!")
        else:
            print(f"Failed to start GoPro: {response.status}")

        await asyncio.sleep(TIME)

        # Example: Set the shutter to OFF
        await gopro.http_command.set_shutter(shutter=constants.Toggle.DISABLE)
        print(f"Stopped GoPro.")

        media_list_resp = await gopro.http_command.get_media_list()

        if not media_list_resp.ok:
            print("Failed to retrieve media list.")
            return

        media_data = media_list_resp.data.model_dump()

        if (not media_data) or ("media" not in media_data):
            print("No media found.")
            return

        latest_folder = media_data["media"][-1]
        folder_name = latest_folder["directory"]
        latest_file_info = latest_folder["file_system"][-1]
        full_filename = latest_file_info["filename"]
        latest_file = full_filename.split("/")[-1]

        print(f"Latest video found: {latest_file} in folder {folder_name}")

        # Verify if the outputs folder exists
        os.makedirs("./outputs", exist_ok=True)

        # Construct the download URL
        #download_url = f"http://10.5.5.9:8080/videos/DCIM/{folder_name}/{latest_file}"
        download_url = f"http://172.23.159.51:8080/videos/DCIM/{folder_name}/{latest_file}"
        output_path = os.path.join(OUTPUT_DIR, latest_file)

        print(f"Downloading {latest_file} to Jetson...")

        async with httpx.AsyncClient() as client:
            response = await client.get(download_url)
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                    print(f"Download complete! Saved to {output_path}")
            else:
                print(f"Failed to download video. HTTP Status: {response.status_code}")
                return

        # Launch video playback on Jetson
        abs_output_path = os.path.abspath(output_path)
        gst_cmd = (
            f"gst-launch-1.0 filesrc location={abs_output_path} ! "
            f"qtdemux name=demux demux.video_0 ! "
            f"h265parse ! "
            f"nvv4l2decoder ! "
            f"nv3dsink sync=true"
        )

        print("\nRunning GStreamer pipeline:\n")
        print(gst_cmd)

        os.system(gst_cmd)

if __name__ == "__main__":
    asyncio.run(main())
