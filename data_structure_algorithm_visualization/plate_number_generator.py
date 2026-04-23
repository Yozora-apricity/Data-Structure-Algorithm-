import random
import string

def generate_plate_number():
    letters = "".join(random.choices(string.ascii_uppercase, k=3))
    numbers = "".join(random.choices(string.digits, k=3))
    return f"{numbers}-{letters}"