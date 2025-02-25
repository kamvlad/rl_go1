#!/bin/bash

source /root/miniconda3/bin/activate
conda activate ssrl
cd /workspace
pip install -e submodules/free-dog-sdk
pip install -e submodules/ssrl/ssrl
