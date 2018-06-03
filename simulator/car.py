from copy import deepcopy


class Car:

    def __init__(self, path, departure):
        self.path = deepcopy(path)
        self.departure = departure

    def get_way_index(self):
        return self.path.next_direction()

    def go_forward(self):
        self.path.pop_direction()