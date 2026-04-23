from plate_number_generator import generate_plate_number

class Car:
    def __init__(self, manual_plate=None):
        self.plate_number = manual_plate if manual_plate else generate_plate_number()
        self.arrivals = 0
        self.departures = 0

    def __repr__(self):
        return self.plate_number #returns plate number when object is printed instead of memory location like <Car object at 0x000001> :0
    

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, car):
        self.queue.append(car)
        car.arrivals += 1

    def dequeue(self):
        if self.is_empty():
            return None
        car = self.queue.pop(0)
        car.departures += 1
        return car

    def peek(self):
        return None if self.is_empty() else self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def remove_car(self, target_plate):
        if self.is_empty():
            print("Queue is empty.")
            return False

        temp_departures = []  # cars that will temporarily leave
        found = False
        size = self.size()

        # Phase 1: Depart cars until we find the target
        for _ in range(size):
            car = self.dequeue()
            if car is None:
                continue

            if car.plate_number == target_plate:
                print(f"{car.plate_number} permanently departs.")
                print(f"Arrivals: {car.arrivals}, Departures: {car.departures}")
                found = True
                break
            else:
                print(f"{car.plate_number} temporarily departs.")
                temp_departures.append(car)

        # Phase 2: Re-enter temporarily departed cars
        for car in temp_departures:
            self.enqueue(car)
            print(f"{car.plate_number} re-enters.")
            print(f"Arrivals: {car.arrivals}, Departures: {car.departures}")

        if not found:
            print(f"Car {target_plate} not found.")
        return found
