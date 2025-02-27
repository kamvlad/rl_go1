#!/bin/bash

source /root/miniconda3/bin/activate
conda activate rma
cd /workspace
pip install -e submodules/free-dog-sdk
