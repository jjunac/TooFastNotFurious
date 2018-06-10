class Node:
    def __init__(self, entity):
        self.entity = entity
        self.successors = []
        self.predecessors = []
        self.current_car = None
        self.next_car = None

    def compute_next(self, simulator):
        if not self.current_car:
            return
        if len(self.successors) == 0:
            self.next_car = None
            return
        destination = self.current_car.get_next_node()
        if self.__can_move_to(destination, simulator):
            destination.next_car = self.current_car
            self.next_car = None
            self.current_car.go_forward()
        else:
            self.next_car = self.current_car

    def __can_move_to(self, destination, simulator):
        if destination.next_car:
            return False
        dependencies = simulator.dependencies[(self, destination)]
        for d in dependencies:
            if not d.is_dependency_satisfied(self):
                return False
        return True

    def is_dependency_satisfied(self, source):
        if not self.entity.is_dependency_satisfied(source):
            return False
        if self.current_car:
            return False
        return True

    def apply_next(self):
        self.current_car = self.next_car
        self.next_car = None
        if self.current_car:
            self.current_car.tick(self)
