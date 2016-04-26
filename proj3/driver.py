from PIL import Image
import sys
import os

def main():

    if len(sys.argv[1:]) == 0:
        print('driver.py <image file>')
        sys.exit(1)

    imgFp = sys.argv[1]

    if not os.path.exists(imgFp):
        print(imgFp, 'file does not exist!')
        sys.exit(1)
    elif not imgFp.endswith('jpg'):
        print('File not supported!')
        sys.exit(1)

    img = Image.open(imgFp)
    pixelArr = img.getdata()

main()