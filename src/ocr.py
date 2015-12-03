import ocr_machine_learning
from PIL import Image
import os
import digitASCII
from drawDigit import DrawDigit

def phaseThree():

	print "***************************************************"
	print 'Filling the memory bank with sample digits...'
	digitsData = ocr_machine_learning.loadSampleImages()

	cont = True
	while (cont):
		print "***************************************************"
		print "COMMANDS:"
		print " (0) Go back"
		print " (1) Load a digit"
		print " (2) Draw a digit"
		print "***************************************************"
		command = raw_input('Please choose a command: ')
		if (command == '0'):
			cont = False
		elif (command == '1'):
			openImageOCR(digitsData)
		elif (command == '2'):
			print "***************************************************"
			drawDigit = DrawDigit(digitsData)
			drawDigit.startGUI()
		else:
			print "'" + command + "' is not a valid command!"

	return

def openImageOCR(digitsData):

	try: 
		imageFileName = raw_input('--> Please enter name of the digit image file to be recognized (0 to go back): ')
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

		print 'Recognizing the digit...'

		featureVector = ocr_machine_learning.getVector(originalImage,digitsData)
		print 'The feature vector for the image is: {0}'.format(featureVector)
		print "***************************************************"

		finalDigit = ocr_machine_learning.recognizeDigit(featureVector)
		print 'The digit in the image is:'
		print digitASCII.digits[finalDigit]
		print "***************************************************"

	except Exception, e:
		print "Error opening the file!"

	return