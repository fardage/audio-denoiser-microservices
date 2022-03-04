docker run -p 80:8080 -d --mount type=bind,source=/home/ubuntu/shared_dir,target=/shared_dir --gpus all  -v : nvidia-maxine-wrapper:latest
