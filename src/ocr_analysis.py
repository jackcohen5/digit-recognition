import numpy
import ocr_utils

def analyzePreResizeDigitImage(digitImage, imageAnalysis):

    digitImageArray = numpy.asarray(digitImage)

    # Aspect ratio
    imageAnalysis['aspectRatio'] = ocr_utils.getAspectRatio(digitImageArray)

    return imageAnalysis

def analyzePostResizeDigitImage(digitImage, imageAnalysis):

    digitImageArray = numpy.asarray(digitImage)

    # Histogram
    imageAnalysis['verticalHistogram'] = ocr_utils.createVerticalHistogram(digitImageArray)
    imageAnalysis['horizontalHistogram'] = ocr_utils.createHorizontalHistogram(digitImageArray)
    imageAnalysis['50x25grid'] = ocr_utils.createMxNGrid(50,25,digitImageArray)
    imageAnalysis['40x20grid'] = ocr_utils.createMxNGrid(40,20,digitImageArray)
    imageAnalysis['20x10grid'] = ocr_utils.createMxNGrid(20,10,digitImageArray)
    imageAnalysis['5x1grid'] = ocr_utils.createMxNGrid(5,1,digitImageArray)
    imageAnalysis['1x5grid'] = ocr_utils.createMxNGrid(1,5,digitImageArray)

    return imageAnalysis