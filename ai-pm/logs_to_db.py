#!/usr/bin/env python3
import os
import time

LOG_PATH = "/app/data/latest.log"

def main():
    print("Watching for jc_cr...")
    
    if not os.path.exists(LOG_PATH):
        print(f"Log file not found: {LOG_PATH}")
        return
        
    last_position = os.path.getsize(LOG_PATH)
    print(f"Starting monitoring from position: {last_position}")
    
    try:
        while True:
            current_size = os.path.getsize(LOG_PATH)
            
            if current_size > last_position:
                with open(LOG_PATH, 'r') as f:
                    f.seek(last_position)
                    new_lines = f.readlines()
                    last_position = current_size
                    
                    for line in new_lines:
                        if "jc_cr joined the game" in line:
                            print("🎮 jc_cr joined!")
            
            time.sleep(0.5)  # Check twice per second
            
    except KeyboardInterrupt:
        print("\nStopping...")

if __name__ == "__main__":
    main()