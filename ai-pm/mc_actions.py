# AI imports
from agents import Agent, Runner

# MC imports
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
            return response

    except Exception as e:
        return None



class Actions:
    def __init__():
        pass

    def ai_welcome_greeting(self, username="DEFAULT_NAME"):
        agent = Agent(name="TownCrier", instructions="You are a medivial town crier meant to announce to the town when events have occured.")

        result = Runner.run_sync(agent, f"Make a celebratory announcment that {username} has joined the server")

        print(result.final_output)

    

