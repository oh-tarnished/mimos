# Mimos Engine

## Development

- To run a development version of the engine, run (after activating the environment)

  ```
  $ uvicorn app.api:app --reload
  ```

- To run the blender animation

  ```
  $ blender -y <PATH_TO_BLEND_FILE> -P engine/app/service/blender.py -- <ANIMATION_NAME>
  ```

## Production

To run the production version of the engine run (after activating the environment)

```
python3 main.py
```

## License: MIT

---

© 2022 Machani Robotics
