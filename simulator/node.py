class Node():
    def __init__(self):
        self.successors = []
        self.predecessors = []
        self.current_car = None
        self.next_car = None

    def compute_next(self, simulator):
        if self.current_car is None:
            return
        if len(self.successors) == 0:
            self.next_car = None
            return
        destination = self.successors[self.current_car.get_way_index()]
        if self.__can_move_to(destination, simulator):
            destination.next_car = self.current_car
            self.next_car = None
            self.current_car.go_forward()
        else:
            self.next_car = self.current_car

    def __can_move_to(self, destination, simulator):
        dependencies = simulator.dependencies[(self, destination)]
        for d in dependencies:
            if self.current_car:
                return False
        return True

    def apply_next(self):
        self.current_car = self.next_car
        self.next_car = None

    def __str__(self):
        return "#" if self.current_car else " "
