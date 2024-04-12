import json
from urllib import request
from chromosome import *
from individual import *

# Example usage
chromosome_classes = {
    'Chromosome': Chromosome,
    'FeatureChromo11': FeatureChromo11,
    'FeatureChromoAB': FeatureChromoAB,
    'FeatureChromoCD': FeatureChromoCD,
    'FeatureChromoEF': FeatureChromoEF,
    'FeatureChromoGH': FeatureChromoGH,
    'FeatureChromoIJ': FeatureChromoIJ,
    'FeatureChromoKL': FeatureChromoKL,
    'FeatureChromoMN': FeatureChromoMN,
    'FeatureChromoOP': FeatureChromoOP,
    'FeatureChromoQR': FeatureChromoQR,
    'FeatureChromoST': FeatureChromoST,
    'FeatureChromoUV': FeatureChromoUV,
    'FeatureChromoWX': FeatureChromoWX,
    'FeatureChromoYZ': FeatureChromoYZ,
    'QualityChromo': QualityChromo,
    'SizeChromo': SizeChromo,
}

def serialize_individuals(individuals, file_name):
    def individual_to_dict(ind):
        return {
            'name': ind.name,
            'chromosomes': [
                {
                    'type': type(chromosome).__name__,
                    'genes': [list(genes) for genes in chromosome.genes],
                    # Add additional properties here if needed
                }
                for chromosome in ind.chromosomes
            ],
            'parentage': ind.parentage
        }

    with open(file_name, 'w') as file:
        json.dump([individual_to_dict(ind) for ind in individuals], file)

def unserialize_individuals(file_name, chromosome_classes):
    def dict_to_individual(ind_data):
        ind = Individual()
        ind.name = ind_data['name']
        ind.parentage = ind_data['parentage']
        for chromosome_data in ind_data['chromosomes']:
            chromosome_class = chromosome_classes[chromosome_data['type']]
            chromosome = chromosome_class(*[set(genes) for genes in chromosome_data['genes']])
            ind.add_chromosome(chromosome)
        return ind

    with open(file_name, 'r') as file:
        individuals_data = json.load(file)
        return [dict_to_individual(ind_data) for ind_data in individuals_data]

def submit_job(expression, folder, filename):
    def submit_workflow(wf, url='127.0.0.1'):
        req = request.Request(f'http://{url}:8188/prompt', data=wf)
        res = request.urlopen(req)
        return res
    
    width, height = (832, 832)
    if 'meta_bigsquare' in expression:
        width, height = (1024, 1024)
        expression = expression.replace('meta_bigsquare', '')
    elif 'meta_portrait' in expression:
        width, height = (832, 1216)
        expression = expression.replace('meta_portrait', '')
    elif 'meta_landscape' in expression:
        width, height = (1216, 832)
        expression = expression.replace('meta_landscape', '')
    elif 'meta_square' in expression:
        width, height = (512, 512)
        expression = expression.replace('meta_square', '')
    
    while ', ,' in expression:
        expression = expression.replace(', ,', ',')

    with open('breed_diffusion.api.json', 'rt', encoding = 'utf-8') as fh:
        workflow_object = json.load(fh)

    workflow_object['326']['inputs']['empty_latent_width'] = width
    workflow_object['326']['inputs']['empty_latent_height'] = height
    workflow_object['621']['inputs']['text'] = expression
    workflow_object['624']['inputs']['path'] = folder
    workflow_object['624']['inputs']['filename'] = filename

    wrapped_workflow = {'prompt': workflow_object}
    wrapped_string = json.dumps(wrapped_workflow).encode('utf-8')
    submit_workflow(wrapped_string)

