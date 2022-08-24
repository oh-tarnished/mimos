# Mimos Engine

### Development

To create virtual environment, run the following command

```
$ ./create_venv.sh
```

Activate the environment using the following command (while in the engine folder):

```
$ source ./venv/bin/activate
```

To run a development version of the engine, run (after activating the environment)

```
$ uvicorn app:app --reload
```
