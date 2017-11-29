from random import randint

def generate_data(data):
        data["rpm"] = randint(0, 7000)
        data["speed"] = randint(0, 200)
