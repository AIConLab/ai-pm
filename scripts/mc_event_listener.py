#!/usr/bin/env python3
# mc_event_listener.py - Event-based updates from log parsing only
import subprocess
import sys
import os 
import re
import tomllib
from mc_actions import Actions
from mc_database import Database

LOG_PATH = "/mc-data/logs/latest.log"
ADMIN_USERS = ["Loopking", "BT1013", "jc_cr"]

CHAT_PATTERN = r'\[.*?\] \[Async Chat Thread.*?\]: <(\w+)> (.*)'
AIPM_PATTERN = r'@aipm\s*(.*)'  # Added missing pattern
DEBUG_PATTERN = r'@debug\s*(.*)'
JOIN_PATTERN = r'\[.*?\] \[Server thread/INFO\]: (\w+) joined the game'
LEAVE_PATTERN = r'\[.*?\] \[Server thread/INFO\]: (\w+) left the game'

def load_config(config_path="config.toml"):
    """Load all params from config file"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found")
    
    with open(config_path, 'rb') as f:
        return tomllib.load(f)

def handle_player_join(db, actions, username, config):
    """Handle player join event"""
    print(f"🎮 Player joined: {username}")
    db.add_user(username)
    db.set_online(username, True)
    
    # Send welcome for team members
    if username in config["aipm_team"]["members"]:
        actions.get_ai_welcome_greeting(username=username)

def handle_player_leave(db, username):
    """Handle player leave event"""
    print(f"👋 Player left: {username}")
    db.set_online(username, False)

def main():
    print("🤗 Starting event listener service 🤗")
    
    try:
        actions = Actions()
        db = Database()
        config = load_config()
        
        # Start tail process for log monitoring
        tail_process = subprocess.Popen(
            ['tail', '-F', '-n', '0', LOG_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        print(f"📡 Monitoring {LOG_PATH} for events...")
        
        for line in iter(tail_process.stdout.readline, ''):
            line = line.strip()
            
            if line:
                # Handle player joins
                join_match = re.search(JOIN_PATTERN, line)
                if join_match:
                    username = join_match.group(1)
                    handle_player_join(db, actions, username, config)
                    continue
                
                # Handle player leaves
                leave_match = re.search(LEAVE_PATTERN, line)
                if leave_match:
                    username = leave_match.group(1)
                    handle_player_leave(db, username)
                    continue
                
                # Handle chat messages (both @debug and @aipm)
                chat_match = re.search(CHAT_PATTERN, line)
                if chat_match:
                    username = chat_match.group(1)
                    message = chat_match.group(2)
                    
                    # Check for @debug commands first (admin only)
                    debug_cmd_match = re.search(DEBUG_PATTERN, message)
                    if debug_cmd_match and username in ADMIN_USERS:
                        command_text = debug_cmd_match.group(1).strip()
                        print(f"🔧 @debug command from {username}: '{command_text}'")
                        actions.handle_debug_command(db, username, command_text)
                        continue
                    
                    # Check for @aipm commands (team members only)
                    aipm_cmd_match = re.search(AIPM_PATTERN, message)
                    if aipm_cmd_match and username in config["aipm_team"]["members"]:
                        command_text = aipm_cmd_match.group(1).strip()
                        print(f"🤖 @aipm command from {username}: '{command_text}'")
                        actions.handle_aipm_command(db, username, command_text)
                        continue
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'tail_process' in locals():
            tail_process.terminate()
            tail_process.wait()
        print("✅ Event listener stopped")

if __name__ == "__main__":
    main()