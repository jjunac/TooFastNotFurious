class Statistics:

    def __init__(self):
        self.list_cars_arrived = {}

    def add_car_travel(self, car):
        if not (car.departure, car.original_path) in self.list_cars_arrived:
            self.list_cars_arrived[(car.departure, car.original_path)] = []
        self.list_cars_arrived[(car.departure, car.original_path)].append(car)
