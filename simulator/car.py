class Car:

    def __init__(self, path):
        self.path = path

    def get_way_index(self):
        return self.path.next_direction()

    def go_forward(self):
        self.path.pop_direction()