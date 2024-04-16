import os
from PIL import Image
from infrastucture import *

root_dir = 'Z:/programming/sd_projects/breed_diffusion/exp_0002'

def find_image_path(root_dir, image_id):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.startswith(image_id):
                return os.path.join(subdir, file)
    return None

def stitch_images_horizontally(images):
    if not images:
        return None
    total_width = sum(img.size[0] for img in images)
    max_height = max(img.size[1] for img in images)
    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in images:
        y_offset = (max_height - img.size[1]) // 2  # Vertically center the image
        new_im.paste(img, (x_offset, y_offset))
        x_offset += img.size[0]

    return new_im

def stitch_images_vertically(images):
    max_width = max(img.size[0] for img in images)
    total_height = sum(img.size[1] for img in images)
    new_im = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for img in images:
        x_offset = (max_width - img.size[0]) // 2  # Center the image horizontally
        new_im.paste(img, (x_offset, y_offset))
        y_offset += img.size[1]

    return new_im

def flatten_tree(tree):
   graph = {}
   def process_node(node):
       if node[1]:
           children_names = tuple(child[0] for child in node[1])
           graph[node[0]] = children_names
           for child in node[1]:
               process_node(child)
   process_node(tree)
   return graph
 
def traverse(row_spec, graph):
    results = []

    def descend(node_and_width, graph):
        node, width = node_and_width
        children = graph.get(node, (None,))
        return [(child, width/len(children)) for child in children]

    node_names = [x[0] for x in row_spec]
    while any(node_names):
        results.append(row_spec)
        new_spec = []
        for item in row_spec:
            new_spec.extend(descend(item, graph))
        row_spec = new_spec
        node_names = [x[0] for x in row_spec]
    return results

def load_and_scale(fn_width_tuple, root_dir):
    fn, width = fn_width_tuple
    image_path = find_image_path(root_dir, fn)
    if not image_path:
        return None
    image = Image.open(image_path)
    scale_factor = width / image.size[0]
    new_height = scale_factor * image.size[1]
    return image.resize((int(width), int(new_height)), Image.LANCZOS)

if __name__ == "__main__":
    import random
    gen005 = unserialize_individuals('gen005.json', chromosome_classes)
    pick = random.choice(gen005)
    for pick in gen005:
        tree = [pick.name, pick.parentage]
        flattened = flatten_tree(tree)
        root_image_path = find_image_path(root_dir, pick.name)
        if root_image_path:
            root_image = Image.open(root_image_path)
            overall_width = root_image.size[0]
            instructions = traverse([(pick.name, overall_width)], flattened)
            image_rows = []
            for row in instructions:
                row_images = [load_and_scale(x, root_dir) for x in row]
                image_rows.append(stitch_images_horizontally(row_images))
            combined = stitch_images_vertically(image_rows)
            combined.save(f'{pick.name}-parents.png')
