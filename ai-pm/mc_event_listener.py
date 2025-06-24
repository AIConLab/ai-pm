#!/usr/bin/env python3
# mc_event_listener.py - Event-based updates from log parsing only
import subprocess
import sys
import re
from mc_actions import Actions
from mc_database import Database

LOG_PATH = "/mc-data/logs/latest.log"
ADMIN_USERS = ["Loopking", "BT1013", "jc_cr"]

CHAT_PATTERN = r'\[.*?\] \[Async Chat Thread.*?\]: <(\w+)> (.*)'
AIPM_PATTERN = r'@aipm\s*(.*)'
JOIN_PATTERN = r'\[.*?\] \[Server thread/INFO\]: (\w+) joined the game'
LEAVE_PATTERN = r'\[.*?\] \[Server thread/INFO\]: (\w+) left the game'

def handle_player_join(db, username):
    """Handle player join event"""
    print(f"🎮 Player joined: {username}")
    db.add_user(username)
    db.set_online(username, True)

def handle_player_leave(db, username):
    """Handle player leave event"""
    print(f"👋 Player left: {username}")
    db.set_online(username, False)

def handle_aipm_command(actions, db, username, command):
    """Handle @aipm commands"""
    command_lower = command.lower()
    
    if command_lower == 'players':
        online_users = db.get_online_users()
        if online_users:
            names = [user['minecraft_username'] for user in online_users]
            response = f"Online players: {', '.join(names)}"
        else:
            response = "No players online"
    elif command_lower.startswith('inv'):
        # Get inventory of specified player or self
        target = command.split()[-1] if len(command.split()) > 1 else username
        inventory = db.get_user_inventory(target)
        
        if inventory:
            items = [f"{item['item_type']} x{item['quantity']}" for item in inventory[:5]]  # First 5 items
            response = f"{target} inventory: {', '.join(items)}"
            if len(inventory) > 5:
                response += f" (+{len(inventory)-5} more)"
        else:
            response = f"No inventory data for {target}"
        actions.message_service.send_private(username, response)
        
    elif command_lower.startswith('pos'):
        # Get position of specified player or self
        target = command.split()[-1] if len(command.split()) > 1 else username
        online_users = db.get_online_users()
        target_user = next((u for u in online_users if u['minecraft_username'] == target), None)
        
        if target_user:
            x, y, z = target_user['current_x'], target_user['current_y'], target_user['current_z']
            response = f"{target} position: X={x:.1f}, Y={y:.1f}, Z={z:.1f}"
        else:
            response = f"Player {target} not found or offline"
        actions.message_service.send_private(username, response)
        
    else:
        # Regular AI response
        actions.get_ai_pm_response(username=username, command=command)

def main():
    print("🤗 Starting event listener service 🤗")
    
    try:
        actions = Actions()
        db = Database()
        
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
                    handle_player_join(db, username)
                    
                    # Send welcome for admin users
                    if username in ADMIN_USERS:
                        actions.get_ai_welcome_greeting(username=username)
                    continue
                
                # Handle player leaves
                leave_match = re.search(LEAVE_PATTERN, line)
                if leave_match:
                    username = leave_match.group(1)
                    handle_player_leave(db, username)
                    continue
                
                # Handle chat with @aipm
                chat_match = re.search(CHAT_PATTERN, line)
                if chat_match:
                    username = chat_match.group(1)
                    message = chat_match.group(2)
                    
                    aipm_match = re.search(AIPM_PATTERN, message)
                    if aipm_match:
                        command_text = aipm_match.group(1).strip()
                        print(f"🤖 @aipm command from {username}: '{command_text}'")
                        handle_aipm_command(actions, db, username, command_text)
        
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