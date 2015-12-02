import os
import numpy
import ocr_utils
import ocr_analysis
from PIL import Image
import utilities

resizeHeight = 200
resizeWidth = 100

def compileImageDatabase(database):
    data = []

    for digit in range(0,10):
        averageDigitAspectRatio = 0
        averageDigitVerticalHistogram = database[digit][0]['verticalHistogram']
        averageDigitHorizontalHistogram = database[digit][0]['horizontalHistogram']
        averageDigit20x10Grid = database[digit][0]['20x10grid']

        for image in range(0,len(database[digit])):
            averageDigitAspectRatio += database[digit][image]['aspectRatio']

            if (image != 0):
                for columnIndex in range(0,len(database[digit][image]['verticalHistogram'])):
                    averageDigitVerticalHistogram[columnIndex] += database[digit][image]['verticalHistogram'][columnIndex]
                for rowIndex in range(0,len(database[digit][image]['horizontalHistogram'])):
                    averageDigitHorizontalHistogram[rowIndex] += database[digit][image]['horizontalHistogram'][rowIndex]

                for squareIndex in range(0,len(database[digit][image]['20x10grid'])):
                    averageDigit20x10Grid[squareIndex] += database[digit][image]['20x10grid'][squareIndex]

        averageDigitAspectRatio = averageDigitAspectRatio/float(len(database[digit]))

        for columnIndex in range(0, len(averageDigitVerticalHistogram)):
            averageDigitVerticalHistogram[columnIndex] = float(averageDigitVerticalHistogram[columnIndex])/float(len(database[digit]))
        for rowIndex in range(0, len(averageDigitHorizontalHistogram)):
            averageDigitHorizontalHistogram[rowIndex] = float(averageDigitHorizontalHistogram[rowIndex])/float(len(database[digit]))
        for squareIndex in range(0,len(database[digit][image]['20x10grid'])):
            averageDigit20x10Grid[squareIndex] = float(averageDigit20x10Grid[squareIndex])/float(len(database[digit]))

        digitData = {
            'aspectRatio': averageDigitAspectRatio,
            'verticalHistogram': averageDigitVerticalHistogram,
            'horizontalHistogram': averageDigitHorizontalHistogram,
            '20x10grid': averageDigit20x10Grid
        }
        data.append(digitData)

    return data

def loadSampleImages():

    database = []

    for index in range(0,10):

        digitData = []

        fullPath = os.getcwd() + '/digits/{0}/'.format(index)
        print 'Loading files for digit {0}...'.format(index)

        for imageFile in os.listdir(fullPath):
            if imageFile.endswith(".tif"): 

                digitImageAnalysis = {}

                imagePath = fullPath + imageFile
                temporaryDigitImage = Image.open(imagePath).convert('L')
                digitImageArray = numpy.asarray(temporaryDigitImage)

                digitImageAnalysis = ocr_analysis.analyzePreResizeDigitImage(digitImageArray, digitImageAnalysis)          # get aspect ratio, ...

                temporaryDigitImage = temporaryDigitImage.crop(ocr_utils.findEndpoints(digitImageArray))                # crop
                temporaryDigitImage = temporaryDigitImage.resize((resizeWidth, resizeHeight))                                  # resize

                digitImageAnalysis = ocr_analysis.analyzePostResizeDigitImage(temporaryDigitImage, digitImageAnalysis)     # get histogram, ...

                digitData.append(digitImageAnalysis)

        database.append(digitData)

    data = compileImageDatabase(database)

    return data

def getRecognized20x10GridDigit(original20x10Grid,data):
    recognized20x10GridDigit = 0
    gridDifference = 0

    for squareIndex in range(0,len(data[0]['20x10grid'])):
        gridDifference += abs(original20x10Grid[squareIndex] - data[0]['20x10grid'][squareIndex])

    for digit in range(0,10):

        averageDigit20x10Grid = data[digit]['20x10grid']
        temp20x10GridDifference = 0

        for squareIndex in range(0,len(averageDigit20x10Grid)):
            temp20x10GridDifference += abs(original20x10Grid[squareIndex] - averageDigit20x10Grid[squareIndex])
        
        if temp20x10GridDifference < gridDifference:
            gridDifference = temp20x10GridDifference
            recognized20x10GridDigit = digit

    return recognized20x10GridDigit

