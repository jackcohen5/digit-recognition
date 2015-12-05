import filters
import features
import ocr
import os

# MAIN FUNCTION
def main():
	
	path = os.getcwd() + '/output'
	if not os.path.exists(path):
	    os.makedirs(path)

	try:
		printIntro()

		cont = True
		while (cont):
			print "***************************************************"
			print "COMMANDS:"
			print " (1) Image Filters and Thinning - Phase 1"
			print " (2) Feature Extraction - Phase 2"
			print " (3) Digit Recognition - Phase 3"
			print " (0) Exit"
			print "***************************************************"
			command = raw_input('Please choose a command: ')
			if (command == '0'):
				cont = False
			elif (command == '1'):
				filters.phaseOne()
			elif (command == '2'):
				features.phaseTwo()
			elif (command == '3'):
				ocr.phaseThree()
			else:
				print "'" + command + "' is not a valid command!"

	except Exception, e:
		print "Error!"
		print str(e)
		main()

	finally:
		return

def printIntro():
	print """ _____ _ _ _                 __  _____ _     _             _               
|  ___(_) | |_ ___ _ __     / / |_   _| |__ (_)_ __  _ __ (_)_ __   __ _   
| |_  | | | __/ _ \ '__|   / /    | | | '_ \| | '_ \| '_ \| | '_ \ / _` |  
|  _| | | | ||  __/ |     / /     | | | | | | | | | | | | | | | | | (_| |  
|_|   |_|_|\__\___|_|    /_/      |_| |_| |_|_|_| |_|_| |_|_|_| |_|\__, |  
  __ _ _ __   __| |                                                |___/   
 / _` | '_ \ / _` |                                                        
| (_| | | | | (_| |                                                        
 \__,_|_| |_|\__,_|                                                        
 ____  _       _ _     ____                            _ _   _             
|  _ \(_) __ _(_) |_  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __  
| | | | |/ _` | | __| | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \ 
| |_| | | (_| | | |_  |  _ <  __/ (_| (_) | (_| | | | | | |_| | (_) | | | |
|____/|_|\__, |_|\__| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
 ____    |___/       _            _       _|___/    _                      
| __ ) _   _ _      | | __ _  ___| | __  / ___|___ | |__   ___ _ __        
|  _ \| | | (_)  _  | |/ _` |/ __| |/ / | |   / _ \| '_ \ / _ \ '_ \       
| |_) | |_| |_  | |_| | (_| | (__|   <  | |__| (_) | | | |  __/ | | |      
|____/ \__, (_)  \___/ \__,_|\___|_|\_\  \____\___/|_| |_|\___|_| |_|
        |___/"""
	return

if __name__ == '__main__':
	main()