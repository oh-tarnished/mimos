# Mimos

Mimos 👾 is a simple, fast, and powerful animation framework build using blender for python 🐍.

- Recommended Editor: `Visual Studio Code`

## Setup

`clone this repository to get started`

- Setting up the development environment on visual studio code (locally)

  - `install blender` (recommended version: 3.2.2)
  - `install python` (recommended version: 3.10)

- Setting up the development environment on visual studio code (via docker)

  - `install docker`
  - `install visual studio code`
  - `install blender` (recommended version: 3.2.2)
  - `install python` (recommended version: 3.10)
  - Open the project folder in visual studio code
  - `install Remote - Containers extension for visual studio code from Microsoft`
  - `ctrl + p ` opens a drawer in visual studio code and select `open in container` from the dropdown menu for the first time to create a container for the project folder. or when installed remote containers extension, select `open in container` from the side alert pop-up menu.

Make sure you have python 3.10 installed on your system. To create virtual environment, run the following command

```
$ mimos.sh
```

Activate the environment using the following command:

```
$ source ./venv/bin/activate
```

## Project Structure

`Root`

```
.
├── animations
├── blender
├── client.py
├── create_env.sh
├── docker
│ └── Dockerfile.vscode.dev
├── engine
└── readme.md
```

`Engine`

```
engine
├── app
│   ├── __init__.py
│   ├── controllers
│   │   ├── __init__.py
│   │   └── controllers.py
│   ├── models
│   │   ├── __init__.py
│   │   └── models.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── service
│   │   ├── __init__.py
│   │   └── blender.py
│   └── utils
│       ├── __init__.py
│       └── config.py
├── main.py
├── readme.md
└── requirements.txt
```

## License: MIT

---

© 2022 Machani Robotics
