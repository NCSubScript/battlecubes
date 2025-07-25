class NetworkClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        # TODO: open socket, handshake
        print(f"Connecting to {self.host}:{self.port}")
