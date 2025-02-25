FROM ros:noetic

RUN apt-get update && \
    apt-get install -y wget mesa-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda.sh && \
    mkdir -p /root/.conda && \
    bash /root/miniconda.sh -b -p /root/miniconda3 && \
    rm -f miniconda.sh

ENV PATH=/root/miniconda3/bin:$PATH
COPY ./ssrl_environment.yml .
RUN conda env create -n ssrl --file /ssrl_environment.yml

COPY ssrl_entry.sh .

# xhost si:localuser:root
# docker run --rm -it --ipc=host --gpus all --net=host -v .:/workspace --volume=$HOME/.Xauthority:/root/.Xauthority:rw -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --privileged
