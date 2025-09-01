# File:mc_actions
# Desc: Class for defining expected actions for game events. Is the central locaiton for database operations.

from agents import Agent, Runner
import re
import os

import json
from datetime import datetime

from rcon_client import MessageService, RCONClient
from mc_database import Database, UserDataService
from utils import load_config

class Actions:
    """Business logic for AI actions"""
    
    def __init__(
        self, 
        config):

        self.rcon_client = RCONClient(password_file="/mc-data/.rcon-cli.env")
        self.message_service = MessageService(self.rcon_client)

        # Load db without init tables since mc_game_query already handles that
        self.db = Database(
            db_path="/app/database/aipm.db",
            user_config=config
            )

        self.user_data_service = UserDataService(db=self.db)

        self.config = config

        self.last_planned_round = None

    def handle_player_join(self, username):
        """Handle player join event"""
        print(f"🎮 Player joined: {username}")
        self.user_data_service.add_user(username)
        self.user_data_service.set_online(username, True)

    def handle_player_leave(self, username):
        """Handle player leave event"""
        print(f"👋 Player left: {username}")
        self.user_data_service.set_online(username, False)

    def handle_debug_command(self, username, command):
        """Handle @debug commands - SYSTEM COMMANDS ONLY"""
        command_lower = command.lower()
        
        debug_commands = {
            "help": "Show all available debug commands",
            "players": "List all online players", 
            "inv": "Show player inventory. Usage: @debug inv [playername]",
            "pos": "Show player position. Usage: @debug pos [playername]",
            "database": "Show database statistics",
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
            online_users = self.user_data_service.get_online_users()
            if online_users:
                names = [user['minecraft_username'] for user in online_users]
                response = f"Online players ({len(names)}): {', '.join(names)}"
            else:
                response = "No players online"
            self.message_service.send_private(username, response)
        
        elif command_lower.startswith('inv'):
            # Get inventory of specified player or self
            target = command.split()[-1] if len(command.split()) > 1 else username
            inventory = self.user_data_service.get_user_inventory(target)
            
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
            online_users = self.user_data_service.get_online_users()
            target_user = next((u for u in online_users if u['minecraft_username'] == target), None)
            
            if target_user:
                x, y, z = target_user['current_x'], target_user['current_y'], target_user['current_z']
                response = f"{target} position: X={x:.1f}, Y={y:.1f}, Z={z:.1f}"
            else:
                response = f"Player {target} not found or offline"
            self.message_service.send_private(username, response)
        
        elif command_lower == 'database':
            try:
                all_users = self.user_data_service.get_all_users()
                online_count = len([u for u in all_users if u['is_online']])
                response = f"user_data_service Stats: {len(all_users)} total users, {online_count} online, user_data_service: {self.user_data_service.user_data_service_path}"
                self.message_service.send_private(username, response)
            except Exception as e:
                self.message_service.send_private(username, f"user_data_service error: {str(e)}")
        
        elif command_lower == 'sync':
            response = "Database sync triggered (not implemented yet)"
            self.message_service.send_private(username, response)
        
        elif command_lower == 'status':
            online_users = self.user_data_service.get_online_users()
            all_users = self.user_data_service.get_all_users()
            
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
        self.get_ai_helper_response(username=username, command=command)
        
    
    def get_ai_helper_response(self, username="player", command=""):
        """Generate and send private AI response"""
        try:
            print(f"🤖 Processing @aipm command from {username}: '{command}'")
            
            agent = Agent(
                name="MinecraftProjectManager", 
                instructions=self.config["aipm"]["helper_agent"]["helper_instructions"]
            )
            
            result = Runner.run_sync(agent, f"Player {username} asks: {command}")
            print(f"🤖 AI Response: {result.final_output}")
            
            # Send private response
            if self.message_service.send_private(username, result.final_output):
                print(f"✅ AI response sent privately to {username}!")
            else:
                print("❌ Failed to send AI response")
                
        except Exception as e:
            print(f"❌ Error in ai_helper_response: {e}")
            self.message_service.send_private(username, "Sorry, I'm having trouble right now. Try again later!")

    
    def handle_aipm_logic(self, round_number: int):
        """
        Handles the AIPM agent syncing if the current round is an AIPM one.
        Only generates plan once per round.
        """
        try:
            # 10 is the tutorial round
            aipm_rounds = [1, 4, 7, 10]

            if round_number in aipm_rounds:
                # Check if we've already generated a plan for this round
                if self.last_planned_round == round_number:
                    print(f"⏭️  Plan already generated for AIPM Round {round_number} - Skipping")
                    return
                
                print(f"🤖 AIPM Round {round_number} detected! Generating new plan...")
                
                # Get high level plan from AI Planner
                plan_msg = self.get_aipm_plan()
                
                if plan_msg:
                    # Get personnel specific plans from AI Manager
                    self.send_aipm_plan(high_level_plan_msg=plan_msg)
                    
                    # Mark this round as planned
                    self.last_planned_round = round_number
                    
                    print(f"✅ AIPM Round {round_number} management complete! Plan generated once.")
                else:
                    print(f"❌ Failed to generate plan for AIPM Round {round_number}")
            else:
                print(f"ℹ️  Round {round_number} is not an AIPM round (1,4,7)")

                # Reset last planned
                self.last_planned_round = None

        except Exception as e:
            print(f"❌ Error in AIPM logic for round {round_number}: {e}")
            import traceback
            traceback.print_exc()

    def get_aipm_plan(self):
        """
        Calls the planning agent, a high level reasoning planning agent,
        to create the optimal high level plan to complete the structure in
        min time
        
        Injects:
        - prompt from config
        - round data from RoundData Table

        Output:
        - High Level Plan str

        High level plan is saved as a timestamped file for debugging
        """
        try:
            print("🧠 Generating AIPM high-level plan...")
            
            # Get current round data from database
            round_data = self._get_current_round_data()
            if not round_data:
                print("❌ No current round data found")
                return None
            
            # Get structure requirements
            structure_requirements = self._get_structure_requirements(round_data['current_round'])
            
            # Get player information
            player_data = self._get_player_data()
            
            # Get resource area data
            resource_data = self._get_resource_area_data()
            
            # Get processing area data  
            processing_data = self._get_processing_area_data()
            
            # Get map locations
            map_locations = self._get_map_locations()
            
            # Format the planner prompt
            formatted_prompt = self.config["aipm"]["planner_agent"]["planner_prompt"].format(
                round_number=round_data['current_round'],
                build_area_xyz=map_locations.get('build_area', [0, 0, 0]),
                resource_area_xyz=map_locations.get('resource_area', [0, 0, 0]),
                processing_area_xyz=map_locations.get('processing_area', [0, 0, 0]),
                structure_name=f"Structure {round_data['current_round']}",
                block_requirements=structure_requirements,
                active_players=player_data['active_players'],
                player_positions=player_data['player_positions'],
                player_inventories=player_data['player_inventories'],
                resource_area_items=resource_data,
                processing_area_items=processing_data
            )
            
            # Create planning agent
            planner_agent = Agent(
                name="AIPM_Planner",
                instructions=self.config["aipm"]["planner_agent"]["planner_system_prompt"],
                model=self.config["aipm"]["planner_agent"]["model"]
            )
            
            # Run the planner
            print(f"🤖 Running planner for Round {round_data['current_round']}")
            result = Runner.run_sync(planner_agent, formatted_prompt)
            high_level_plan = result.final_output
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            plan_filename = f"aipm_plan_round_{round_data['current_round']}_{timestamp}.txt"
            
            output_dir = "/app/database/logs"
            os.makedirs(output_dir, exist_ok=True)
            
            output_file = os.path.join(output_dir, plan_filename)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"AIPM High-Level Plan - Round {round_data['current_round']}\n")
                f.write(f"Generated at: {timestamp}\n")
                f.write("=" * 50 + "\n\n")
                f.write(high_level_plan)
            
            print(f"✅ High-level plan generated and saved to {output_file}")
            return high_level_plan
            
        except Exception as e:
            print(f"❌ Error generating AIPM plan: {e}")
            import traceback
            traceback.print_exc()
            return None


    def send_aipm_plan(self, high_level_plan_msg: str):
        """
        Given a high level plan, breaks down the plan
        as direct instructions for each player on the team.
        Then uses rcon to announce instructions to server for 
        players to read.

        Stores instructions as timestamped file for debugging
        """
        try:
            if not high_level_plan_msg:
                print("❌ No high-level plan provided")
                return
                
            print("📋 Converting plan to player-specific instructions...")
            
            # Get current round and player data
            round_data = self._get_current_round_data()
            if not round_data:
                print("❌ No current round data found")
                return
                
            player_data = self._get_player_data()
            structure_requirements = self._get_structure_requirements(round_data['current_round'])
            
            # Format the manager prompt
            formatted_prompt = self.config["aipm"]["manager_agent"]["manager_start_prompt"].format(
                round_number=round_data['current_round'],
                strategic_plan=high_level_plan_msg,
                player_status=player_data['active_players'],
                player_positions=player_data['player_positions'], 
                player_inventories=player_data['player_inventories'],
                structure_name=f"Structure {round_data['current_round']}"
            )
            
            # Create manager agent
            manager_agent = Agent(
                name="AIPM_Manager",
                instructions=self.config["aipm"]["manager_agent"]["manager_system_prompt"],
                model=self.config["aipm"]["manager_agent"]["model"]
            )
            
            # Run the manager
            print(f"🤖 Running manager for Round {round_data['current_round']}")
            result = Runner.run_sync(manager_agent, formatted_prompt)
            player_instructions = result.final_output
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            instructions_filename = f"aipm_instructions_round_{round_data['current_round']}_{timestamp}.txt"
            
            output_dir = "/app/database/logs"
            os.makedirs(output_dir, exist_ok=True)
            
            output_file = os.path.join(output_dir, instructions_filename)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"AIPM Player Instructions - Round {round_data['current_round']}\n")
                f.write(f"Generated at: {timestamp}\n")
                f.write("=" * 50 + "\n\n")
                f.write("HIGH-LEVEL PLAN:\n")
                f.write(high_level_plan_msg)
                f.write("\n\n" + "=" * 50 + "\n\n")
                f.write("PLAYER INSTRUCTIONS:\n")
                f.write(player_instructions)
            
            # Send instructions to all AIPM team members via broadcast
            print("📢 Broadcasting AIPM instructions to team...")
            
            # First send a header message
            header_msg = f"🤖 AIPM ROUND {round_data['current_round']} - AI PROJECT MANAGER"
            self.message_service.send_broadcast(header_msg)
            
            # Then send the instructions
            self.message_service.send_broadcast(player_instructions)
            
            print(f"✅ Instructions generated and sent! Saved to {instructions_filename}")
            
        except Exception as e:
            print(f"❌ Error sending AIPM plan: {e}")
            import traceback
            traceback.print_exc()

    # Helper methods for data retrieval
    def _get_current_round_data(self):
        """Get current round information from database"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT round_id, current_round, last_updated 
                    FROM RoundData 
                    ORDER BY last_updated DESC 
                    LIMIT 1
                """)
                result = cursor.fetchone()
                return dict(result) if result else None
        except Exception as e:
            print(f"❌ Error getting round data: {e}")
            return None

    def _get_structure_requirements(self, round_number):
        """Get structure requirements from BuildRecipes table"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT item_type, item_attributes, quantity
                    FROM BuildRecipes 
                    WHERE structure_id = ?
                """, (round_number,))
                results = cursor.fetchall()
                
                requirements = {}
                for row in results:
                    item_name = row['item_type']
                    if row['item_attributes']:
                        item_name += f" ({row['item_attributes']})"
                    requirements[item_name] = row['quantity']
                
                return requirements if requirements else f"Structure {round_number} blocks"
        except Exception as e:
            print(f"❌ Error getting structure requirements: {e}")
            return f"Structure {round_number} blocks"

    def _get_player_data(self):
        """Get current player information"""
        try:
            online_users = self.user_data_service.get_online_users()
            aipm_members = set(self.config["aipm"]["members"])
            
            # Filter for AIPM team members only
            aipm_online = [user for user in online_users if user['minecraft_username'] in aipm_members]
            
            active_players = [user['minecraft_username'] for user in aipm_online]
            
            player_positions = {}
            player_inventories = {}
            
            for user in aipm_online:
                username = user['minecraft_username']
                player_positions[username] = f"X:{user['current_x']:.1f}, Y:{user['current_y']:.1f}, Z:{user['current_z']:.1f}"
                
                # Get inventory
                inventory = self.user_data_service.get_user_inventory(username)
                if inventory:
                    inv_summary = {item['item_type']: item['quantity'] for item in inventory[:10]}  # Top 10 items
                    player_inventories[username] = inv_summary
                else:
                    player_inventories[username] = "Empty"
            
            return {
                'active_players': active_players,
                'player_positions': player_positions,
                'player_inventories': player_inventories
            }
        except Exception as e:
            print(f"❌ Error getting player data: {e}")
            return {
                'active_players': [],
                'player_positions': {},
                'player_inventories': {}
            }

    def _get_resource_area_data(self):
        """Get available resources from ResourceArea table"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT item_type, item_attributes FROM ResourceArea")
                results = cursor.fetchall()
                
                resources = []
                for row in results:
                    item_name = row['item_type']
                    if row['item_attributes']:
                        item_name += f" ({row['item_attributes']})"
                    resources.append(item_name)
                
                return resources if resources else ["Various building materials available"]
        except Exception as e:
            print(f"❌ Error getting resource area data: {e}")
            return ["Various building materials available"]

    def _get_processing_area_data(self):
        """Get available processing equipment from ProcessingArea table"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT item_type, item_attributes FROM ProcessingArea")
                results = cursor.fetchall()
                
                equipment = []
                for row in results:
                    item_name = row['item_type']
                    if row['item_attributes']:
                        item_name += f" ({row['item_attributes']})"
                    equipment.append(item_name)
                
                return equipment if equipment else ["Crafting tables, furnaces, and specialized equipment"]
        except Exception as e:
            print(f"❌ Error getting processing area data: {e}")
            return ["Crafting tables, furnaces, and specialized equipment"]

    def _get_map_locations(self):
        """Get map waypoint locations"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT waypoint_name, x, y, z FROM GameMap")
                results = cursor.fetchall()
                
                locations = {}
                for row in results:
                    locations[row['waypoint_name']] = [row['x'], row['y'], row['z']]
                
                return locations
        except Exception as e:
            print(f"❌ Error getting map locations: {e}")
            return {}
