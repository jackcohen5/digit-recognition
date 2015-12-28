from Tkinter import Tk,Canvas,Button
from PIL import Image,ImageDraw,ImageOps
import ocr_machine_learning
import ocr_utils
import digitASCII
import os
import utilities

canvasWidth = 100
canvasHeight = 200

class DrawDigit(object):

	def __init__(self, digitsData):
		self.digitsData = digitsData
		self.checkingDigit = False

		self.master = Tk()
		self.master.title("Draw Digit")
		self.master.config(bg='grey',width=canvasWidth*2, height=625,padx=50,pady=50)

		self.isClicking = False
		self.currentX = -1
		self.currentY = -1

		self.canvas = Canvas(self.master, width=canvasWidth, height=canvasHeight)
		self.canvas.config(bg='white')
		self.canvas.pack()

		self.recognizeButton = Button(self.master, text="Recognize", command=self.recognize)
		self.recognizeButton.pack()

		self.clearButton = Button(self.master, text="Clear", command=self.clearCanvas)
		self.clearButton.pack()

		self.rightButton = Button(self.master, text="Right!", command=self.digitRecognized)
		self.rightButton.pack_forget()

		self.wrongButton = Button(self.master, text="Wrong!", command=self.digitNotRecognized)
		self.wrongButton.pack_forget()

		self.retryButton = Button(self.master, text="Retry!", command=self.resetGUI)
		self.retryButton.pack_forget()

		self.master.bind('<Button-1>', self.mousePress)
		self.master.bind('<B1-Motion>', self.mouseMove)
		self.master.bind('<ButtonRelease-1>', self.mouseRelease) 

		self.image = Image.new("L",(canvasWidth,canvasHeight))
		self.draw = ImageDraw.Draw(self.image)

		return


	def mousePress(self, event):
		if not self.isClicking and not self.checkingDigit:
			self.currentX = event.x
			self.currentY = event.y
			self.isClicking = True
		return

	def mouseMove(self, event):
		if self.isClicking and not self.checkingDigit:
			self.draw.line([(self.currentX,self.currentY),(event.x,event.y)],(0,0,0),width=5)
			self.canvas.create_line(self.currentX, self.currentY, event.x, event.y, width=5.0)
			self.currentX = event.x
			self.currentY = event.y
		return

	def mouseRelease(self, event):
		self.isClicking = False
		return

	def clearCanvas(self):
		self.canvas.delete('all')
		self.image = Image.new("L",(canvasWidth,canvasHeight))
		self.draw = ImageDraw.Draw(self.image)
		return

	def recognize(self):
		if len(self.canvas.find_all()) != 0:
			self.checkingDigit = True

			self.originalImage = ImageOps.invert(self.image)
			print "***************************************************"
			print 'Recognizing the digit...'

			featureVector = ocr_machine_learning.getVector(self.originalImage, self.digitsData)
			print 'The feature vector for the image is: {0}'.format(featureVector)

			finalDigit = ocr_machine_learning.recognizeDigit(featureVector)
			print 'The digit in the image is:'
			print digitASCII.digits[finalDigit]

			self.checkCorrectDigitGUI(finalDigit)

		return

	def startGUI(self):
		print 'Please draw the digit in the white square of the GUI window...'
		self.master.mainloop()
		return

	def checkCorrectDigitGUI(self, finalDigit):

		self.finalDigit = finalDigit

		self.recognizeButton.pack_forget()
		self.clearButton.pack_forget()
		self.rightButton.pack()
		self.wrongButton.pack()
		self.retryButton.pack()
		
		self.master.update()

		return

	def digitRecognized(self):
		ocr_utils.saveImageToCorrectDigitFolder(self.originalImage, self.finalDigit)
		self.resetGUI()
		return

	def digitNotRecognized(self):
		ocr_utils.guessedWrong(self.originalImage)
		self.resetGUI()
		return

	def resetGUI(self):
		self.clearCanvas()

		self.rightButton.pack_forget()
		self.wrongButton.pack_forget()
		self.retryButton.pack_forget()
		self.canvas.pack()
		self.recognizeButton.pack()
		self.clearButton.pack()

		self.checkingDigit = False
		print "***************************************************"
		print "Please draw another digit..."

		self.master.update()
		return