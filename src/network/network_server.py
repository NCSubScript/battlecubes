class NetworkServer:
    def __init__(self, port):
        self.port = port

    def start(self):
        # TODO: listen for clients, accept connections
        print(f"Starting server on port {self.port}")
