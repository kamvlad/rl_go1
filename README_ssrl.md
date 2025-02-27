# Before start on host
```bash
git submodule update --init --recursive
```

# Build docker
Inside dir ```rl_go1/docker``` run
```bash
docker build -t ros-jax-gpu .
```
# Start Docker
Inside dir: ```rl_go1```

```bash
xhost si:localuser:root
docker run --rm -it --ipc=host --gpus all --net=host -v .:/workspace --volume=$HOME/.Xauthority:/root/.Xauthority:rw -e NVIDIA_DRIVER_CAPABILITIES=all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --privileged ros-jax-gpu bash
```

# After docker started init env
```bash
source /ssrl_entry.sh
cd ssrl_ws
```

# Build ros workspace
```bash
cd /workspace/ssrl_ws
catkin_make
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