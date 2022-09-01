## Openpose with Blender

### Deployment

Starts the pose stream client at TCP port 6666

```
$ python3 streamclient.py
```

To run blender's pose client

```
$ blender -y ../../blendfiles/Ria.blend -P poseoperator.py
```

To run open-pose server, check out this server repo
