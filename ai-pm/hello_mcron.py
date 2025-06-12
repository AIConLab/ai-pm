from mcrcon import MCRcon

def broadcast(message):
    """Send message to all players"""
    try:
        # Read RCON password from the file
        with open('/mc-data/.rcon-cli.env', 'r') as f:
            for line in f:
                if 'password=' in line:
                    password = line.split('=')[1].strip()
                    break
        
        # Connect to minecraft container (not localhost!)
        with MCRcon("minecraft", password, port=25575) as mcr:
            response = mcr.command(f"say {message}")
            print(f"✅ Broadcasted: {message}")
            return response
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None

def assign_team(player, team):
    """Add player to team"""
    try:
        with open('/mc-data/.rcon-cli.env', 'r') as f:
            for line in f:
                if 'password=' in line:
                    password = line.split('=')[1].strip()
                    break
        
        with MCRcon("minecraft", password, port=25575) as mcr:
            # Create team if doesn't exist
            mcr.command(f"team add {team}")
            # Add player to team
            response = mcr.command(f"team join {team} {player}")
            print(f"✅ Assigned {player} to {team}")
            return response
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None

# Examples
broadcast("Hello from Python container!")
assign_team("jc_cr", "RedTeam")