from plate_number_generator import generate_plate_number

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        if self.isEmpty():
            return None
        return self.stack.pop()

    def peek(self):
        if self.isEmpty():
            return None
        return self.stack[-1]

    def isEmpty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

class Car():
    def __init__(self, manual_plate = None):
        self.plate_number = manual_plate if manual_plate else generate_plate_number()
        self.arrivals = 0
        self.departures = 0

    def remove_car(self, stack, target):
        if stack.isEmpty():
            return False

        # Physical departure
        top_car = stack.pop()
        top_car.departures += 1

        # If this is the target, removal is complete
        if top_car.plate_number == target:
            return True

        # Recurse down the stack
        found = self.remove_car(stack, target)

        # Physical re-arrival (always, because the car comes back)
        stack.push(top_car)
        top_car.arrivals += 1

        return found
