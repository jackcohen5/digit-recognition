import os
from PIL import Image
import utilities

def findEndpoints(digitImageArray):

    endpoints = [ -1, -1, -1, -1] # endpoints = [left, top, right, bottom]

    width = len(digitImageArray[0])
    height = len(digitImageArray)

    for column in range(0,width):
        for row in range(0,height):

            if endpoints[0] == -1 and digitImageArray[row][column] == 0:
                endpoints[0] = column

            if endpoints[0] > -1 and digitImageArray[row][column] == 0:
                if row > endpoints[2]:
                    endpoints[2] = column

    for row in range(0,height):
        for column in range(0,width):

            if endpoints[1] == -1 and digitImageArray[row][column] == 0:
                endpoints[1] = row

            if endpoints[1] > -1 and digitImageArray[row][column] == 0:
                if row > endpoints[2]:
                    endpoints[3] = row

    return endpoints

def getAspectRatio(digitImageArray):
	endpoints = findEndpoints(digitImageArray)
	width = endpoints[2] - endpoints[0]
	height = endpoints[3] - endpoints[1]
	float(width)/float(height)
	return float(width)/float(height)

def createVerticalHistogram(digitImageArray):
    histogram = []

    width = len(digitImageArray[0])
    height = len(digitImageArray)

    for column in range(0,width):
        temp = 0.0
        for row in range(0,height):
            temp += float(digitImageArray[row][column])

        blankPixelCount = int(float(temp)/255.0)
        histogram.insert(column,(height - blankPixelCount))

    return histogram

def createHorizontalHistogram(digitImageArray):
    histogram = []

    width = len(digitImageArray[0])
    height = len(digitImageArray)

    for row in range(0,height):
        temp = 0.0
        for column in range(0,width):
            temp += float(digitImageArray[row][column])

        blankPixelCount = int(float(temp)/255.0)
        histogram.insert(column,(width - blankPixelCount))

    return histogram


# this assumes M divides 200 evenly and N divides 100 evenly - need to fix this
def createMxNGrid(M,N,digitImageArray):

    grid = []
    imageWidth = len(digitImageArray[0])
    imageHeight = len(digitImageArray)

    gridRowHeight = int(float(imageHeight)/float(M))
    gridColumnWidth = int(float(imageWidth)/float(N))
    totalPixelInSquare = gridRowHeight*gridColumnWidth

    for row in range(0,M):
        for column in range(0,N):
            temp = 0.0
            for imageRowIndex in range((row*gridRowHeight), (row*gridRowHeight)+gridRowHeight):
                for imageColumnIndex in range((column*gridColumnWidth), (column*gridColumnWidth)+gridColumnWidth):
                    temp += float(digitImageArray[imageRowIndex][imageColumnIndex])

            gridElementPixelCount = int(float(temp)/255.0)
            grid.append(int(totalPixelInSquare) - int(gridElementPixelCount))

    return grid

def saveImageToCorrectDigitFolder(originalImage,correctDigit):
    print 'Okay! Saving the image to the {0} digit bank...'.format(correctDigit)
    digitImagePath = os.getcwd() + '/digits/{0}'.format(correctDigit)
    numImages = 0

    for imageFile in os.listdir(os.getcwd() + '/digits/{0}'.format(correctDigit)):
        if imageFile.endswith(".tiff") or imageFile.endswith(".tif"):
            numImages += 1

    imageFileName = "{0}-{1}".format(correctDigit,numImages)
    imagePath = os.getcwd() + '/digits/{0}/{1}.tif'.format(correctDigit, imageFileName)
    originalImage.save(imagePath)
    print 'Saved as {0}!'.format(imagePath)
    return

def guessedWrong(originalImage):
    print 'WHOOPS!'
    cont = True
    while (cont):
        correctDigit = raw_input("--> Please input the correct digit ('X' to exit): ")
        if correctDigit == 'X' or correctDigit == 'x':
            cont = False
        else:
            if utilities.isInteger(correctDigit):
                for i in range (0,10):
                    if correctDigit == "{0}".format(i):
                        saveImageToCorrectDigitFolder(originalImage,correctDigit)
                        print "Please go back to the main menu and restart the Digit Recognition program to reload the new image into the database!"
                        cont = False
                if cont:
                    print "Command must be an integer from [0,10], or 'X' to exit!"
            else:
                print "Command must be an integer from [0,10], or 'X' to exit!"
    return