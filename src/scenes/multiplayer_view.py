class MultiplayerView:
    def __init__(self, screen):
        self.screen = screen

    def run(self, connection):
        # TODO: use connection to sync game state between peers
        print("Running multiplayer view")
