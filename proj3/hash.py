"""
hash.py - Hashing PIL images and how to compare the hashes
CMSC 471 - Spring 2016
Author: Christopher Sidell (csidell1@umbc.edu)
ID: JZ28610
"""
from PIL import Image
import numpy


def hash(image):
    """
    hash
    Hash the given image
    :param image - PIL Image resource
    :return Hash
    """

    image = image.convert("L").resize((8, 8), Image.ANTIALIAS)
    pixels = numpy.array(image.getdata()).reshape(8, 8)
    avg = pixels.mean()
    diff = pixels > avg

    return Hash(diff)


class Hash:
    """
    Hash
    Hash class to handle hash comparisons and functions
    """

    def __init__(self, arr):
        """
        Initialize classes
        """
        self.hash = arr

    def __sub__(self, other):
        """
        Subtraction of Hashes
        """
        return (self.hash.flatten() != other.hash.flatten()).sum()

    def __hash__(self):
        """
        Hash the hash
        """
        return sum([2**(i % 8) for i, v in enumerate(self.hash.flatten()) if v])