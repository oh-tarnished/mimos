# Mimos

Mimos 👾 is a simple, fast, and powerful animation framework built for python 🐍.

> This has been tested and developed on linux systems only.

## Setup

`clone this repository to get started`

- Setting up the development environment on visual studio code (locally)

  - `install blender` (recommended version: 3.2.2)
  - `install python` (recommended version: 3.10)
  - `install virtualenv`

Make sure you have python 3.10 installed on your system.

### Engine

To install Python 3.10.0, run the following command

```
$ cd engine
$ ./install_py.sh
```

To create virtual environment, run the following command

```
$ ./create_venv.sh
```

Activate the environment using the following command (while in the engine folder):

```
$ source ./venv/bin/activate
```

## Run

Make sure `engine/animations` folder contains the required animations. Start the engine using the following command

```
$ cd engine
$ ./mimos.sh
```

### Blender client

To run the blender client after running mimos engine, run the following command:

```
$ cd clients/blender
$ ./start-blender-client.sh -f <path to blend file> -a <animation name>
```

### License: MIT

---

© 2022 Machani Robotics
