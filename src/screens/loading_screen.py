class LoadingScreen:
    def __init__(self, screen):
        self.screen = screen

    def run(self, progress_callback=None):
        # TODO: display loading bar, call progress_callback(percent)
        print("Loading assets/resources")
