import numpy
from scipy import weave

def ZSThinningIteration(originalImageArray, iteration):
    I, M = originalImageArray, numpy.zeros(originalImageArray.shape, numpy.uint8)

    c_code = """
    for (int i = 1; i < NI[0]-1; i++) {
        for (int j = 1; j < NI[1]-1; j++) {
            int p2 = I2(i-1, j);
            int p3 = I2(i-1, j+1);
            int p4 = I2(i, j+1);
            int p5 = I2(i+1, j+1);
            int p6 = I2(i+1, j);
            int p7 = I2(i+1, j-1);
            int p8 = I2(i, j-1);
            int p9 = I2(i-1, j-1);
            int A  = (p2 == 0 && p3 == 1) + (p3 == 0 && p4 == 1) +
                     (p4 == 0 && p5 == 1) + (p5 == 0 && p6 == 1) +
                     (p6 == 0 && p7 == 1) + (p7 == 0 && p8 == 1) +
                     (p8 == 0 && p9 == 1) + (p9 == 0 && p2 == 1);
            int B  = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9;
            int m1 = iteration == 0 ? (p2 * p4 * p6) : (p2 * p4 * p8);
            int m2 = iteration == 0 ? (p4 * p6 * p8) : (p2 * p6 * p8);
            if (A == 1 && B >= 2 && B <= 6 && m1 == 0 && m2 == 0) {
                M2(i,j) = 1;
            }
        }
    } 
    """

    weave.inline(c_code, ["I", "iteration", "M"])
    return (I & ~M)


def thinImage(originalImageArray):
    thinnedImageArray = originalImageArray.copy() / 255
    prev = numpy.zeros(originalImageArray.shape[:2], numpy.uint8)
    diff = None

    while True:
        thinnedImageArray = ZSThinningIteration(thinnedImageArray, 0)
        thinnedImageArray = ZSThinningIteration(thinnedImageArray, 1)
        diff = numpy.absolute(thinnedImageArray - prev)
        prev = thinnedImageArray.copy()
        if numpy.sum(diff) == 0:
            break

    return thinnedImageArray * 255
