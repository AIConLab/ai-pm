#!/usr/bin/env python3
# File: mc_game_query.py
# Desc: Code to query game state and get information for players in the AIPM team to feed to AI agents

import os
import time
import nbtlib
from pathlib import Path
from typing import List 
import sys

from mc_database import Database, UserDataService, RoundDataService
from rcon_client import RCONClient
from utils import load_config

def get_round_information(rcon_client):
    """Get current round information from the game scoreboards"""
    try:
        # First check if a round is active
        active_response = rcon_client.execute("scoreboard players get #round_active bm_status")
        print(f"🔍 Round active response: {active_response}")
        
        if not active_response or "has no score" in active_response:
            print("❌ No round status found")
            return None
        
        # Parse if round is active (1) or not (0)
        try:
            parts = active_response.split("has")[1].split("[")[0].strip()
            round_active = int(parts) == 1
            print(f"🎮 Round active: {round_active}")
        except (ValueError, IndexError):
            print("❌ Could not parse round active status")
            return None
        
        # If no round is active, return early
        if not round_active:
            print("⏸️  No round currently active")
            return None
        
        # Round is active, get the current round number
        round_response = rcon_client.execute("scoreboard players get #current current_round")
        print(f"🔍 Current round response: {round_response}")
        
        if not round_response or "has no score" in round_response:
            print("❌ No current round found")
            return None
        
        # Parse current round number
        try:
            parts = round_response.split("has")[1].split("[")[0].strip()
            current_round = int(parts)
            print(f"🎯 Current round: {current_round}")
            return current_round
        except (ValueError, IndexError):
            print("❌ Could not parse current round number")
            return None
        
    except Exception as e:
        print(f"❌ Error getting round info: {e}")
        return None


def get_server_players(rcon_client):
    """Get list of players currently on server"""
    response = rcon_client.execute("list")
    if not response or "players online:" not in response:
        return []
    
    players_part = response.split("players online:")[-1].strip()
    if players_part:
        return [name.strip() for name in players_part.split(",")]
    return []


def get_player_position(rcon_client, username):
    """Get player's current position"""
    response = rcon_client.execute(f"data get entity {username} Pos")
    if not response or "No entity was found" in response:
        return None
    
    try:
        pos_str = response.split("[")[1].split("]")[0]
        coords = [float(coord.rstrip('d').strip()) for coord in pos_str.split(",")]
        return coords if len(coords) >= 3 else None
    except:
        return None


def get_player_inventory_from_nbt(username):
    """Get player inventory from NBT file with better debugging"""
    try:
        playerdata_dir = Path("/mc-data/world/playerdata")
        if not playerdata_dir.exists():
            print(f"❌ Playerdata directory not found: {playerdata_dir}")
            return {}
        
        print(f"🔍 Looking for player: {username}")
        player_file_found = None
        
        # Find the player's NBT file by checking lastKnownName
        for player_file in playerdata_dir.glob("*.dat"):
            try:
                nbt_data = nbtlib.load(player_file)
                
                # Debug: print the structure we're working with
                if 'bukkit' in nbt_data and 'lastKnownName' in nbt_data['bukkit']:
                    stored_name = str(nbt_data['bukkit']['lastKnownName'])
                    print(f"📁 Found player file {player_file.name} with name: {stored_name}")
                    
                    if stored_name == username:
                        player_file_found = player_file
                        print(f"✅ Matched player file for {username}")
                        
                        # Parse inventory with better filtering
                        inventory_dict = {}
                        inventory = nbt_data.get('Inventory', [])
                        
                        print(f"📦 Raw inventory has {len(inventory)} items")
                        
                        for item in inventory:
                            try:
                                item_id = str(item.get('id', 'unknown'))
                                count = int(item.get('count', 0))
                                slot = int(item.get('Slot', -1))
                                
                                # Debug: print each item
                                print(f"  Item: {item_id}, Count: {count}, Slot: {slot}")
                                
                                # Filter for main inventory slots (0-35) and hotbar (0-8)
                                # Skip enderchest items, crafting slots, etc.
                                if 0 <= slot <= 35:  # Main inventory + hotbar
                                    # Clean up item ID (remove minecraft: prefix if present)
                                    if item_id.startswith('minecraft:'):
                                        item_id = item_id[10:]
                                    
                                    # Add to inventory dict (combine if item already exists)
                                    if item_id in inventory_dict:
                                        inventory_dict[item_id] += count
                                    else:
                                        inventory_dict[item_id] = count
                                else:
                                    print(f"  ⏭️  Skipping slot {slot} (not main inventory)")
                                    
                            except Exception as e:
                                print(f"❌ Error parsing item: {e}")
                                continue
                        
                        print(f"📊 Final inventory for {username}: {inventory_dict}")
                        return inventory_dict
                        
            except Exception as e:
                print(f"❌ Error reading NBT file {player_file}: {e}")
                continue
        
        if not player_file_found:
            print(f"❌ No NBT file found for player: {username}")
            # List all available player files for debugging
            available_players = []
            for player_file in playerdata_dir.glob("*.dat"):
                try:
                    nbt_data = nbtlib.load(player_file)
                    if 'bukkit' in nbt_data and 'lastKnownName' in nbt_data['bukkit']:
                        available_players.append(str(nbt_data['bukkit']['lastKnownName']))
                except:
                    pass
            print(f"📋 Available players in NBT files: {available_players}")
        
        return {}
        
    except Exception as e:
        print(f"❌ Error reading NBT for {username}: {e}")
        import traceback
        traceback.print_exc()
        return {}


