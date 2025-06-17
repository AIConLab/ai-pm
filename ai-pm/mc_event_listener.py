#!/usr/bin/env python3
# mc_event_listener.py - Using tail -F for log rotation handling
import subprocess
import sys
from mc_actions import Actions

LOG_PATH = "/mc-data/logs/latest.log"
ADMIN_USERS = ["Loopking", "BT1013", "jc_cr"]

def main():
    print("🤗 Starting event listener (using tail -F) 🤗")
    
    try:
        action = Actions()
        
        # Start tail -F process
        # -F follows by name and handles rotation
        # -n 0 means start from end (don't show existing lines)
        tail_process = subprocess.Popen(
            ['tail', '-F', '-n', '0', LOG_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1  # Line buffered
        )
        
        print(f"📡 Monitoring {LOG_PATH} with tail -F...")
        
        # Read lines as they come in
        for line in iter(tail_process.stdout.readline, ''):
            line = line.strip()
            
            if line:  # Skip empty lines
                # Check for any admin joining
                for user in ADMIN_USERS:
                    if f"{user} joined the game" in line:
                        print(f"🎮 Detected {user} joining!")
                        action.ai_welcome_greeting(username=user)
                        break  # Only trigger once per line
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        if 'tail_process' in locals():
            tail_process.terminate()
            tail_process.wait()
            print("✅ Tail process terminated")

if __name__ == "__main__":
    main()