def getRecognizedVerticalHistogramDigit(originalImageVerticalHistogram,data):
    recognizedVerticalHistogramDigit = 0
    verticalHistogramDifference = 0
    for columnIndex in range(0,len(data[0]['verticalHistogram'])):
        verticalHistogramDifference += abs(originalImageVerticalHistogram[columnIndex] - data[0]['verticalHistogram'][columnIndex])

    for digit in range(0,10):

        averageDigitVerticalHistogram = data[digit]['verticalHistogram']
        tempVerticalHistogramDifference = 0
        for columnIndex in range(0,len(averageDigitVerticalHistogram)):
            tempVerticalHistogramDifference += abs(originalImageVerticalHistogram[columnIndex] - averageDigitVerticalHistogram[columnIndex])
        
        if tempVerticalHistogramDifference < verticalHistogramDifference:
            verticalHistogramDifference = tempVerticalHistogramDifference
            recognizedVerticalHistogramDigit = digit
    return recognizedVerticalHistogramDigit

def getRecognizedHorizontalHistogramDigit(originalImageHorizontalHistogram,data):
    recognizedHorizontalHistogramDigit = 0
    horizontalHistogramDifference = 0
    for rowIndex in range(0,len(data[0]['horizontalHistogram'])):
        horizontalHistogramDifference += abs(originalImageHorizontalHistogram[rowIndex] - data[0]['horizontalHistogram'][rowIndex])

    for digit in range(0,10):

        averageDigitHorizontalHistogram = data[digit]['horizontalHistogram']
        tempHorizontalHistogramDifference = 0
        for rowIndex in range(0,len(averageDigitHorizontalHistogram)):
            tempHorizontalHistogramDifference += abs(originalImageHorizontalHistogram[rowIndex] - averageDigitHorizontalHistogram[rowIndex])
        
        if tempHorizontalHistogramDifference < horizontalHistogramDifference:
            horizontalHistogramDifference = tempHorizontalHistogramDifference
            recognizedHorizontalHistogramDigit = digit
    return recognizedHorizontalHistogramDigit

def getRecognizedAspectRatioDigit(originalImageAspectRatio,data):
    recognizedAspectRatioDigit = 0
    aspectRatioDifference = abs(originalImageAspectRatio - data[0]['aspectRatio'])
    for digit in range(0,10):
        if abs(originalImageAspectRatio - data[digit]['aspectRatio']) < aspectRatioDifference:
            aspectRatioDifference = abs(originalImageAspectRatio - data[digit]['aspectRatio'])
            recognizedAspectRatioDigit = digit
    return recognizedAspectRatioDigit

def getVector(originalImage, data):

    originalImageArray = numpy.asarray(originalImage)
    originalImageAspectRatio = ocr_utils.getAspectRatio(originalImageArray)
    originalImage = originalImage.crop(ocr_utils.findEndpoints(originalImageArray))
    originalImage = originalImage.resize((resizeWidth, resizeHeight))

    original20x10Grid = ocr_utils.createMxNGrid(20,10,numpy.asarray(originalImage))
    originalImageVerticalHistogram = ocr_utils.createVerticalHistogram(numpy.asarray(originalImage))
    originalImageHorizontalHistogram = ocr_utils.createHorizontalHistogram(numpy.asarray(originalImage))

    featureVector = []

    recognized20x10GridDigit = getRecognized20x10GridDigit(original20x10Grid,data)
    featureVector.append(recognized20x10GridDigit)

    recognizedVerticalHistogramDigit = getRecognizedVerticalHistogramDigit(originalImageVerticalHistogram,data)
    featureVector.append(recognizedVerticalHistogramDigit)

    recognizedHorizontalHistogramDigit = getRecognizedHorizontalHistogramDigit(originalImageHorizontalHistogram,data)
    featureVector.append(recognizedHorizontalHistogramDigit)

    recognizedAspectRatioDigit = getRecognizedAspectRatioDigit(originalImageAspectRatio,data)
    featureVector.append(recognizedAspectRatioDigit)

    return featureVector

def recognizeDigit(featureVector):
    return utilities.findArrayMode(featureVector)