import random

def get_random_name(filename):
    with open(filename, 'r') as file:
        names = file.readlines()
        names = [name.strip() for name in names]  # Remove any extra whitespace

    return random.choice(names)

first_name = get_random_name('firstnames.csv')
last_name = get_random_name('lastnames.csv')

print(f"{first_name} {last_name}")

