from PIL import Image
from hash import hash
import os


def find_most_similar(image, resource_dir='resources'):
    lst = []
    hashed_image = hash(image)
    for name in os.listdir(resource_dir):
        path = os.path.join(resource_dir, name)
        for fp in os.listdir(path):
            compared = Image.open(os.path.join(path, fp))
            if image == compared:
                return name
            else:
                lst.append({'name': name, 'value': hash(compared) - hashed_image})

    def comp(a):
        return a['value']

    lst.sort(key=comp)

    return lst[0]['name']
