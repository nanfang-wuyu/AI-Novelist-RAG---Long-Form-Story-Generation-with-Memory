#!/bin/bash

docker build -t ai-novelist .

docker run -p 8000:8000 -p 7860:7860 ai-novelist