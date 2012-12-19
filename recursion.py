from PIL import Image
import math
from random import randint

def gif(sauce, frameCount, targetRect):
    """Given a source image `sauce`, return `frameCount` frames
    into `targetRect` target window.
    Returns iterable of PIL.Image"""

    fullSize = sauce.size
    targetSize = (targetRect[2]-targetRect[0], targetRect[3]-targetRect[1])
    ratio = (1.0*fullSize[0]/targetSize[0], 1.0*fullSize[1]/targetSize[1])
    targetCenter = (targetRect[0]/(1 - 1/ratio[0]), targetRect[1]/(1 - 1/ratio[1]))

    def scale(i):
        factor = (math.pow(ratio[0], 1.0*i/frameCount),
                    math.pow(ratio[1], 1.0*i/frameCount))
        return tuple(map(lambda x: x, 
                (targetCenter[0] - targetCenter[0]/ratio[0]*factor[0],
                 targetCenter[1] - targetCenter[1]/ratio[1]*factor[1],
                 targetSize[0] * factor[0],
                 targetSize[1] * factor[1])))

    for frame in range(frameCount):
        dest = Image.new(sauce.mode, fullSize)
        iterations = 1000 # maximum number of iterations allowed per frame
        i = frame + frameCount
        rectum = scale(i)
        while rectum[2] > 1 and rectum[3] > 1 and iterations > 0:
            draw(sauce, rectum, dest)
            i -= frameCount
            rectum = scale(i)
            iterations -= 1

        yield dest
    print targetRect, sauce.size, ratio, targetCenter

def clamp(rectum, dest):
    left, top, w, h = int(rectum[0]), int(rectum[1]), int(rectum[2]), int(rectum[3])
    return (w,h), (left, top, left+w, top+h)

def draw(sauce, target, dest):
    size, box = clamp(target, dest)
    matrix = (sauce.size[0]/target[2], 0, 0, 
              0, sauce.size[1]/target[3], 0)
    scaled = sauce.transform(size, Image.AFFINE, matrix)
    dest.paste(scaled, box)
