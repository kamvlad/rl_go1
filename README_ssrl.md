# Before start on host
```bash
git submodule update --init --recursive
```

# Start Docker

```bash
xhost si:localuser:root
docker run --rm -it --ipc=host --gpus all --net=host -v .:/workspace --volume=$HOME/.Xauthority:/root/.Xauthority:rw -e NVIDIA_DRIVER_CAPABILITIES=all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --privileged ros-conda bash
```

# After docker started init env
```bash
source /ssrl_entry.sh
cd ssrl_ws
```

# Build
```bash
catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3
```

# Use ros env
```bash
source devel/setup.sh
```

# Run
Run controller node
```bash
rosrun ssrl_ros_go1 controller.py
```