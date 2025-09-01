#!/bin/bash

tmux kill-session -t minecraft 2>/dev/null
docker ps -q --filter "name=minecraft" | xargs -r docker kill

echo "Stopepd tmux and containers"