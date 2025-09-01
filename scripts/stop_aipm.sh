#!/bin/bash
# Kill tmux sessions
tmux kill-session -t event_listener 2>/dev/null
tmux kill-session -t game_query 2>/dev/null

# Kill any running containers by name pattern
docker ps -q --filter "name=event_listener" | xargs -r docker kill
docker ps -q --filter "name=game_query" | xargs -r docker kill

echo "Stopped tmux sessions and killed containers"