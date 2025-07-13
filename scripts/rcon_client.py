from mcrcon import MCRcon

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


class MessageService:
    """Handles message formatting and delivery"""
    
    def __init__(self, rcon_client, max_length=200):
        self.rcon = RCONClient()
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
        
        try:
            for command in commands:
                self.rcon.execute(command)
            
            return True

        except Exception as e:
            return False
    
    def send_private(self, username, message):
        """Send private message to specific player"""
        chunks = self._chunk_message(message)
        commands = []
        
        for i, chunk in enumerate(chunks):
            if len(chunks) > 1:
                commands.append(f'msg {username} [{i+1}/{len(chunks)}] {chunk}')
            else:
                commands.append(f'msg {username} {chunk}')
        
        try:
            for command in commands:
                self.rcon.execute(command)
            
            return True

        except Exception as e:
            return False


