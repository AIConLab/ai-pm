#!/usr/bin/env python3
# mc_event_listener.py - Event-based updates from log parsing only
import subprocess
import sys
import os 
import re
from mc_actions import Actions
from utils import load_config

CHAT_PATTERN = r'\[.*?\] \[Async Chat Thread.*?\]: <(\w+)> (.*)'
AIPM_PATTERN = r'@aipm\s*(.*)'
DEBUG_PATTERN = r'@debug\s*(.*)'
JOIN_PATTERN = r'\[.*?\] \[Server thread/INFO\]: (\w+) joined the game'
LEAVE_PATTERN = r'\[.*?\] \[Server thread/INFO\]: (\w+) left the game'


def is_admin_user(username: str, config: dict) -> bool:
    return username in config["minecraft"]["admins"]


def is_in_aipm_team(username: str, config: dict) -> bool:
    return username in config["aipm"]["members"]


def main():
    print("🤗 Starting event listener service 🤗")
    
    try:
        # Load config with better error handling
        print("📄 Loading configuration...")
        config = load_config()
        print("✅ Configuration loaded successfully")
        
        # Initialize actions

        actions = Actions(config=config)

        LOG_PATH = config["minecraft"]["log_path"]
        print(f"📁 Log path: {LOG_PATH}")

        # Check if log file exists
        if not os.path.exists(LOG_PATH):
            raise FileNotFoundError(f"Minecraft log file not found: {LOG_PATH}")

        # Start tail process for log monitoring
        # We use this since minecraft makes a new log file everyday.
        # Popen we can monitor even if new file is made
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
                    if is_in_aipm_team(username, config):
                        actions.handle_player_join(username)
                    continue
                
                # Handle player leaves
                leave_match = re.search(LEAVE_PATTERN, line)
                if leave_match:
                    username = leave_match.group(1)

                    if is_in_aipm_team(username, config):
                        actions.handle_player_leave(username)
                    continue
                
                # Handle chat messages (both @debug and @aipm)
                chat_match = re.search(CHAT_PATTERN, line)
                if chat_match:
                    username = chat_match.group(1)
                    message = chat_match.group(2)
                    
                    # Check for @debug commands first (admin only)
                    debug_cmd_match = re.search(DEBUG_PATTERN, message)
                    if debug_cmd_match and is_admin_user(username, config):
                        command_text = debug_cmd_match.group(1).strip()
                        print(f"🔧 @debug command from {username}: '{command_text}'")
                        actions.handle_debug_command(username, command_text)
                        continue
                    
                    # Check for @aipm commands (team members only)
                    aipm_cmd_match = re.search(AIPM_PATTERN, message)
                    if aipm_cmd_match and is_in_aipm_team(username, config):
                        command_text = aipm_cmd_match.group(1).strip()
                        print(f"🤖 @aipm command from {username}: '{command_text}'")
                        actions.handle_aipm_command(username, command_text)
                        continue

                    # TODO: round start event, round progress event

    except KeyboardInterrupt:
        print("\n🛑 Stopping...")

    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        sys.exit(1)
        
    except ValueError as e:
        # This will catch our TOML parsing errors with detailed info
        print(f"❌ Configuration Error: {e}")
        sys.exit(1)
        
    except RuntimeError as e:
        # This will catch other config loading errors
        print(f"❌ Runtime Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        if 'tail_process' in locals():
            tail_process.terminate()
            tail_process.wait()
        print("✅ Event listener stopped")

if __name__ == "__main__":
    main()