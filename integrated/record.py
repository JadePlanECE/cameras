"""
Record video of a preselected time, and put it into the outputs folder
"""

import os
import time
import subprocess

OUTPUT_DIR = "./outputs"
TIME = 10

def main():
    # 1. Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate a unique filename using a timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"integrated_{timestamp}.mp4"
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    print(f"Recording from integrated camera for {TIME} seconds...")
    print(f"Target path: {output_path}")

    # 2. GStreamer pipeline to record from /dev/video0 using Jetson hardware encoding
    # We use qtmux to pack the raw H264 stream safely into an MP4 container.
    record_cmd = (
        f"gst-launch-1.0 -e "
        f"v4l2src device=/dev/video0 num-buffers={TIME * 30} ! "
        f"video/x-h264,width=1920,height=1080,framerate=30/1 ! "
        f"h264parse ! "
        f"qtmux ! "
        f"filesink location={output_path}"
    )

    try:
        # Run the recording pipeline and wait for it to complete
        proc = subprocess.Popen(record_cmd, shell=True)
        proc.wait()
        print(f"Recording complete! Saved to {output_path}")
    except KeyboardInterrupt:
        proc.terminate()
        print("Recording interrupted by user.")
        return

    # 3. Launch video playback on Jetson using hardware acceleration
    # Get the absolute path to mimic your GoPro script structure
    abs_output_path = os.path.abspath(output_path)
    
    playback_cmd = (
        f"gst-launch-1.0 filesrc location={abs_output_path} ! "
        f"qtdemux name=demux demux.video_0 ! "
        f"h264parse ! "
        f"avdec_h264 ! "
        f"videoconvert ! "
        f"autovideosink sync=true"
    )

    print("\nRunning GStreamer playback pipeline:\n")
    print(playback_cmd)

    try:
        playback_proc = subprocess.Popen(playback_cmd, shell=True)
        playback_proc.wait()
    except KeyboardInterrupt:
        playback_proc.terminate()
        print("Playback stopped.")

if __name__ == "__main__":
    main()
