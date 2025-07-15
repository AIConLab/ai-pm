#!/usr/bin/env python3
# File: mc_game_query.py
# Desc: Code to query game state and get information for players in the AIPM team to feed to AI agents

import os
import time
import nbtlib
from pathlib import Path
from typing import List 
import sys

from mc_database import Database
from rcon_client import RCONClient
from utils import load_config


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


def sync_server_data(db, rcon, aimp_team: List[str]):
    """Updated sync function with proper inventory replacement"""
    try:
        # Get current server players
        all_server_players = set(get_server_players(rcon))
        
        # Filter for players in AIPM team only
        aimp_team_set = set(aimp_team) 
        server_players = all_server_players & aimp_team_set
        
        # Delete players from database who are not currently in AIPM team
        deleted_count = db.delete_users_not_in_list(aimp_team)
        if deleted_count > 0:
            print(f"Removed {deleted_count} users not in AIPM team")
        
        # Get database online players (filtered to AIMP team)
        db_online = {user['minecraft_username'] for user in db.get_online_users() 
                    if user['minecraft_username'] in aimp_team_set}
        
        # Handle disconnected AIMP players (in DB but not on server)
        for username in db_online - server_players:
            db.set_online(username, False)
            print(f"Set {username} offline (not on server)")
        
        # Get information for online AIMP team members only
        for username in server_players:
            print(f"🔄 Processing player: {username}")
            db.add_user(username)
            db.set_online(username, True)
            
            # Update position
            position = get_player_position(rcon, username)
            if position:
                db.update_position(username, position[0], position[1], position[2])
                print(f"📍 Updated position for {username}: {position}")
            
            # Update inventory from NBT file - REPLACE entire inventory
            print(f"📦 Getting inventory for {username}...")
            inventory = get_player_inventory_from_nbt(username)
            
            if inventory:
                print(f"📊 Replacing database inventory with: {inventory}")
                # Use the new replace method instead of individual updates
                db.replace_user_inventory(username, inventory)
            else:
                print(f"❌ No inventory found for {username}, clearing database inventory")
                # Clear inventory if NBT shows no items
                db.clear_user_inventory(username)
        
        if server_players:
            print(f"✅ Synced {len(server_players)} AIPM team members")
        
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
        db = Database()
        db.init_tables()
        rcon = RCONClient()
        print("✅ Database and RCON initialized")
        
        if not rcon.password:
            print("❌ No RCON password found, exiting")
            return
        
        interval = 30  # seconds
        print(f"📊 Querying server every {interval} seconds...")

        while True:
            sync_server_data(db, rcon, config["aipm"]["members"])
            time.sleep(interval)

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