def boot_population(bf = 'initial.json'):
    bulk = """1girl, solo, looking_at_viewer, smile, short_hair, open_mouth, shirt, long_sleeves, brown_eyes, standing, white_shirt, pink_hair, flower, :d, cowboy_shot, outdoors, sky, teeth, pants, hand_up, denim, arm_behind_back, sunset, hand_in_pocket, waving, overalls, field
1girl, solo, long_hair, breasts, looking_at_viewer, blush, smile, large_breasts, shirt, red_eyes, holding, cleavage, jewelry, collarbone, white_shirt, pink_hair, purple_hair, multicolored_hair, cowboy_shot, earrings, glasses, collared_shirt, pants, necklace, nail_polish, mole, vest, covered_nipples, two-tone_hair, fur_trim, thigh_gap, black_pants, staff, black_vest, holding_staff, amulet
1girl, solo, breasts, looking_at_viewer, short_hair, large_breasts, shirt, cleavage, jewelry, collarbone, yellow_eyes, upper_body, red_hair, earrings, choker, black_shirt, makeup, blurry_background, piercing, ear_piercing, red_lips, mechanical_arms, cyborg, single_mechanical_arm, prosthesis, prosthetic_arm
1girl, solo, breasts, looking_at_viewer, short_hair, large_breasts, dress, holding, animal_ears, cleavage, green_eyes, tail, cowboy_shot, outdoors, parted_lips, green_hair, cat_ears, blurry, lips, fingernails, cat_tail, animal_ear_fluff, torn_clothes, bell, blood, night, blurry_background, bandages, moon, cat_girl, staff, night_sky, jingle_bell, neck_bell, full_moon, halloween, plump, holding_staff, sharp_fingernails, halloween_costume, bat_\(animal\), torn_dress
solo, looking_at_viewer, smile, red_eyes, 1boy, male_focus, teeth, fingernails, book, muscular, glowing, colored_skin, glowing_eyes, open_book, grey_skin, crack
solo, 1boy, holding, standing, full_body, weapon, male_focus, boots, outdoors, belt, sword, hood, holding_weapon, armor, holding_sword, helmet, shoulder_armor, gauntlets, facing_viewer, 1other, hood_up, pauldrons, breastplate, greaves, full_armor, ambiguous_gender, chainmail
1girl, solo, long_hair, breasts, skirt, large_breasts, brown_hair, dress, holding, cleavage, jewelry, earrings, indoors, necklace, armor, lips, makeup, lipstick, shoulder_armor, facing_viewer, blindfold, red_lips, candle, mechanical_arms, coin, single_mechanical_arm, gold
grey_background, gradient, military, gradient_background, no_humans, robot, ground_vehicle, mecha, motor_vehicle, machinery, science_fiction, turret, cannon, military_vehicle, cable, tank, vehicle_focus, caterpillar_tracks, non-humanoid_robot
1girl, solo, breasts, looking_at_viewer, large_breasts, gloves, dress, holding, cleavage, standing, full_body, boots, wings, black_gloves, hood, black_footwear, black_dress, torn_clothes, capelet, moon, knee_boots, staff, facing_viewer, corset, cross-laced_footwear, hood_up, dual_wielding, lace-up_boots, covered_eyes
1girl, solo, long_hair, breasts, looking_at_viewer, blue_eyes, large_breasts, cleavage, bare_shoulders, jewelry, blue_hair, upper_body, earrings, outdoors, glasses, sleeveless, choker, necklace, lips, tattoo, ground_vehicle, building, scenery, motor_vehicle, hoop_earrings, city, sign, realistic, round_eyewear, car, road, motorcycle, power_lines, street""".split('\n')
    
    initial_population = []
    qual = QualityChromo({'score_9', 'score_8', 'score_7', 'score_6', 'score_5', 'score_4', 'rating_safe'})
    sizs = SizeChromo({'large_width', 'large_height'})
    sizp = SizeChromo({'large_height'})
    sizl = SizeChromo({'large_width'})

    for i in range(10):
        feat_set = set(bulk[i].split(', '))
        ind = Individual()
        ind.add_chromosome(qual)
        ind.add_chromosome(sizs if i != 9 else sizl)
        ind.add_chromosome(FeatureChromo11(feat_set))
        ind.add_chromosome(FeatureChromoAB(feat_set))
        ind.add_chromosome(FeatureChromoCD(feat_set))
        ind.add_chromosome(FeatureChromoEF(feat_set))
        ind.add_chromosome(FeatureChromoGH(feat_set))
        ind.add_chromosome(FeatureChromoIJ(feat_set))
        ind.add_chromosome(FeatureChromoKL(feat_set))
        ind.add_chromosome(FeatureChromoMN(feat_set))
        ind.add_chromosome(FeatureChromoOP(feat_set))
        ind.add_chromosome(FeatureChromoQR(feat_set))
        ind.add_chromosome(FeatureChromoST(feat_set))
        ind.add_chromosome(FeatureChromoUV(feat_set))
        ind.add_chromosome(FeatureChromoWX(feat_set))
        ind.add_chromosome(FeatureChromoYZ(feat_set))
        initial_population.append(ind)
    serialize_individuals(initial_population, bf)