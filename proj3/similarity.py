"""
similarity.py - Checks similarity between given image to a set of resources
CMSC 471 - Spring 2016
Author: Christopher Sidell (csidell1@umbc.edu)
ID: JZ28610
"""
from PIL import Image
from hash import hash
import os


def find_most_similar(image, resource_dir='resources'):
    """
    find_most_similar
    :param image - PIL resource
    :param resource_dir Resource directory
    :return Name of what the image probably is
    """

    lst = []
    # Hash the image
    hashed_image = hash(image)

    # Go through all resources in resource directory
    for name in os.listdir(resource_dir):
        # Join the path names
        path = os.path.join(resource_dir, name)

        # Go through all images in new paths
        for fp in os.listdir(path):

            # Load other image
            compared = Image.open(os.path.join(path, fp))

            # If images are the same, return the name of the image
            if image == compared:
                return name
            else:
                # Otherwise append to the list the name, and hashed value comparison
                lst.append({'name': name, 'value': hash(compared) - hashed_image})

    def comp(a):
        """
        comp
        What key is the comparison being run on?
        """
        return a['value']

    # Sort list with custom key
    lst.sort(key=comp)

    # Return the most likely chance
    return lst[0]['name']
