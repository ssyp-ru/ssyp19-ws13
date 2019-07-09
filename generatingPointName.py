def generatePointName(num):
	dictionary = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
	if num <= 26:
		return dictionary[num - 1]
	else:
		firstletter = dictionary[(num // 26) - 1]
		secondletter = dictionary[(num % 26) - 1]
		return firstletter + secondletter

a = int(input())
print(generatePointName(a))
