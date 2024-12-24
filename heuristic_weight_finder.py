# Genetic algorithm will be implemented here to find the best weightings for our system

# Processing of the Genetic Algorith:

# 1. Start with a population of a certain amount of chromosomes (set of weights for each of the heuristics)
# 2. Run the tetris for different seeds with the defined chromosome (10 different ones)
# 3. Filter the fittest chromosomes and reproduce them to create newer chromosomes
#    - Multiple strategies:
#       - Getting a random point to cut the list at (CURRENT APPROACH)
# 4. Mutate the children to add some randomly generated values
#    - Adding a +/- randomised value to some of the weights based on a probability of mutation
# 5. Iterate through the steps with the new set of chromosomes until the weightings give a sufficiently good score

# Important Information: Seed is in the constants.py

# Important Adjustment: Run the games just on the board with no graphics to reduce the amount of resources allocated and to be able to conduct as many tests as possible


import random
from visual import run_weights_test_for_genetic_algorithm
    
    
def find_best_weight_heuristics():
    best_performing_weight = []
    score_of_best_performing_weight = -(10**10)
    set_of_weights = generate_set_of_random_weights()
    for _ in range(50):
        scores_of_weights = [weight_fitness(weights) for weights in set_of_weights]
        parents, score_of_best_weight_in_generation, best_weight_in_generation = select_best_weights(scores_of_weights, set_of_weights)
        if score_of_best_performing_weight < score_of_best_weight_in_generation:
            score_of_best_performing_weight = score_of_best_weight_in_generation
            best_performing_weight = best_weight_in_generation
        set_of_weights = parents[:]
        while len(set_of_weights) < 20:
            new_offspring_weight = reproduce_two_weights(*random.sample(parents,2))
            weight_mutation(new_offspring_weight, 0.1)
            set_of_weights.append(new_offspring_weight)
    return best_performing_weight


def generate_set_of_random_weights():
    return [[random.uniform(0, 10) for _ in range(7)] for _ in range(20)]


def weight_fitness(weights):
    fitness = run_game_with_given_weights(weights)
    print(weights, "with score", fitness)
    return fitness


def run_game_with_given_weights(weight):
    return run_weights_test_for_genetic_algorithm(weight)
    
    
def select_best_weights(scores_of_weights, set_of_weights):
    chromosomes = dict(zip(scores_of_weights, set_of_weights))
    chromosomes = dict(sorted(chromosomes.items()))
    return list(chromosomes.values())[:len(scores_of_weights()//2)], *(list(chromosomes.items())[-1])


def reproduce_two_weights(first_weight, second_weight):
    separation_point = random.uniform(1, len(first_weight) - 1)
    return first_weight[:separation_point] + second_weight[:separation_point]


def weight_mutation(weights, mutation_probability):
    for current_weight in range(4):
        if random.rand() < mutation_probability:
            weights[current_weight] += random.uniform(-2,2)
        if weights[current_weight] < 0:
            weights[current_weight] = 0
        elif weights[current_weight] > 10:
            weights[current_weight] = 10
            
            
print(find_best_weight_heuristics())