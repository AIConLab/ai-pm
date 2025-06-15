#!/usr/bin/env python3
import os
import time
from mc_actions import Actions

LOG_PATH = "/mc-data/logs/latest.log"
ADMIN_USERS = ["Loopking", "BT1013", "jc_cr"]

def main():

    if not os.path.exists(LOG_PATH):
        print(f"Log file not found: {LOG_PATH}")
        return
        
    print("🤗 Starting event listener 🤗")
        
    last_position = os.path.getsize(LOG_PATH)
    print(f"Starting monitoring from position: {last_position}")
    
    try:
        action = Actions()

        while True:
            current_size = os.path.getsize(LOG_PATH)
            
            if current_size > last_position:
                with open(LOG_PATH, 'r') as f:
                    f.seek(last_position)
                    new_lines = f.readlines()
                    last_position = current_size
                    
                    for line in new_lines:
                        # Check for any admin joining
                        for user in ADMIN_USERS:
                            if f"{user} joined the game" in line:
                                action.ai_welcome_greeting(username=user)
                                break  # Only trigger once per line
            
            time.sleep(1) # check every sec
            
    except KeyboardInterrupt:
        print("\nStopping...")

if __name__ == "__main__":
    main()