#!/bin/bash

# Create the event_listener session
tmux new -s event_listener -d

# Send the command to the session
tmux send-keys -t event_listener 'cd /root/ai-pm-jc-dev/.docker' Enter
tmux send-keys -t event_listener 'docker compose run --rm event_listener' Enter

# Create the game_query session
tmux new -s game_query -d

# Send the command to the session
tmux send-keys -t game_query 'cd /root/ai-pm-jc-dev/.docker' Enter
tmux send-keys -t game_query 'docker compose run --rm game_query' Enter

echo "Started event_listener and game_query in tmux sessions"
echo "Check status with: tmux list-sessions"
echo "Attach to view logs: tmux attach -t event_listener or game_query "