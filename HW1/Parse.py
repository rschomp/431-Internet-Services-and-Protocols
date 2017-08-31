#this program is building a simple string parser 
#to determine if a command (text string) is a valid SMTP command

index = 0 #keeps track of where i am in the string, is updated throughout

#checks to make sure there is only one @ sign, or else it is not valid
def atSign(string):
	global index
	at = 0
	for y in range (index,len(input)):
		if (input[y] == "@"):
			at = at + 1		
	if (at != 1): # if it doesn't have exactly one, throw mailbox error
		print "ERROR -- mailbox"
		return False
	return True

#checks to make sure there are exactly 2 angle brackets
def angleBrackets(string):
	global index
	twoSigns = 0
	for z in range (index,len(input)):
		if (input[z] == ">" or input[z] == "<"):
			twoSigns = twoSigns + 1		
	if (twoSigns != 2): # if not 2 angle brackets, throw path error
		print "ERROR -- path"
		return False
	return True

#checks to make sure MAIL is the first word in the command
def mail(string):
	global index 
	if (string[:4] == "MAIL"):
		index = index + 4
		return True
	else: #if it doesn't match exactly throw mail from command error
		print "ERROR -- mail-from-cmd"
		return False

#checks to see if there is whitespace
def whitespace(string):
	global index 
	counter = 0 #counter keeps track of how much whitespace there is
	while (string[index] == " " or string[index] == "\t"):
		index = index + 1
		counter = counter + 1
	if (counter == 0): #if there is no white space, throw error
		print "ERROR -- mail-from-cmd"
		return False
	return True

#checks to make sure FROM: is correct
def fromLine(string):
	global index 
	if(string[index:index+5] == "FROM:"):
		index = index + 5
		return True
	else: #throw error 
		print "ERROR -- mail-from-cmd"
		return False

#checks nullspace, nullspace can be whitespace
def nullspace(string):
	global index
	while (string[index] == " " or string[index] == "\t"):
		index = index + 1
	return True

#calls path
def reversePath(string):
	if (path(string) == False):
		return False 

#start checking for the < and > and make sure the mailbox in between is valid
def path(string):
	global index 
	if(string[index] != "<"):
		print "ERROR -- path"
		return False
	index = index +1 #update spot in string
	if(mailbox(string) == False): #calls mailbox on the entire string
		return False
	if(string[index] != ">"):
		print "ERROR -- path"
		return False
	index = index + 1 #update spot in string
	return True

#checks the local part and domain section with @ in between
def mailbox(string):
	global index 
	if(localPart(string) == False):
		return False
	if (string[index] != "@"):
		print "ERROR -- mailbox"
		index = index + 1
		return False
	index = index + 1
	if(domain(string) == False): #if false it will make mailbox return false
		return False
	return True

#local part should contain a string 
def localPart(string):
	x = 0 #how to keep the index the same when checking both parts
	y = 0
	if (stringS(string) == False):
		x = x + 2
	if (string[index] != "@"):
		y =  y + 4
	if (x == 2 and y == 4):
		print "ERROR -- local-part"
		return False
	return True

#check if valid domain
def domain(string):
	global index 
	x = 0 #x is a way to see if element is false with no change to index
	if(element(string) == False):
		x = "k"
	if (x == "k"):
		print "ERROR -- domain"
		return False
	if (string[index] == "."): #check if where we are is the .
		index = index + 1
		if (domain(string) == False):
			return False
	return True

#check if there is a valid element
def element(string):
	if(name(string) == False): #call name
		return False
	return True

#check if valid name
def name(string):
	global index 
	if(a(string) == False): 
		#if name starts with something other than a letter, bump above by 1
		return False
	if(letDigStr(string) == False): 
		return False
	return True

#checks if in the alphabet (upper and lower case)
def a(string):
	global index 
	#alphabet holds all the characters in the alphabet
	alphabet = ["a","b", "c", "d", "e", "f", "g", "h", 
	"i", "j", "k", "l", "m", "n", "o", "p", "q", "r", 
	"s", "t", "u", "v", "w", "x", "y", "z", "A", "B",
	"C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
	"M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
	"W", "X", "Y", "Z"]
	if(string[index] not in alphabet):
		index = index + 1
		return False
	index = index + 1
	return True

#checks if there is at least a letter/digit
def letDigStr(string):
	global index 
	if (letDig(string) == False):
		return False
	while (letDig(string) == True):
		continue
	return True

#holds both letters and digits for when testing letDig
def ad(string):
	global index
	both = ["a","b", "c", "d", "e", "f", "g", "h", 
	"i", "j", "k", "l", "m", "n", "o", "p", "q", "r", 
	"s", "t", "u", "v", "w", "x", "y", "z", "A", "B",
	"C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
	"M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
	"W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", 
	"6", "7", "8", "9"]
	if (string[index] not in both):
		return False
	index = index + 1
	return True

#must be a letter or a digit
def letDig(string):
	global index
	if(ad(string) == False):
		return False
	return True

#checks if it is a valid string
def stringS(string):
	global index 
	if (char(string) == False): #call char
		return False
	stringS(string) #recursive call to string
	return True

#checks if valid char
def char(string):
	if (c(string) == False): #call c
		return False
	return True

#checks if valid c
def c(string):
	global index
	if (sP(string) == True): #if there is a space return false
		return False
	if(special(string) == True):
		return False
	if (asciiCount(string) == True): #can be any one of 128 ascii 
		return False	
	if (string[index] == "@"):
		return False
	index = index + 1
	return True

#tests if it is an ascii character within range
def asciiCount(string):
	global index
	if (ord(string[index]) >= 128):
		return True
	return False

#checks if there is space, space or tab
def sP(string):
	global index 
	if(string[index] == " "):
		return True
	if(string[index] == "\t"):
		return True
	return False

#checks if there is a special character, if so return true
def special(string):
	global index
	specialArray = ["<", ">", "(", ")", "[", "]",
	 "\\", ".", ",", ";", ":", '"']
	if (string[index] in specialArray):
		index = index + 1
		return True
	return False

#main function that runs through text/mail commands	
while True:
	index = 0
	extraAtEnd = 0 
	try: 
		input = raw_input() #reads in input
	except EOFError:
		break

	print input #initial print of command
	
	#this chunk is where I actually run the methods
	#if any of these are false, continue to next command
	if(atSign(input) == False):
		continue
	if(angleBrackets(input) == False):
		continue
	if (mail(input) == False):
		continue 
	if(whitespace(input) == False):
		continue
	if(fromLine(input) == False):
		continue
	nullspace(input)
	if(reversePath(input) == False):
		continue
	#make sure only whitespace at end of command
	for x in range (index,len(input)):
		if (input[x] != " " or input[x] != "\t"):
			print "ERROR -- mail-from-cmd"
			extraAtEnd = extraAtEnd + 1
			break
	if (extraAtEnd == 0):
		print "Sender ok" #if the command is all good, print this
exit() #end the program



