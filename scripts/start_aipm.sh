# Create the session
tmux new -s event_listener -d

# Send the command to the session
tmux send-keys -t event_listener 'cd /root/ai-pm-jc-dev/.docker' Enter
tmux send-keys -t event_listener 'docker compose run --rm event_listener' Enter

# Attach to see it running
tmux attach -t event_listener


# Create the session
tmux new -s game_query -d

# Send the command to the session
tmux send-keys -t game_query 'cd /root/ai-pm-jc-dev/.docker' Enter
tmux send-keys -t game_query 'docker compose run --rm game_query' Enter

# Attach to see it running
tmux attach -t game_query


tmux new -s  game_query /root/ai-pm-jc-dev/.docker 'docker compose run --rm game_query'