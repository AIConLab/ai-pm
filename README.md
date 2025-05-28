# ai-pm

AI PM project source code

## Minecraft

To start a minecraft server instance:
```
tmux new-session -d -s minecraft
tmux send-keys -t minecraft 'docker compose up minecraft --remove-orphans --abort-on-container-exit' Enter
```

