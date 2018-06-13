class Node:
    def __init__(self, entity, can_ignore_dependency=False):
        self.entity = entity
        self.successors = []
        self.predecessors = []
        self.current_car = None
        self.next_car = None
        self.can_ignore_dependency = can_ignore_dependency

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
        if destination.current_car or destination.next_car:
            return False
        dependencies = simulator.dependencies[(self, destination)]
        all_dependency_satisfied = True
        for d in dependencies:
            if not d.is_dependency_satisfied(self):
                all_dependency_satisfied = False
                break
        if all_dependency_satisfied:
            return True
        if self.can_ignore_dependency:
            for d in dependencies:
                if d.current_car and self.current_car.id < d.current_car.id:
                    return False
        return self.can_ignore_dependency

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
