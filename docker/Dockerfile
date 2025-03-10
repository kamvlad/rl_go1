FROM ros:noetic

RUN apt-get update && \
    apt-get install -y wget mesa-utils python3-pip python-is-python3 && \
    wget -qO - https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub | apt-key add - && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y libcudnn8=8.9.7.29-1+cuda12.2 cuda-toolkit && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install jaxlib==0.4.13+cuda12.cudnn89 -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html && \
    pip install optax==0.1.7 jax==0.4.13 \
                dill==0.3.7 hydra-core==1.3.2 matplotlib numpy==1.24.4 omegaconf==2.3.0 submitit==1.4.6 wandb==0.15.5 pynput cbor2 plotly \
                absl-py dm_env etils flask flask_cors flax grpcio gym jaxopt jinja2 mujoco Pillow pytinyrenderer scipy tensorboardX trimesh==3.9.35 typing-extensions

COPY ssrl_entry.sh .