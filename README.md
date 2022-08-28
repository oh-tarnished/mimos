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

#### Development

```
$ uvicorn app:app --reload
```

#### Production

```
$ python main.py
```

### Blender Client

Execute this command in `clients/blender` directory. To run the blender client after running mimos engine, execute the following command:

```
$ ./start-blender-client.sh -f <path to blend file> -a <animation name>
```

Animation name here is same as Toml file name in `engine/animations` folder

### License: MIT

---

© 2022 Machani Robotics
