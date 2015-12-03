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