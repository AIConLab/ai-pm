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
