import numpy
import thinning
import kernels
from scipy import ndimage
from PIL import Image
import os
import utilities

# PHASE 1 FUNCTIONS
def phaseOne():

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

	filterFunction(originalImage)

	cont = True
	while (cont):
		print "***************************************************"
		print "COMMANDS:"
		print " (0) Go back"
		print " (1) Choose a different filter"
		print " (2) Load another image"
		print "***************************************************"
		command = raw_input('Please choose a command: ')
		if (command == '0'):
			cont = False
		elif (command == '1'):
			filterFunction(originalImage)
		elif (command == '2'):
			phaseOne()
			cont = False
		else:
			print "'" + command + "' is not a valid command!"


	return

def filterFunction(originalImage):
	print 'Kernel Types:'
	for kernelIndex in range(0,len(kernels.kernels)):
		print '({0}) {1}'.format(kernelIndex, kernels.kernels[kernelIndex]['name'])
	print '({0}) ZS Thinning'.format(len(kernels.kernels))

	cont = True
	while (cont):
		command = raw_input('--> Please choose a filter: ')
		if (utilities.isInteger(command)):
			command = int(command)
			if (command >= 0 and command <= (len(kernels.kernels))):
				cont = False
			else:
				print "Must be an integer in the range [0, {0}]!".format(len(kernels.kernels))

		else:
			print "Must be an integer in the range [0, {0}]!".format(len(kernels.kernels))

	if command == len(kernels.kernels):
		print 'Thinning...'
		thinnedImage = thinningFilter(originalImage)
		thinnedImage.show()
		print 'Saving the thinned image to the output folder as thinnedImage.jpg...'
		thinnedImage.save(os.getcwd() + '/output/thinnedImage.jpg')
	else:

		multiplier = 1.0/float(kernels.kernels[command]['factor'])

		print 'Applying the filter - {0}...'.format(kernels.kernels[command]['name'])
		filteredImage = apply3x3Filter(originalImage,kernels.kernels[command]['kernel'],multiplier)
		# filteredImage = Image.fromarray(ndimage.convolve(numpy.asarray(originalImage),kernels.kernels[command]['kernel']))
		print 'Displaying the image with the applied filter - {0}...'.format(kernels.kernels[command]['name'])
		filteredImage.show()
		print 'Saving the image with the applied filter to the output folder as filteredImage.jpg...'
		filteredImage.save(os.getcwd() + '/output/filteredImage.jpg')

	return

def apply3x3Filter(originalImage, filterArray, multiplier):
	
	width = int(originalImage.size[0])
	height = int(originalImage.size[1])

	originalImageArray = numpy.asarray(originalImage)
	filteredImageArray = originalImageArray.copy()

	for row in range(0, width):
		for column in range(0,height):
			
			C1 = C2 = C3 = C4 = C5 = C6 = C7 = C8 = C9 = 0
			left = row - 1
			right = row + 1
			up = column - 1
			down = column + 1

			if (left >= 0 and up >= 0):
				C1 = originalImageArray[left][up] * filterArray[0][0]

			if (left >= 0):
				C2 = originalImageArray[left][column] * filterArray[0][1]

			if (left >= 0 and down < height):
				C3 = originalImageArray[left][down] * filterArray[0][2]

			if (up >= 0):
				C4 = originalImageArray[row][up] * filterArray[1][0]

				C5 = originalImageArray[row][column] * filterArray[1][1]

			if (down < height):
				C6 = originalImageArray[row][down] * filterArray[1][2]

			if (right < width and up >= 0):
				C7 = originalImageArray[right][up] * filterArray[2][0]

			if (right < width):
				C8 = originalImageArray[right][column] * filterArray[2][1]

			if (right < width and down < height):
				C9 = originalImageArray[right][down] * filterArray[2][2]

			filteredImageArray[row][column] = (C1 + C2 + C3 + C4 + C5 + C6 + C7 + C8 + C9)*multiplier

	filteredImage = Image.fromarray(filteredImageArray)

	return filteredImage

def thinningFilter(originalImage):

	originalImageArray = numpy.asarray(originalImage)

	filteredImageArray = thinning.thinImage(originalImageArray)

	# Convert back to PIL image
	filteredImage = Image.fromarray(filteredImageArray)

	return filteredImage

# END PHASE 1 FUNCTIONS