def sync_player_data_table(
    user_data_service:UserDataService,
    rcon:RCONClient,
    config):

    try:
        aipm_team = config["aipm"]["members"]

        # Get current server players
        all_server_players = set(get_server_players(rcon))
        
        # Filter for players in AIPM team only
        aipm_team_set = set(aipm_team) 
        server_players = all_server_players & aipm_team_set
        
        # Delete players from database who are not currently in AIPM team
        deleted_count = user_data_service.delete_users_not_in_list(aipm_team)
        if deleted_count > 0:
            print(f"Removed {deleted_count} users not in AIPM team")
        
        # Get database online players (filtered to aipm team)
        user_data_service_online = {user['minecraft_username'] for user in user_data_service.get_online_users() 
                    if user['minecraft_username'] in aipm_team_set}
        
        # Handle disconnected aipm players (in user_data_service but not on server)
        for username in user_data_service_online - server_players:
            user_data_service.set_online(username, False)
            print(f"Set {username} offline (not on server)")
        
        # Get information for online aipm team members only
        for username in server_players:
            print(f"🔄 Processing player: {username}")
            user_data_service.add_user(username)
            user_data_service.set_online(username, True)
            
            # Update position
            position = get_player_position(rcon, username)
            if position:
                user_data_service.update_position(username, position[0], position[1], position[2])
                print(f"📍 Updated position for {username}: {position}")
            
            # Update inventory from NBT file - REPLACE entire inventory
            print(f"📦 Getting inventory for {username}...")
            inventory = get_player_inventory_from_nbt(username)
            
            if inventory:
                print(f"📊 Replacing database inventory with: {inventory}")
                # Use the new replace method instead of individual updates
                user_data_service.replace_user_inventory(username, inventory)
            else:
                print(f"❌ No inventory found for {username}, clearing database inventory")
                # Clear inventory if NBT shows no items
                user_data_service.clear_user_inventory(username)
        
        if server_players:
            print(f"✅ Synced {len(server_players)} AIPM team members")

    except Exception as e:
        print(f"❌ Sync error: {e}")
        import traceback
        traceback.print_exc()
        

def sync_round_data_table(
    round_data_service:RoundDataService,
    rcon:RCONClient,
    config):
    try:
        round_num = get_round_information(rcon)
        if round_num:
            print(f"✅ Currently in round: {round_num}")
        else:
            print("ℹ️  No active round")

    
    except Exception as e:
        print(f"❌ Sync error: {e}")
        import traceback
        traceback.print_exc()


def sync_server_data(
    user_data_service:UserDataService,
    round_data_service:RoundDataService,
    rcon:RCONClient,
    config):

    """Updated sync function with proper inventory replacement"""
    try:
        sync_player_data_table(
            user_data_service=user_data_service,
            rcon=rcon,
            config=config
        )


        sync_round_data_table(
            round_data_service=round_data_service,
            rcon=rcon,
            config=config
        )

    except Exception as e:
        print(f"❌ Sync error: {e}")
        import traceback
        traceback.print_exc()



def main():
    
    try:
        print("🔄 Starting periodic query service")
        
        # Load config with better error handling
        print("📄 Loading configuration...")
        config = load_config()
        print("✅ Configuration loaded successfully")
        
        # Initialize database and RCON
        print("🔧 Initializing database and RCON...")
        db = Database(
            db_path="/app/database/aipm.db",
            user_config=config
            )
        db.init_tables()

        user_data_service = UserDataService(db=db)
        round_data_service = RoundDataService(db=db)

        rcon = RCONClient()
        print("✅ Database and RCON initialized")
        
        if not rcon.password:
            print("❌ No RCON password found, exiting")
            return
        
        query_interval = config["aipm"]["query_interval_sec"]
        print(f"📊 Querying server every {query_interval} seconds...")

        while True:

            sync_server_data(
                user_data_service=user_data_service,
                round_data_service=round_data_service,
                rcon=rcon,
                config=config
            )

            time.sleep(query_interval)

    except KeyboardInterrupt:
        print("\n🛑 Stopping query service...")
        
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        return 1
        
    except ValueError as e:
        # This will catch our TOML parsing errors with detailed info
        print(f"❌ Configuration Error: {e}")
        return 1
        
    except RuntimeError as e:
        # This will catch other config loading errors
        print(f"❌ Runtime Error: {e}")
        return 1
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        print("✅ Query service stopped")


if __name__ == "__main__":

    exit_code = main()

    if exit_code:
        sys.exit(exit_code)