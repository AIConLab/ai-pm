#!/bin/bash

DOCKER_PATH="/root/ai-pm-mc-world-dev/.docker"

tmux new -s minecraft -d

tmux send-keys -t minecraft "cd $DOCKER_PATH" Enter
tmux send-keys -t minecraft "docker compose up minecraft --abort-on-container-exit" Enter