# Cameras

Structure of the code:
```
├── gopro
│   ├── live_test.py
│   ├── test.py
├── integrated
│   ├── live.py
│   ├── save_video.py
│   ├── test.py
├── outputs
│   ├── ...
├── README.md
└── requirements.txt
```


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