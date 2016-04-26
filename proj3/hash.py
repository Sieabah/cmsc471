from PIL import Image
import numpy

def hash(image):
    image = image.convert("L").resize((8, 8), Image.ANTIALIAS)
    pixels = numpy.array(image.getdata()).reshape(8, 8)
    avg = pixels.mean()
    diff = pixels > avg

    return Hash(diff)

class Hash():
    def __init__(self, arr):
        self.hash = arr

    def __sub__(self, other):
        return (self.hash.flatten() != other.hash.flatten()).sum()

    def __hash__(self):
        return sum([2**(i % 8) for i, v in enumerate(self.hash.flatten()) if v])