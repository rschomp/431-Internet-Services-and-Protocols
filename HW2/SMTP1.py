
#turns the parser into the basic engine of an SMTP server by having it process 
#the DATA command to receive and store the contents of a mail message in a file

index = 0 #keeps track of where i am in the string, is updated throughout
fileText = "" #this is where i store the email message 
numRCPT = 0 #make sure we have at least one TO address 
import sys

fromAddress = "" #store from address
toAddress = [] #store to address
#checks to make sure there is only one @ sign, or else it is not valid
def atSign(string):
	global index
	at = 0
	for y in range (index,len(input)):
		if (input[y] == "@"):
			at = at + 1		
	if (at != 1): # if it doesn't have exactly one, throw mailbox error
		state = "mf"
		print "501 Syntax error in parameters or arguments"
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
		state = "mf"
		print "501 Syntax error in parameters or arguments"
		return False
	return True

#checks to make sure MAIL is the first word in the command
def mail(string):
	global index 
	if (string[:4] == "MAIL"):
		index = index + 4
		return True
	else: #if it doesn't match exactly throw mail from command error
		state = "mf"
		print "500 Syntax error: command unrecognized"
		return False

def data(string):
	global index 
	if (string[:4] == "DATA"):
		index = index + 4
		return True
	else: #if it doesn't match exactly throw mail from command error
		state = "mf"
		print "500 Syntax error: command unrecognized"
		return False

def rcptTo(string):
	global index 
	if (string[:4] == "RCPT"):
		index = index + 4
		return True
	else: #if it doesn't match exactly throw mail from command error
		state = "mf"
		print "500 Syntax error: command unrecognized"
		return False

def toLine(string):
	global index 
	if(string[index:index+3] == "TO:"):
		index = index + 3
		return True
	else: #throw error 
		state = "mf"
		print "500 Syntax error: command unrecognized"
		return False

#checks to see if there is whitespace
def whitespace(string):
	global index 
	counter = 0 #counter keeps track of how much whitespace there is
	while (string[index] == " " or string[index] == "\t"):
		index = index + 1
		counter = counter + 1
	if (counter == 0): #if there is no white space, throw error
		state = "mf"
		print "501 Syntax error in parameters or arguments"
		return False
	return True

#checks to make sure FROM: is correct
def fromLine(string):
	global index 
	if(string[index:index+5] == "FROM:"):
		index = index + 5
		return True
	else: #throw error 
		state = "mf"
		print "500 Syntax error: command unrecognized"
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
		state = "mf"
		print "501 Syntax error in parameters or arguments"
		return False
	index = index +1 #update spot in string
	if(mailbox(string) == False): #calls mailbox on the entire string
		return False
	if(string[index] != ">"):
		state = "mf"
		print "501 Syntax error in parameters or arguments"
		return False
	index = index + 1 #update spot in string
	return True

begIndex = 0 #keep track of beginning of address
endIndex = 0 #for end of address
#checks the local part and domain section with @ in between
def mailbox(string):
	global index 
	global begIndex
	global endIndex
	begIndex = index
	if(localPart(string) == False):
		return False
	if (string[index] != "@"):
		state = "mf"
		print "501 Syntax error in parameters or arguments"
		index = index + 1
		return False
	index = index + 1
	if(domain(string) == False): #if false it will make mailbox return false
		return False
	endIndex = index
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
		state = "mf"
		print "501 Syntax error in parameters or arguments"
		return False
	return True

#check if valid domain
def domain(string):
	global index 
	x = 0 #x is a way to see if element is false with no change to index
	if(element(string) == False):
		x = "k"
	if (x == "k"):
		state = "mf"
		print "501 Syntax error in parameters or arguments"
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

#testing mail part
def mailFromFunction(string):
	
	print input #initial print of command
		
	#this chunk is where I actually run the methods
	#if any of these are false, continue to next command		
	if(atSign(input) == False):
		return False
	if(angleBrackets(input) == False):
		return False		
	if (mail(input) == False):
		return False 
	if(whitespace(input) == False):
		return False
	if(fromLine(input) == False):
		return False
	nullspace(input)
	if(reversePath(input) == False):
		return False
	#make sure only whitespace at end of command
	for x in range (index,len(input)):
		if (input[x] != " " and input[x] != "\t"):
			state = "mf"
			print "501 Syntax error in parameters or arguments"
			return False
			break
	
	print "250 OK" #if the command is all good, print this
	return True

#testing rcpt part
def rcptFunction(string):

	print input #initial print of command

	#this chunk is where I actually run the methods
	#if any of these are false, continue to next command		
	if(atSign(input) == False):
		return False
	if(angleBrackets(input) == False):
		return False		
	if (rcptTo(input) == False):
		return False 
	if(whitespace(input) == False):
		return False
	if(toLine(input) == False):
		return False
	nullspace(input)
	if(reversePath(input) == False):
		return False
	#make sure only whitespace at end of command
	for x in range (index,len(input)):
		if (input[x] != " " and input[x] != "\t"):
			state = "mf"
			print "501 Syntax error in parameters or arguments"
			return False
			break
	
	print "250 OK" #if the command is all good, print this
	return True

