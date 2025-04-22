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

# SSRL Hardware using simulation setup
Start simulation and supply nodes in docker container
```bash
roslaunch ssrl_ros_go1 support_nodes_sim.launch
```

Start controller in same container in "/workspace" folder:
```bash
source /ros_entrypoint.sh
source devel/setup.sh
rosrun ssrl_ros_go1 scripts/controller.py
```

Or one-liner from root:
```bash
source ros_entrypoint.sh && source workspace/ssrl_ws/devel/setup.sh && cd workspace/ssrl_ws/ && rosrun ssrl_ros_go1 /workspace/ssrl_ws/src/ssrl_ros_go1/scripts/controller.py
```

Train:
```bash
python src/ssrl_ros_go1/scripts/train.py run_name=run_name
```