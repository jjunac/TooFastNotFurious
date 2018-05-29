class Core:
    def __init__(self):
        self.entities = []

    def tick(self):
        for e in self.entities:
            e.tick()
