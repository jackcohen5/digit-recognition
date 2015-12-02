def isInteger(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def findArrayMode(array):

	frequencies = []
	for i in range(0,10):
		frequencies.append(0)

	for digit in array:
		frequencies[digit] += 1

	return frequencies.index(max(frequencies))