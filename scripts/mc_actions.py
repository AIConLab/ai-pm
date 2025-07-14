# File:mc_actions
# Desc: Class for defining expected actions for game events
from agents import Agent, Runner
import re

from rcon_client import MessageService, RCONClient
from mc_database import Database
from utils import load_config



class Actions:
    """Business logic for AI actions"""
    
    def __init__(self):
        self.rcon_client = RCONClient(password_file="/mc-data/.rcon-cli.env")
        self.message_service = MessageService(self.rcon_client)
        self.database = Database(db_path="/app/database/aipm.db")
        self.config = load_config("/app/config.toml")

    def handle_player_join(self, username):
        """Handle player join event"""
        print(f"🎮 Player joined: {username}")
        self.database.add_user(username)
        self.database.set_online(username, True)

    def handle_player_leave(self, username):
        """Handle player leave event"""
        print(f"👋 Player left: {username}")
        self.database.set_online(username, False)

    def handle_debug_command(self, username, command):
        """Handle @debug commands - SYSTEM COMMANDS ONLY"""
        command_lower = command.lower()
        
        debug_commands = {
            "help": "Show all available debug commands",
            "players": "List all online players", 
            "inv": "Show player inventory. Usage: @debug inv [playername]",
            "pos": "Show player position. Usage: @debug pos [playername]",
            "db": "Show database statistics",
            "sync": "Force database sync",
            "status": "Show system status"
        }
        
        # Handle help command
        if command_lower == 'help':
            help_lines = ["Available @debug commands:"]
            for cmd, desc in debug_commands.items():
                help_lines.append(f"• @debug {cmd} - {desc}")
            help_message = "\n".join(help_lines)
            self.message_service.send_private(username, help_message)
            return
        
        # System commands
        if command_lower == 'players':
            online_users = self.database.get_online_users()
            if online_users:
                names = [user['minecraft_username'] for user in online_users]
                response = f"Online players ({len(names)}): {', '.join(names)}"
            else:
                response = "No players online"
            self.message_service.send_private(username, response)
        
        elif command_lower.startswith('inv'):
            # Get inventory of specified player or self
            target = command.split()[-1] if len(command.split()) > 1 else username
            inventory = self.database.get_user_inventory(target)
            
            if inventory:
                items = [f"{item['item_type']} x{item['quantity']}" for item in inventory[:5]]  # First 5 items
                response = f"{target} inventory: {', '.join(items)}"
                if len(inventory) > 5:
                    response += f" (+{len(inventory)-5} more)"
            else:
                response = f"No inventory data for {target}"
            self.message_service.send_private(username, response)
            
        elif command_lower.startswith('pos'):
            # Get position of specified player or self
            target = command.split()[-1] if len(command.split()) > 1 else username
            online_users = self.database.get_online_users()
            target_user = next((u for u in online_users if u['minecraft_username'] == target), None)
            
            if target_user:
                x, y, z = target_user['current_x'], target_user['current_y'], target_user['current_z']
                response = f"{target} position: X={x:.1f}, Y={y:.1f}, Z={z:.1f}"
            else:
                response = f"Player {target} not found or offline"
            self.message_service.send_private(username, response)
        
        elif command_lower == 'db':
            try:
                all_users = self.database.get_all_users()
                online_count = len([u for u in all_users if u['is_online']])
                response = f"DB Stats: {len(all_users)} total users, {online_count} online, DB: {self.database.db_path}"
                self.message_service.send_private(username, response)
            except Exception as e:
                self.message_service.send_private(username, f"DB error: {str(e)}")
        
        elif command_lower == 'sync':
            response = "Database sync triggered (not implemented yet)"
            self.message_service.send_private(username, response)
        
        elif command_lower == 'status':
            online_users = self.database.get_online_users()
            all_users = self.database.get_all_users()
            
            status_lines = [
                f"System Status:",
                f"• Online players: {len(online_users)}",
                f"• Total registered: {len(all_users)}"
            ]
            
            if online_users:
                player_names = [u['minecraft_username'] for u in online_users]
                status_lines.append(f"• Active: {', '.join(player_names)}")
            
            response = "\n".join(status_lines)
            self.message_service.send_private(username, response)
        
        else:
            # Unknown debug command
            available = list(debug_commands.keys())
            error_msg = f"Unknown debug command '{command_lower}'. Available: {', '.join(available)}. Use '@debug help' for details."
            self.message_service.send_private(username, error_msg)


    def handle_aipm_command(self, username, command):
        """Handle @aipm commands - AI INQUIRIES ONLY"""

        help_message = """AIPM Assistant:
    I'm your AI project manager! Ask me:
    • Minecraft questions: "how do I craft redstone?"
    • Strategy advice: "what should we build first?"  
    • Project management: "how should we organize our team?"
    • Building tips: "best materials for a castle?"

    Just type your question after the command!"""

        command_clean = command.lower().strip()

        # Handle empty commands
        if not command_clean:
            self.message_service.send_private(username, "How can I help? Send your question after the command.")
            return

        # Handle help requests - FIX: Use string comparison, not list
        if command_clean == "help":
            self.message_service.send_private(username, help_message)
            return

        # All other commands go to AI
        self.get_ai_pm_response(username=username, command=command)
        

    def get_ai_pm_response(self, username="player", command=""):
        """Generate and send private AI response"""
        try:
            print(f"🤖 Processing @aipm command from {username}: '{command}'")
            
            agent = Agent(
                name="MinecraftProjectManager", 
                instructions=self.config["aipm"]["manager_agent"]["helper_instructions"]
            )
            
            result = Runner.run_sync(agent, f"Player {username} asks: {command}")
            print(f"🤖 AI Response: {result.final_output}")
            
            # Send private response
            if self.message_service.send_private(username, result.final_output):
                print(f"✅ AI response sent privately to {username}!")
            else:
                print("❌ Failed to send AI response")
                
        except Exception as e:
            print(f"❌ Error in ai_pm_response: {e}")
            self.message_service.send_private(username, "Sorry, I'm having trouble right now. Try again later!")