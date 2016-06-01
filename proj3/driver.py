"""
driver.py - Image recognition Driver
CMSC 471 - Spring 2016
Author: Christopher Sidell (csidell1@umbc.edu)
ID: JZ28610

driver.py runs a hash check of the image given against a set of resources
    further training of a hash model could be used to have the system recognize
    what the image is actually of but this is a small project so I opted for the
    simple solution
PYTHON VERSION: 3.5.1

Usage: driver.py <filename>

Dependencies:
    PIL for easy image support (Didn't want to write an image parser)
    numpy for extra matrix math
"""
from PIL import Image
from similarity import find_most_similar
import os
import sys


def main():

    # Determine if valid number of arguments are found
    if len(sys.argv[1:]) == 0:
        print('driver.py <image file>')
        sys.exit(1)

    # Get the image filepath
    imgFp = sys.argv[1]

    # On this specific instance use the /tests folder and check against all of the test cases
    if imgFp == 'ALL':
        testdir = 'tests'
        for fp in os.listdir(testdir):
            # Only handle .jpg and .png
            if fp.endswith('.jpg') or fp.endswith('.png'):
                name = fp
                fp = os.path.join(testdir, fp)
                print(name, 'is found to be a', find_most_similar(Image.open(fp)))
        sys.exit(0)

    # See if file exists
    if not os.path.exists(imgFp):
        print(imgFp, 'file does not exist!')
        sys.exit(1)

    # Load image
    img = Image.open(imgFp)

    # Find most similar image
    print(find_most_similar(img))

main()
