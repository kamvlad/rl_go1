xhost si:localuser:root

docker run --rm -it --ipc=host --gpus all --net=host -v .:/workspace --volume=$HOME/.Xauthority:/root/.Xauthority:rw -e NVIDIA_DRIVER_CAPABILITIES=all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --privileged ros-conda bash


# Before start in host
git submodule update --init --recursive

# Start in docker
source /ssrl_entry.sh


# Build
catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3

# Use
source devel/setup.sh

# Run
rosrun ssrl_ros_go1 controller.py