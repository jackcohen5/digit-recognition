import numpy
import scipy
from scipy import ndimage
from PIL import Image
import os

# PHASE 2 FUNCTIONS
def phaseTwo():

	print "***************************************************"

	imageFileName = raw_input('--> Please enter the image file name (0 to go back): ')
	if imageFileName == '0':
		return
	print 'Opening '  + imageFileName + '...'
	imageFileName = os.getcwd() + '/images/' + imageFileName
	originalImage = Image.open(imageFileName).convert('L')
	print '    Image Format: {0}'.format(originalImage.format)
	print '    Image Mode: {0}'.format(originalImage.mode)
	print '    Image Size: {0}'.format(originalImage.size)
	print 'Converting the original file to grayscale and displaying...'
	originalImage.show()
	print "***************************************************"

	print 'Extracting features from the image...'

	edgeDetectedImage = sobelEdgeDetection(originalImage)
	print 'Displaying the Sobel edge detected image...'
	edgeDetectedImage.show()
	print 'Saving the Sobel edge detected image to the output folder...'
	edgeDetectedImage.save(os.getcwd() + '/output/sobelEdgeDetectedImage.jpg')

	blobDetectedImage = gaussianLaplaceBlobDetection(originalImage)
	print 'Displaying the blob detected image...'
	blobDetectedImage.show()
	print 'Saving the blob detected image to the output folder...'
	blobDetectedImage.save(os.getcwd() + '/output/blobDetectedImage.jpg')

	cont = True
	while (cont):
		print "***************************************************"
		print "COMMANDS:"
		print " (0) Go back"
		print " (1) Load another image"
		print "***************************************************"
		command = raw_input('Please choose a command: ')
		if (command == '0'):
			cont = False
		elif (command == '1'):
			phaseTwo()
			cont = False
		else:
			print "'" + command + "' is not a valid command!"


	return

def sobelEdgeDetection(originalImage):
	originalImageArray = numpy.asarray(originalImage)
	edgeDetectedImageArray = ndimage.sobel(originalImageArray)
	edgeDetectedImage = Image.fromarray(edgeDetectedImageArray)
	return edgeDetectedImage

def gaussianLaplaceBlobDetection(originalImage):
	originalImageArray = numpy.asarray(originalImage)
	blobDetectedImageArray = ndimage.gaussian_laplace(originalImageArray,sigma=2)
	blobDetectedImage = Image.fromarray(blobDetectedImageArray)
	return blobDetectedImage

# END PHASE 2 FUNCTIONS
