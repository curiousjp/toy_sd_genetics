from infrastucture import *
from chromosome import *
from individual import *
import random

def breed_new_generation(individuals, winners = None, mutation_rate = 0.0000075, target_population_size = None):
    if winners:
        winner_positions = {x:i for (i, x) in enumerate(winners)}
        winning_individuals = [x for x in individuals if x.name in winners]
        winning_individuals.sort(key = lambda x: winner_positions[x.name])
    else:
        winning_individuals = individuals[:10]
        random.shuffle(winning_individuals)
    if not target_population_size:
        target_population_size = len(winners) * len(winners - 1)
    new_population = Individual.breed_population(winning_individuals, target_population_size)
    for i, x in enumerate(new_population):
        x.mutate(mutation_rate)
    return new_population

# note for generating contact sheet:
# montage -verbose -label '%f' -font Helvetica -pointsize 8 -background '#000000' -fill 'gray' -define jpeg:size=200x200 -geometry 200x200+2+2 -auto-orient *.png ../contact.jpg
# you may need to adjust your im6 cache policy: https://blog.eq8.eu/til/imagemagic-cache-resources-exhausted.html

# individuals = unserialize_individuals('gen001.json', chromosome_classes)
# new_population = breed_new_generation(individuals, target_population_size = 100)
# serialize_individuals(new_population, 'gen002.json')

# PS C:\Users\curious\Documents\GitHub\breed_diffusion> python .\main.py
# !! individual 2cbbb8cc-0d06-4ee7-9967-87020299aa5b underwent mutation on chromosome 15!
# !! individual 479dedd3-3384-4a38-8f39-986d3fb31a38 underwent mutation on chromosome 6!
# !! individual 7ca148b7-710b-4383-8c7a-e58736db6d4c underwent mutation on chromosome 4!
# !! individual 1b733fff-4a03-4614-aa05-82cdf4353633 underwent mutation on chromosome 6!
# !! individual 4d40ae75-65f6-4722-ab7a-e384703788ac underwent mutation on chromosome 9!

gen002_winners = [
    '1a219c70-dc63-4541-8245-fd6947092545',
    '3bc040f4-b1f2-4a4d-b488-809ee198146b',
    '504b4763-0389-46c2-9594-c5131458f628',
    '644931eb-2867-4d8e-89b5-7c2ea2d3ad76',
    '53358778-94f7-4509-950b-d8a93b4b7b76',
    'a9b32fd4-bb20-48c8-87ac-bea4c79dfabd',
    'afdfe092-51ea-4951-a25c-453350b6de2c',
    'c5b601de-4765-4e89-bfb3-9fdf384f2fbc',
    'cbc05d8c-d7d2-41f8-a62c-559b33284e5e',
    '3a6f89a8-dfc9-4aa6-b0b9-f92dced60d11',
]

# gen002 = unserialize_individuals('gen002.json', chromosome_classes)
# new_population = breed_new_generation(gen002, winners = gen002_winners, target_population_size = 100)
# serialize_individuals(new_population, 'gen003.json')

# PS C:\Users\curious\Documents\GitHub\breed_diffusion> python .\main.py
# !! individual 929117a8-b870-4742-be5d-691ebf2aaed3 underwent mutation on chromosome 5!
# !! individual 3c6132df-972b-4f3f-9b0f-62a8dafd1957 underwent mutation on chromosome 5!
# !! individual 58f07a3e-30c4-47fd-8e67-acb507b336b2 underwent mutation on chromosome 12!
# !! individual 89806f64-5f77-4a62-8fe2-e491a0bd4c90 underwent mutation on chromosome 6!
# !! individual 85e233a2-b796-41c2-9d1d-8fd68f996f87 underwent mutation on chromosome 6!
# !! individual 62069ec8-b538-4e9b-b4a7-eb1ca116e792 underwent mutation on chromosome 3!
# !! individual 1ba1fb45-028c-463b-b84c-4714e45547d2 underwent mutation on chromosome 14!
# !! individual 1178e10f-8324-4178-8877-8a51d1a3d469 underwent mutation on chromosome 6!
# !! individual 4f7b0c46-7e3e-4d3c-b62c-c9edd10c3426 underwent mutation on chromosome 5!
# !! individual 46a22436-5489-483a-b8db-4c4a34a0ab0c underwent mutation on chromosome 12!
# !! individual f5087d74-088f-4c84-ae2e-358f1ec45902 underwent mutation on chromosome 12!
# !! individual 0761e736-8e0e-4adc-b5d0-bf83e8c9169a underwent mutation on chromosome 5!
# !! individual d394caee-fb3c-4133-aa96-cb4f53a6ea5f underwent mutation on chromosome 3!

