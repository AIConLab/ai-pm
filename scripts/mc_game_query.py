#!/usr/bin/env python3
# mc_game_query.py - Periodic RCON query service
import time
import nbtlib
from pathlib import Path
import tomllib

from mc_database import Database
from rcon_client import RCONClient

def load_config(config_path="config.toml"):
    """Load all params from config file"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found")
    
    with open(config_path, 'rb') as f:
        return tomllib.load(f)

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
    """Get player inventory from NBT file"""
    try:
        playerdata_dir = Path("/mc-data/world/playerdata")
        if not playerdata_dir.exists():
            return {}
        
        # Find the player's NBT file by checking lastKnownName
        for player_file in playerdata_dir.glob("*.dat"):
            try:
                nbt_data = nbtlib.load(player_file)
                if 'bukkit' in nbt_data and 'lastKnownName' in nbt_data['bukkit']:
                    if str(nbt_data['bukkit']['lastKnownName']) == username:
                        # Parse inventory
                        inventory_dict = {}
                        inventory = nbt_data.get('Inventory', [])
                        
                        for item in inventory:
                            item_id = str(item.get('id', 'unknown'))
                            count = int(item.get('count', 0))
                            
                            # Clean up item ID (remove minecraft: prefix if present)
                            if item_id.startswith('minecraft:'):
                                item_id = item_id[10:]
                            
                            # Add to inventory dict (combine if item already exists)
                            if item_id in inventory_dict:
                                inventory_dict[item_id] += count
                            else:
                                inventory_dict[item_id] = count
                        
                        return inventory_dict
            except Exception as e:
                # Skip files that can't be read
                continue
        
        return {}
    except Exception as e:
        print(f"Error reading NBT for {username}: {e}")
        return {}

def sync_server_data(db, rcon):
    """Sync all online players with database"""
    try:
        # Get current server players
        server_players = set(get_server_players(rcon))
        
        # Get database online players
        db_online = {user['minecraft_username'] for user in db.get_online_users()}
        
        # Handle disconnected players (in DB but not on server)
        for username in db_online - server_players:
            db.set_online(username, False)
            print(f"Set {username} offline (not on server)")
        
        # Handle online players
        for username in server_players:
            db.add_user(username)
            db.set_online(username, True)
            
            # Update position
            position = get_player_position(rcon, username)
            if position:
                db.update_position(username, position[0], position[1], position[2])
            
            # Update inventory from NBT file
            inventory = get_player_inventory_from_nbt(username)
            for item_type, quantity in inventory.items():
                db.update_inventory(username, item_type, quantity)
        
        if server_players:
            print(f"Synced {len(server_players)} online players")
        
    except Exception as e:
        print(f"Sync error: {e}")

def main():
    
    try:
        print("🔄 Starting periodic query service")
        
        db = Database()
        rcon = RCONClient()
        config = load_config()
        
        if not rcon.password:
            print("❌ No RCON password found, exiting")
            return
        
        interval = 30  # seconds
        print(f"📊 Querying server every {interval} seconds...")

        while True:
            sync_server_data(db, rcon)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Stopping query service...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("✅ Query service stopped")

if __name__ == "__main__":
    main()