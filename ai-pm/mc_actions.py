# mc_actions
# AI imports
from agents import Agent, Runner

# MC imports
from mcrcon import MCRcon
import re

def clean_message_for_minecraft(message):
    """Clean message for Minecraft compatibility"""
    # Remove markdown formatting
    message = re.sub(r'\*\*(.*?)\*\*', r'\1', message)  # Remove **bold**
    message = re.sub(r'\*(.*?)\*', r'\1', message)      # Remove *italic*
    message = re.sub(r'`(.*?)`', r'\1', message)        # Remove `code`
    
    # Replace newlines with spaces
    message = message.replace('\n', ' ')
    
    # Remove multiple spaces
    message = re.sub(r'\s+', ' ', message)
    
    # Remove special characters that might break commands
    message = re.sub(r'[^\w\s\!\?\.\,\-\:]', '', message)
    
    # Trim whitespace
    message = message.strip()
    
    return message

def broadcast(message):
    """Send message to all players"""
    try:
        # Clean the message first
        clean_msg = clean_message_for_minecraft(message)
        
        # Split long messages (Minecraft has ~256 char limit for chat)
        max_length = 200
        if len(clean_msg) > max_length:
            # Split into chunks
            words = clean_msg.split()
            chunks = []
            current_chunk = ""
            
            for word in words:
                if len(current_chunk + " " + word) <= max_length:
                    current_chunk += (" " + word) if current_chunk else word
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = word
            
            if current_chunk:
                chunks.append(current_chunk)
        else:
            chunks = [clean_msg]
        
        # Read RCON password from the file
        with open('/mc-data/.rcon-cli.env', 'r') as f:
            password = None
            for line in f:
                if 'password=' in line:
                    password = line.split('=')[1].strip()
                    break
        
        if not password:
            print("❌ Could not find RCON password")
            return None
        
        # Connect to minecraft container and send messages
        with MCRcon("minecraft", password, port=25575) as mcr:
            responses = []
            for i, chunk in enumerate(chunks):
                if len(chunks) > 1:
                    # Add part indicator for multi-part messages
                    response = mcr.command(f'say [{i+1}/{len(chunks)}] {chunk}')
                else:
                    response = mcr.command(f'say {chunk}')
                responses.append(response)
                print(f"✅ Broadcasted chunk {i+1}: {chunk[:50]}...")
            
            return responses
            
    except Exception as e:
        print(f"❌ Broadcast failed: {e}")
        return None

class Actions:
    def __init__(self):
        pass

    def ai_welcome_greeting(self, username="DEFAULT_NAME"):
        try:
            print(f"🎮 Processing welcome for {username}")
            
            # Generate AI message
            agent = Agent(
                name="TownCrier", 
                instructions="""You are a medieval town crier. Create SHORT, enthusiastic welcome messages 
                for new players joining a Minecraft server. Keep messages under 100 words, avoid special 
                formatting, and use simple punctuation only."""
            )
            
            result = Runner.run_sync(agent, f"Make a brief celebratory announcement that {username} has joined the server")
            
            print(f"🤖 AI Result: {result.final_output}")
            
            # Broadcast the AI message
            broadcast_result = broadcast(result.final_output)
            
            if broadcast_result:
                print("✅ Welcome message broadcasted successfully!")
            else:
                print("❌ Failed to broadcast welcome message")
                
        except Exception as e:
            print(f"❌ Error in ai_welcome_greeting: {e}")
            return None