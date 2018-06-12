class Statistics:

    def __init__(self):
        self.list_cars_arrived = {}

    def add_car_travel(self, departure, path, travel):
        if not (departure, path) in self.list_cars_arrived:
            self.list_cars_arrived[(departure, path)] = []
        self.list_cars_arrived[(departure, path)].append(travel)
