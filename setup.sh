#!/bin/bash

conda create -n novel_rag python=3.10 -y
conda activate novel_rag
pip install -r requirements.txt
# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
# CUDA 12.1
# conda install pytorch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 pytorch-cuda=12.1 -c pytorch -c nvidia
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128