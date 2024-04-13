from chromosome import *
import uuid
import random
import math

def softmax_weights(for_length, temperature = 1.0):
    scores = [score / temperature for score in range(for_length - 1, -1, -1)]
    max_score = max(scores)
    exp_scores = [math.exp(score - max_score) for score in scores]
    sum_exp_scores = sum(exp_scores)
    return [exp_score / sum_exp_scores for exp_score in exp_scores]

class Individual:
    def __init__(self):
        self.name = str(uuid.uuid4())  # Assign a unique name to each individual
        self.chromosomes = []  # List to store chromosome objects
        self.parentage = []  # List to store tuples representing parents, initially empty

    def add_chromosome(self, chromosome):
        if isinstance(chromosome, Chromosome):
            self.chromosomes.append(chromosome)
        else:
            raise TypeError("Expected a Chromosome instance")

    def mutate(self, probability):
        for i, chromosome in enumerate(self.chromosomes):
            result = chromosome.mutate(probability)
            if result != False:
                print(f'!! individual {self.name} underwent mutation on chromosome {i}!')
                print(f'   {result}')


    def express(self, perturbation=0.0):
        expressed_genes = [chromosome.express(perturbation) for chromosome in self.chromosomes]
        return ', '.join(', '.join(gene for gene in genes) for genes in expressed_genes)

    def set_parents(self, parent1, parent2):
        self.parentage.append((parent1, parent2))

    @classmethod
    def create_child(cls, *parents):
        if not parents:
            raise ValueError("At least one parent is required")

        chromosome_count = len(parents[0].chromosomes)
        if not all(len(parent.chromosomes) == chromosome_count for parent in parents):
            raise ValueError("All parents must have the same number of chromosomes")

        child = cls()
        for i in range(chromosome_count):
            chromosome_class = type(parents[0].chromosomes[i])
            chosen_genes = [random.choice(parent.chromosomes[i].genes) for parent in parents]
            child_chromosome = chromosome_class(*chosen_genes)
            child.add_chromosome(child_chromosome)

        child.parentage = [(parent.name, parent.parentage) for parent in parents]
        return child
    
    @classmethod
    def breed_population(cls, individuals, target_population_size):
        new_population = []
        # I found this was producing too much of a winner-takes-all situation, but
        # I am committed for this run. you may want to consider using the provided 
        # softmax function instead, something like softmax(len(individuals), temperature = 6.0)
        weights=[1/(i+1) for i in range(len(individuals))]
        while len(new_population) < target_population_size:
            parents = random.choices(individuals, k=2, weights=weights)
            if parents[0] != parents[1]:
                child = cls.create_child(*parents)
                new_population.append(child)
        return new_population
    