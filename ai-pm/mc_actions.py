# mc_actions
# AI imports
from agents import Agent, Runner

# MC imports
from mcrcon import MCRcon
import re


class RCONManager:
    """Manages RCON connections and credentials"""
    
    def __init__(self, host="minecraft", port=25575, password_file="/mc-data/.rcon-cli.env"):
        self.host = host
        self.port = port
        self.password_file = password_file
        self._password = None
    
    def _get_password(self):
        """Cache and return RCON password"""
        if self._password is None:
            try:
                with open(self.password_file, 'r') as f:
                    for line in f:
                        if 'password=' in line:
                            self._password = line.split('=')[1].strip()
                            break
                if not self._password:
                    raise ValueError("Password not found in file")
            except Exception as e:
                print(f"❌ Could not read RCON password: {e}")
                raise
        return self._password
    
    def execute_command(self, command):
        """Execute single RCON command"""
        try:
            password = self._get_password()
            with MCRcon(self.host, password, port=self.port) as mcr:
                response = mcr.command(command)
                print(f"✅ RCON: {command}")
                return response
        except Exception as e:
            print(f"❌ RCON failed: {command} - {e}")
            return None
    
    def execute_commands(self, commands):
        """Execute multiple RCON commands in single connection"""
        try:
            password = self._get_password()
            with MCRcon(self.host, password, port=self.port) as mcr:
                responses = []
                for command in commands:
                    response = mcr.command(command)
                    responses.append(response)
                    print(f"✅ RCON: {command}")
                return responses
        except Exception as e:
            print(f"❌ RCON batch failed: {e}")
            return None


class MessageService:
    """Handles message formatting and delivery"""
    
    def __init__(self, rcon_manager, max_length=200):
        self.rcon = rcon_manager
        self.max_length = max_length
    
    def _clean_message(self, message):
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
        return message.strip()
    
    def _chunk_message(self, message):
        """Split message into chunks if too long"""
        clean_msg = self._clean_message(message)
        
        if len(clean_msg) <= self.max_length:
            return [clean_msg]
        
        # Split into chunks
        words = clean_msg.split()
        chunks = []
        current_chunk = ""
        
        for word in words:
            if len(current_chunk + " " + word) <= self.max_length:
                current_chunk += (" " + word) if current_chunk else word
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = word
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def send_broadcast(self, message):
        """Send public message to all players"""
        chunks = self._chunk_message(message)
        commands = []
        
        for i, chunk in enumerate(chunks):
            if len(chunks) > 1:
                commands.append(f'say [{i+1}/{len(chunks)}] {chunk}')
            else:
                commands.append(f'say {chunk}')
        
        return self.rcon.execute_commands(commands)
    
    def send_private(self, username, message):
        """Send private message to specific player"""
        chunks = self._chunk_message(message)
        commands = []
        
        for i, chunk in enumerate(chunks):
            if len(chunks) > 1:
                commands.append(f'msg {username} [{i+1}/{len(chunks)}] {chunk}')
            else:
                commands.append(f'msg {username} {chunk}')
        
        return self.rcon.execute_commands(commands)


class Actions:
    """Business logic for AI actions"""
    
    def __init__(self):
        self.rcon_manager = RCONManager()
        self.message_service = MessageService(self.rcon_manager)

    def get_ai_welcome_greeting(self, username="player"):
        """Generate and broadcast AI welcome message"""
        try:
            print(f"🎮 Processing welcome for {username}")
            
            agent = Agent(
                name="TownCrier", 
                instructions="""You are a medieval town crier. Create SHORT, enthusiastic welcome messages for the arrival of your majesty, the greatest warrior above the pleebs, a god amongst men. Keep messages under 100 words, avoid special formatting, and use simple punctuation only."""
            )
            
            result = Runner.run_sync(agent, f"Make a brief celebratory announcement that {username} has joined the server")
            print(f"🤖 AI Result: {result.final_output}")
            
            # Broadcast the welcome
            if self.message_service.send_broadcast(result.final_output):
                print("✅ Welcome message broadcasted successfully!")
            else:
                print("❌ Failed to broadcast welcome message")
                
        except Exception as e:
            print(f"❌ Error in ai_welcome_greeting: {e}")

    def get_ai_pm_response(self, username="player", command=""):
        """Generate and send private AI response"""
        try:
            print(f"🤖 Processing @aipm command from {username}: '{command}'")
            
            if not command:
                self.message_service.send_private(username, f"How can I help? Send a msg via @aipm MSG")
                return
            
            agent = Agent(
                name="MinecraftHelper", 
                instructions="""You are a helpful Minecraft assistant. Provide concise, accurate answers about Minecraft gameplay, crafting, mechanics, and tips. Keep responses under 150 words and avoid special formatting. Be friendly and helpful."""
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