gen003_winners = [
    '9165346c-b953-45a9-be4f-d297640fd95b',
    'a2901486-8d27-418c-96f3-2570f0aacee4',
    '89a17593-5693-46a9-b059-cabf0794fe8d',
    'cbaa3ae8-a55a-43aa-aa2d-526a841c0178',
    '4c6fb70d-a0f1-4556-aa73-b1c09111ffbd',
    '068c507a-12d5-4ec0-a6ce-b9e157c8149f',
    '5f4c71e4-9df1-4d38-bbcc-86ead35f8004',
    '5a703b13-7985-4b99-a4c7-21b343ee4aa9',
    '07ff9dac-27f3-41fa-b25c-1dd5682f112a',
    '162bcc35-54c5-4ec5-b9df-12b78d075691',
]

gen003 = unserialize_individuals('gen003.json', chromosome_classes)
new_population = breed_new_generation(gen003, winners = gen003_winners, target_population_size = 100)
serialize_individuals(new_population, 'gen004.json')

# PS C:\Users\curious\Documents\GitHub\breed_diffusion> python .\main.py
# !! individual 0a5ab083-039f-47c3-b232-140d8dd56233 underwent mutation on chromosome 4!
#    [('FeatureChromoCD', 0, 'circle_cut', 'on')]
# !! individual dc671c48-9dfd-4363-9a7f-c051110fd02a underwent mutation on chromosome 10!
#    [('FeatureChromoOP', 1, 'plaid_skirt', 'on')]
# !! individual 0ad246f6-1d4c-4f0c-846d-4633c237675c underwent mutation on chromosome 5!
#    [('FeatureChromoEF', 0, 'ferret', 'on')]
# PS C:\Users\curious\Documents\GitHub\breed_diffusion> python .\main.py
# !! individual 0f8019b2-68cd-4dae-868d-23701519243d underwent mutation on chromosome 10!
#    [('FeatureChromoOP', 1, 'playing_games', 'on')]
# !! individual 20ef2210-af52-48e9-93d6-c9f8767899c3 underwent mutation on chromosome 12!
#    [('FeatureChromoST', 1, 'swimsuit', 'on')]
# !! individual b2af5967-1f77-445f-b7bd-4c57e1e74cfa underwent mutation on chromosome 9!
#    [('FeatureChromoMN', 0, 'monster', 'on')]
# !! individual 48f22c59-38f1-4a9a-8b08-60f8c38b786e underwent mutation on chromosome 10!
#    [('FeatureChromoOP', 0, 'pinching', 'on')]
# !! individual 0ed33587-440d-4ad3-b997-4cf4d85d2e28 underwent mutation on chromosome 12!
#    [('FeatureChromoST', 0, 'shy', 'on')]
# !! individual 9238feb7-24c2-443d-8de1-438c7b554e7b underwent mutation on chromosome 6!
#    [('FeatureChromoGH', 1, 'halloween', 'on')]
# !! individual 07681e33-f2a6-4c95-a26f-1301b7077819 underwent mutation on chromosome 7!
#    [('FeatureChromoIJ', 0, 'injury', 'on')]
# !! individual c13f6832-fd84-4f82-8c12-4eb5335be7cc underwent mutation on chromosome 11!
#    [('FeatureChromoQR', 0, 'rising_sun_flag', 'on')]
# !! individual 2cc8aa98-dbe6-405f-8eb9-45d776f3a407 underwent mutation on chromosome 8!
#    [('FeatureChromoKL', 1, 'keyboard_\\(computer\\)', 'on')]
# !! individual cb09eca7-bc12-49c9-ad9c-27d4ea307ca9 underwent mutation on chromosome 4!
#    [('FeatureChromoCD', 1, 'dyed_bangs', 'on')]

#destination = 'Z:\\programming\\sd_projects\\breed_diffusion\\exp_0002\\gen002\\'
#destination = 'Z:\\programming\\sd_projects\\breed_diffusion\\exp_0002\\gen003\\'
destination = 'Z:\\programming\\sd_projects\\breed_diffusion\\exp_0002\\gen004\\'
for i, individual in enumerate(new_population):
    expression = individual.express()
    submit_job(expression, destination, individual.name)