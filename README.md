# Mimos

Mimos 👾 is a simple, fast, and powerful animation framework built for python 🐍.

> This has been tested and developed on linux systems only.

## Setup

`clone this repository to get started`

- Setting up the development environment on visual studio code (locally)

  - `install python` ([recommended version: 3.10.0](https://www.python.org/downloads/release/python-3100/))
  - `install blender` ([recommended version: 3.2.2](https://www.blender.org/download/releases/3-2/))
  - `install virtualenv`

Make sure you have python 3.10 installed on your system.

### Engine

Make sure `engine/animations` folder contains the required animations. Start the engine using the following command

#### Development

```
$ cd engine/
$ uvicorn app:app --reload
```

#### Production

```
$ cd engine/
$ python main.py
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
