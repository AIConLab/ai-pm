#!/usr/bin/env python3
# mc_game_query.py - Periodic RCON query service
import time
from mcrcon import MCRcon
from mc_database import Database

class RCONClient:
    def __init__(self, host="minecraft", port=25575, password_file="/mc-data/.rcon-cli.env"):
        self.host = host
        self.port = port
        self.password = self._get_password(password_file)
    
    def _get_password(self, password_file):
        try:
            with open(password_file, 'r') as f:
                for line in f:
                    if 'password=' in line:
                        return line.split('=')[1].strip()
        except:
            pass
        return None
    
    def execute(self, command):
        if not self.password:
            return None
        try:
            with MCRcon(self.host, self.password, port=self.port) as mcr:
                return mcr.command(command)
        except:
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
        
        if server_players:
            print(f"Synced {len(server_players)} online players")
        
    except Exception as e:
        print(f"Sync error: {e}")

def main():
    print("🔄 Starting periodic query service")
    
    db = Database()
    rcon = RCONClient()
    
    if not rcon.password:
        print("❌ No RCON password found, exiting")
        return
    
    interval = 30  # seconds
    print(f"📊 Querying server every {interval} seconds...")
    
    try:
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