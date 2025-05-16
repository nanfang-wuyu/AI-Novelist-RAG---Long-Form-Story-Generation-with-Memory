### For CPU
FROM python:3.10-slim

# RUN apt-get update && apt-get install -y git curl libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt

# CMD ["bash", "scripts/start.sh"]

### For GPU

# FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# RUN apt-get update && apt-get install -y python3.10 python3-pip git curl

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app
RUN pip install --no-cache-dir --upgrade pip

COPY --chown=user . $HOME/app

RUN chmod +x scripts/start.sh

RUN pip3 install --upgrade pip
# RUN pip3 install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 --index-url https://download.pytorch.org/whl/cu121
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install -r requirements.txt

CMD ["bash", "scripts/start.sh"]
