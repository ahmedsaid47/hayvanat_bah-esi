import random

class Animal:
    def __init__(self, species, gender, x=None, y=None):
        self.species = species
        self.gender = gender
        self.x = x if x is not None else random.randint(0, FIELD_SIZE)
        self.y = y if y is not None else random.randint(0, FIELD_SIZE)
        self.alive = True

    def move(self):
        dx = random.randint(-movement_ranges[self.species], movement_ranges[self.species])
        dy = random.randint(-movement_ranges[self.species], movement_ranges[self.species])
        self.x = max(0, min(FIELD_SIZE, self.x + dx))
        self.y = max(0, min(FIELD_SIZE, self.y + dy))

    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

class Ecosystem:
    def __init__(self):
        self.animals = []
        self.initialize_animals()

    def initialize_animals(self):
        # Initialize specific number of each animal
        for species, genders in initial_counts.items():
            for gender, count in genders.items():
                for _ in range(count):
                    self.animals.append(Animal(species, gender))

    def simulate_movement(self):
        for animal in self.animals:
            if animal.alive:
                animal.move()

    def handle_interactions(self):
        for predator in self.animals:
            if not predator.alive:
                continue
            # Handle hunting
            if predator.species in hunting_ranges:
                for prey_species, max_distance in hunting_ranges[predator.species].items():
                    for prey in self.animals:
                        if prey.species == prey_species and prey.alive and predator.distance_to(prey) <= max_distance:
                            prey.alive = False
            # Handle reproduction
            if predator.species in ['sheep', 'cow', 'wolf', 'lion']:
                for mate in self.animals:
                    if mate.species == predator.species and mate.gender != predator.gender and mate.alive and predator.distance_to(mate) <= BIRTH_DISTANCE:
                        self.animals.append(Animal(predator.species, random.choice(['male', 'female'])))

    def remove_dead(self):
        self.animals = [animal for animal in self.animals if animal.alive]

    def simulate(self):
        for _ in range(NUM_STEPS):
            self.simulate_movement()
            self.handle_interactions()
            self.remove_dead()

    def count_animals(self):
        counts = {}
        for animal in self.animals:
            key = f"{animal.species} {animal.gender}"
            if key in counts:
                counts[key] += 1
            else:
                counts[key] = 1
        return counts

# Constants
FIELD_SIZE = 500
NUM_STEPS = 1000
BIRTH_DISTANCE = 3

# Movement and hunting ranges
movement_ranges = {"sheep": 2, "wolf": 3, "cow": 2, "chicken": 1, "rooster": 1, "lion": 4, "hunter": 1}
hunting_ranges = {
    "wolf": {"sheep": 4, "chicken": 4, "rooster": 4},
    "lion": {"cow": 5, "sheep": 5},
    "hunter": {"sheep": 8, "wolf": 8, "cow": 8, "chicken": 8, "rooster": 8, "lion": 8}
}

# Initial animal counts
initial_counts = {
    "sheep": {"male": 15, "female": 15},
    "wolf": {"male": 5, "female": 5},
    "cow": {"male": 5, "female": 5},
    "chicken": {"none": 10},
    "rooster": {"none": 10},
    "lion": {"male": 4, "female": 4},
    "hunter": {"none": 1}
}

# Reinitialize and simulate
ecosystem = Ecosystem()
ecosystem.simulate()
final_counts = ecosystem.count_animals()

print(final_counts)
