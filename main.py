from infrastucture import *
from chromosome import *
from individual import *
import random

def breed_new_generation(individuals, winners = None, mutation_rate = 0.000005, target_population_size = None):
    if not target_population_size:
        target_population_size = len(winners) * len(winners - 1)
    if winners:
        winner_positions = {x:i for (i, x) in enumerate(winners)}
        winning_individuals = [x for x in individuals if x.name in winners]
        winning_individuals.sort(key = lambda x: winner_positions[x.name])
    else:
        winning_individuals = individuals[:10]
        random.shuffle(winning_individuals)
    new_population = Individual.breed_population(winning_individuals, target_population_size)
    for i, x in enumerate(new_population):
        x.mutate(mutation_rate)
    return new_population


individuals = unserialize_individuals('initial.json', chromosome_classes)
new_population = breed_new_generation(individuals, target_population_size = 100)
serialize_individuals(new_population, 'gen002.json')

destination = 'Z:\\programming\\sd_projects\\breed_diffusion\\first_experiment\\gen002\\'
for i, individual in enumerate(new_population):
    expression = individual.express()
    submit_job(expression, destination, individual.name)