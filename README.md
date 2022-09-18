# Mimos

![](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![](https://img.shields.io/badge/Blender-F5792A.svg?style=for-the-badge&logo=Blender&logoColor=white)
![](https://img.shields.io/badge/ZeroMQ-DF0000.svg?style=for-the-badge&logo=ZeroMQ&logoColor=white)
![](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white)

Mimos 👾 is a simple, fast, and powerful animation framework built using Python.
> This has been developed and tested on Linux systems(Ubuntu) only.

## Setup

`clone this repository to get started`

- Setting up the development environment on visual studio code (locally)

  - `install python` ([recommended version: 3.10.0](https://www.python.org/downloads/release/python-3100/))
  - `install blender` ([recommended version: 3.2.2](https://www.blender.org/download/releases/3-2/))
  - `install virtualenv`

To run blender from terminal, add the following command to ~/.bashrc or ~/.profile pointing to the directory with Blender’s binary:

```
$ export PATH=/path/to/blender/directory:$PATH
```

Make sure you have **Python 3.10** installed on your system. Also, **Blender-as-Python**(bpy) module is required & can be installed with [this wheel file](https://drive.google.com/drive/folders/1y9VGD_-fZwuAUEcKxiCc2DUrJqjhsJIR?usp=sharing).

### Blender

- **Animation**

  > **_NOTE:_** Make sure **engine/animations** folder contains the required animations. Execute these commands in **engine/** directory.

  Start Animation Server, run this

  ```
  $ # Development Mode
  $ uvicorn app:app --reload

  $ # Production Mode
  $ python3.10 main.py
  ```

  To start Blender Client, run this

  ```
  $ cd clients/blender/animation
  $ blender -y <PATH_TO_BLEND_FILE> -P animoperator.py -- <ANIMATION_NAME>
  ```

  Animation name here is same as TOML file name in `engine/animations` folder

- **Pose**

  > **_NOTE:_** Before starting the pose server, make sure camera is connected. And run `xhost +` in terminal. Also install [pyzmq](https://pypi.org/project/pyzmq/) in Blender's Python Environment.

  Start Openpose server using this command

  ```
  $ docker run --gpus all --net host --privileged -v "/tmp/.X11-unix:/tmp/.X11-unix" --device "/dev/video0:/dev/video0" public.ecr.aws/i8e8x2j1/machanirobotics:mimos-0.1.0
  ```

  To start Blender Client, run this

  ```
  $ cd clients/blender/pose
  $ blender -y <PATH_TO_BLEND_FILE> -P poseoperator.py

  $ # To check openpose stream
  $ python3 streamclient.py

  ```

### License: MIT

---

© 2022 Machani Robotics
