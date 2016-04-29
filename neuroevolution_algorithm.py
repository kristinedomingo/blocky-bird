import random
import math
from blocky_bird import game_function
from neural_network import individual

population = []
pop_size = 20
generations = 10

random.seed(0)

# Fill population[] with individuals
for x in range(pop_size):
    population.append(individual())

best = None
for generation in range(generations):
    print "===== GENERATION " + str(generation) + " ====="

    # Evaluate fitness of each individual - make each individual object play the game
    for individual in population:
        individual.evaluate()
    print "Scores for all individuals: " + str(list(i.fitness for i in population))

    # Find the best individual
    best = max(population, key = lambda x:x.fitness)
    print "Best: " + str(best.fitness)

    # Create new population, first adding the most fit individual from the old one
    new_population = [best]
    for x in range(1, pop_size):
        if random.random() < 0.5:
            # Mutate a random individual from the old population
            child = random.choice(population).mutate()
            new_population.append(child)
        else:
            # Breed and crossover two individuals from the old population
            p1 = random.choice(population)
            p2 = random.choice(population)
            child = p1.crossover(p2)
            new_population.append(child)
    population = new_population

    print ""


ann = best.create_neuron()
print "Score: " + str(game_function(ann, True))