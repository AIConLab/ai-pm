#!/bin/bash
# Continuous backup loop in tmux

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting backup check..."
    
    cd /root/ai-pm-mc-world-dev
    git add .
    
    if ! git diff --staged --quiet; then
        echo "Changes detected, committing..."
        git commit -m "Auto-backup: $(date '+%Y-%m-%d %H:%M:%S')"
        git push origin feature/minecraft-world-dev
        echo "✅ Backup completed successfully"
    else
        echo "No changes to backup"
    fi
    
    echo "Next backup in 30 minutes..."
    echo "---"
    
    # Sleep for 30 minutes
    sleep 1800
done
