# Mimos

Mimos 👾 is a simple, fast, and powerful animation framework built using Python 🐍.

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

To run Mimos, start the Engine first, followed by Blender Client.

### Engine

Make sure `engine/animations` folder contains the required animations. Execute these commands in `engine/` directory.
Start the engine using the following command

### Blender

- **Animation**

  To start Animation Server, run this

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

  > **_NOTE:_** Before starting the pose server, make sure camera is connected. And run `xhost +` in terminal.

  Start Openpose server using this command

  ```
  $ docker run --gpus all --net host --privileged -v "/tmp/.X11-unix:/tmp/.X11-unix" --device "/dev/video0:/dev/video0" public.ecr.aws/i8e8x2j1/machanirobotics:mimos-0.1.0
  ```

  To start Blender Client, run this(not functional yet)

  ```
  $ cd clients/blender/pose
  $ blender -y <PATH_TO_BLEND_FILE> -P poseoperator.py

  $ # To check openpose stream
  $ python3 streamclient.py

  ```

### License: MIT

---

© 2022 Machani Robotics
