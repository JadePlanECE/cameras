# Cameras

The aim of this repo is to compare 2 types of camera (GoPro and built-int camera / integrated camera)


## Virtual Environment

Install Python on your system if you haven't already.
```
apt install python3.10-venv
```

Create a virtual environment (rename the envirnment as you want).
```
python3 -m venv cam
```

Enter the environment.
```
source cam/bin/activate
```

Install pip (if not already here).
```
sudo apt-get install python3-pip
```

Then install all the required libraries.
```
pip install -r requirements.txt
```


**Warning:** To desactivate the virtual environment, run the command.
```
deactivate
```


**Warning:** To destroy the environment.
```
rm -rf cam
```

## Launch comparaison of cameras

Run the following command.
```
python cameras_comparaison.py
```

You can also add arguments:
- Width of the cameras (default = 1280) `--width`
- Height of the cameras (default = 1920) `--height`
- Frame Per Second of the cameras (default = 30) `--fps`
- Field Of View of the GoPro (default = "linear") `--fov`

- Bitrate of the cameras, if is None then calculated automatically (default = None) `--bitrate` (not of use)
- Speed Preset of the built-in camera (default = "veryfast") `--speed-preset` (not of use)
