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
    imageAnalysis['20x10grid'] = ocr_utils.createMxNGrid(20,10,digitImageArray)

    return imageAnalysis