#testing data part
def dataFunction(string):
	global index
	print input #initial print of command

	#this chunk is where I actually run the methods
	#if any of these are false, continue to next command			
	#if (data(input) == False):
	#	return False 
	index = index + 4

	#make sure only whitespace at end of command
	for x in range (index,len(input)):
		if (input[x] != " " and input[x] != "\t"):
			state = "mf"
			print "501 Syntax error in parameters or arguments"
			return False
			break
	#if the command is all good, print this
	print "354 Start mail input; end with <CRLF>.<CRLF>" 
	return True

state = "mf" #always return state to mf (mailFrom) if there is an error 
#everything checking if you are expecting a mail from command
def mailFromState(string):
	global state
	global fromAddress
	global begIndex
	global endIndex
	if (input[:10] == "MAIL FROM:"):
		if(mailFromFunction(input)): #if you get a valid mail from move to rcpt 
				state = "rt"
				fromAddress = input[begIndex:endIndex] #set from address
	else:
		if (input[:8] == "RCPT TO:"): #expecting mail from
			state = "mf"
			print input
			print "503 Bad sequence of commands"
		
		elif (input[:4] == "DATA" and len(input) == 4): #expected mail from, got DATA
			state = "mf"
			print input
			print "503 Bad sequence of commands"
		elif (len(input) > 4): 
			if (input[:4] == "DATA" and (input[4:] == " " or input[4:] == "\t")): #valid data
				state = "mf"
				print input
				print "503 Bad sequence of commands"
			else: 
				state = "mf"
				print input
				print "500 Syntax error: command unrecognized"
		else: 
			state = "mf"
			print input
			print "500 Syntax error: command unrecognized"

rtCounter = 0 #reset counter

#expecting rcpt command
def rtState(string):
	global state
	global rtCounter
	global toAddress
	if (input[:8] == "RCPT TO:"):
		if(rcptFunction(input)):
			state = "rt"
			rtCounter = rtCounter + 1
			toAddress.append(input[begIndex:endIndex]) #add to address
	else:
		if (rtCounter < 1): #if you don't have at least one to address
			if (input[:4] == "DATA" and len(input) == 4):
				state = "mf"
				print input
				print "503 Bad sequence of commands"
			elif (input[:4] == "DATA" and len(input) > 4): #something after DATA
				if (input[4] == " " or input[4] == "\t"): #valid data command
					state = "mf"
					print input
					print "503 Bad sequence of commands"
				else:
					state = "mf"
					print input
					print "500 Syntax error: command unrecognized" #not valid RCPT
			elif (input[:10] == "MAIL FROM:"):
					state = "mf"
					print input
					print "503 Bad sequence of commands" 
			else:
				state = "mf"
				print input
				print "500 Syntax error: command unrecognized" 

		elif (input[:4] == "DATA" and len(input) == 4): #have at least 1 to address
				print input
				rtCounter = 0
				state = "data" #move to data state
				print "354 Start mail input; end with <CRLF>.<CRLF>" #okay to read in data
		elif (input[:4] == "DATA" and len(input) > 4): #something after DATA
			if(input[4] == " " or input[4] == "\t"):
				if (dataFunction(input)): #call the data function
					state = "data"
				else:
					state = "mf"
					toAddress = [] #clear to address
			else: 
				print input
				state = "mf"
				toAddress = [] #clear to address
				print "500 Syntax error: command unrecognized"
		else:
			rtCounter = 0
			if (input[:10] == "MAIL FROM:"):
				state = "mf"
				print input
				toAddress = []
				print "503 Bad sequence of commands" 
			else:
				state = "mf"
				print input
				toAddress = []
				print "500 Syntax error: command unrecognized"

#checking data 
def dataState(string):
	global fileText
	global state

	while string != ".":
		print string
		fileText = fileText + string + "\n" #add data to file

		string = raw_input() #reads in input
		

	print string
	fileText = fileText[:len(fileText)] #putting all the file lines together
	print "250 OK"
	state = "mf" #return to mf for new input

while True:
	#this is where the program runs through the states and actually executes 
	
	index = 0
	try: 
		input = raw_input() #reads in input
	except EOFError:
		break

	if (state == "mf"):
		mailFromState(input)
		continue
	if(state == "rt"):
		rtState(input)
		continue
	if(state == "data"):
		dataState(input)
		#write the file to linux
		for rcpt in toAddress:
			file = open("forward/" + rcpt, 'a+') 
			file.write("From: <" + fromAddress + ">\n")
			for rcpt2 in toAddress:
				file.write("To: <" + rcpt2 + ">\n")
			file.write(fileText)

		#reset for next input	
		fileText = ""
		toAddress = []
		fromAddress = ""

exit() #end the program



