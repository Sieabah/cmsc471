from PIL import Image
from similarity import find_most_similar
import os
import sys


def main():

    if len(sys.argv[1:]) == 0:
        print('driver.py <image file>')
        sys.exit(1)

    imgFp = sys.argv[1]

    if imgFp == 'ALL':
        testdir = 'tests'
        for fp in os.listdir(testdir):
            if fp.endswith('.jpg') or fp.endswith('.png'):
                name = fp
                fp = os.path.join(testdir, fp)
                print(fp, 'is found to be a', find_most_similar(Image.open(fp)))
        sys.exit(0)

    if not os.path.exists(imgFp):
        print(imgFp, 'file does not exist!')
        sys.exit(1)

    img = Image.open(imgFp)

    print(find_most_similar(img))

main()
