#server part to receive input from the client
#turns the parser into the basic engine of an SMTP server by having it process 
#the DATA command to receive and store the contents of a mail message in a file
import sys
from socket import *
serverPort = int(sys.argv[1])

#set up socket
try:
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',serverPort))
	serverSocket.listen(1)
except:
	print "Cannot bind"
	exit()

#checks to make sure there is only one @ sign, or else it is not valid
def atSign(string):
	global index
	global connectionSocket
	at = 0
	for location in range (index,len(string)):
		if (string[location] == "@"):
			at = at + 1		
	if (at != 1): # if it doesn't have exactly one, throw mailbox error
		state = "mf"
		connectionSocket.send("501 Syntax error in parameters or arguments".encode())
		return False
	return True

#checks to make sure there are exactly 2 angle brackets
def angleBrackets(string):
	global index
	global connectionSocket
	twoSigns = 0
	for place in range (index,len(string)):
		if (string[place] == ">" or string[place] == "<"):
			twoSigns = twoSigns + 1		
	if (twoSigns != 2): # if not 2 angle brackets, throw path error
		state = "mf"
		connectionSocket.send("501 Syntax error in parameters or arguments".encode())
		return False
	return True

#checks to make sure MAIL is the first word in the command
def mail(string):
	global index 
	global connectionSocket
	if (string[:4] == "MAIL"):
		index = index + 4
		return True
	else: #if it doesn't match exactly throw mail from command error
		state = "mf"
		connectionSocket.send("500 Syntax error: command unrecognized".encode())
		return False

def data(string):
	global index 
	global connectionSocket
	if (string[:4] == "DATA"):
		index = index + 4
		return True
	else: #if it doesn't match exactly throw mail from command error
		state = "mf"
		connectionSocket.send("500 Syntax error: command unrecognized".encode())
		return False

def rcptTo(string):
	global index 
	global connectionSocket
	if (string[:4] == "RCPT"):
		index = index + 4
		return True
	else: #if it doesn't match exactly throw mail from command error
		state = "mf"
		connectionSocket.send("500 Syntax error: command unrecognized".encode())
		return False

def toLine(string):
	global index 
	global connectionSocket
	if(string[index:index+3] == "TO:"):
		index = index + 3
		return True
	else: #throw error 
		state = "mf"
		connectionSocket.send("500 Syntax error: command unrecognized".encode())
		return False

#checks to see if there is whitespace
def whitespace(string):
	global index 
	global connectionSocket
	counter = 0 #counter keeps track of how much whitespace there is
	while (string[index] == " " or string[index] == "\t"):
		index = index + 1
		counter = counter + 1
	if (counter == 0): #if there is no white space, throw error
		state = "mf"
		connectionSocket.send("501 Syntax error in parameters or arguments".encode())
		return False
	return True

#checks to make sure FROM: is correct
def fromLine(string):
	global connectionSocket
	global index 
	if(string[index:index+5] == "FROM:"):
		index = index + 5
		return True
	else: #throw error 
		state = "mf"
		connectionSocket.send("500 Syntax error: command unrecognized".encode())
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
	global connectionSocket
	global index 
	if(string[index] != "<"):
		state = "mf"
		connectionSocket.send("501 Syntax error in parameters or arguments".encode())
		return False
	index = index +1 #update spot in string
	if(mailbox(string) == False): #calls mailbox on the entire string
		return False
	if(string[index] != ">"):
		state = "mf"
		connectionSocket.send("501 Syntax error in parameters or arguments".encode())
		return False
	index = index + 1 #update spot in string
	return True

#checks the local part and domain section with @ in between
def mailbox(string):
	global index 
	global begIndex
	global endIndex
	global connectionSocket
	begIndex = index
	if(localPart(string) == False):
		return False
	if (string[index] != "@"):
		state = "mf"
		connectionSocket.send("501 Syntax error in parameters or arguments".encode())
		index = index + 1
		return False
	index = index + 1
	if(domain(string) == False): #if false it will make mailbox return false
		return False
	endIndex = index
	return True

#local part should contain a string 
def localPart(string):
	global connectionSocket
	x = 0 #how to keep the index the same when checking both parts
	y = 0
	if (stringS(string) == False):
		x = x + 2
	if (string[index] != "@"):
		y =  y + 4
	if (x == 2 and y == 4):
		state = "mf"
		connectionSocket.send("501 Syntax error in parameters or arguments".encode())
		return False
	return True

#check if valid domain
def domain(string):
	global index 
	global connectionSocket
	x = False #x is a way to see if element is false with no change to index
	if(element(string) == False):
		x = True
	if (x):
		state = "mf"
		connectionSocket.send("501 Syntax error in parameters or arguments".encode())
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
	global connectionSocket
		
	#this chunk is where I actually run the methods
	#if any of these are false, continue to next command		
	if(atSign(string) == False):
		return False
	if(angleBrackets(string) == False):
		return False		
	if (mail(string) == False):
		return False 
	if(whitespace(string) == False):
		return False
	if(fromLine(string) == False):
		return False
	nullspace(string)
	if(reversePath(string) == False):
		return False
	#make sure only whitespace at end of command
	for x in range (index,len(string)):
		if (string[x] != " " and string[x] != "\t"):
			state = "mf"
			connectionSocket.send("501 Syntax error in parameters or arguments".encode())
			return False
			break
	connectionSocket.send("250 OK".encode()) #if the command is all good, send this code
	return True

#testing rcpt part
def rcptFunction(string):
	global connectionSocket

	#this chunk is where I actually run the methods
	#if any of these are false, continue to next command		
	if(atSign(string) == False):
		return False
	if(angleBrackets(string) == False):
		return False		
	if (rcptTo(string) == False):
		return False 
	if(whitespace(string) == False):
		return False
	if(toLine(string) == False):
		return False
	nullspace(string)
	if(reversePath(string) == False):
		return False
	#make sure only whitespace at end of command
	for x in range (index,len(string)):
		if (string[x] != " " and string[x] != "\t"):
			state = "mf"
			connectionSocket.send("501 Syntax error in parameters or arguments".encode())
			return False
			break
	connectionSocket.send("250 OK".encode()) #if the command is all good, send this
	return True

#testing data part
def dataFunction(string):
	global index
	global connectionSocket

	#this chunk is where I actually run the methods
	#if any of these are false, continue to next command			
	#if (data(input) == False):
	#	return False 
	index = index + 4

	#make sure only whitespace at end of command
	for x in range (index,len(string)):
		if (string[x] != " " and string[x] != "\t"):
			state = "mf"
			connectionSocket.send("501 Syntax error in parameters or arguments".encode())
			return False
			break
	#if the command is all good, send this across socket
	connectionSocket.send("354 Start mail input; end with <CRLF>.<CRLF>".encode()) 
	return True

#everything checking if you are expecting a mail from command
def mailFromState(string):
	global state
	global fromAddress
	global begIndex
	global endIndex
	global connectionSocket

	if (input[:10] == "MAIL FROM:"):
		if(mailFromFunction(input)): #if you get a valid mail from move to rcpt 
				state = "rt"
				fromAddress = input[begIndex:endIndex] #set from address
	else:
		if (input[:8] == "RCPT TO:"): #expecting mail from
			state = "mf"
			connectionSocket.send("503 Bad sequence of commands".encode())
		
		elif (input[:4] == "DATA" and len(input) == 4): #expected mail from, got DATA
			state = "mf"
			connectionSocket.send("503 Bad sequence of commands".encode())
		elif (len(input) > 4): 
			if (input[:4] == "DATA" and (input[4:] == " " or input[4:] == "\t")): #valid data
				state = "mf"
				connectionSocket.send("503 Bad sequence of commands".encode())
			else: 
				state = "mf"
				connectionSocket.send("500 Syntax error: command unrecognized".encode())
		else: 
			state = "mf"
			connectionSocket.send("500 Syntax error: command unrecognized".encode())

#expecting rcpt command
def rtState(string):
	global state
	global rtCounter
	global toAddress
	global connectionSocket
	if (input[:8] == "RCPT TO:"):
		if(rcptFunction(input)):
			state = "rt"
			rtCounter = rtCounter + 1
			toAddress.append(input[begIndex:endIndex]) #add to address
	else:
		if (rtCounter < 1): #if you don't have at least one to address
			if (input[:4] == "DATA" and len(input) == 4):
				state = "mf"
				connectionSocket.send("503 Bad sequence of commands".encode())
			elif (input[:4] == "DATA" and len(input) > 4): #something after DATA
				if (input[4] == " " or input[4] == "\t"): #valid data command
					state = "mf"
					connectionSocket.send("503 Bad sequence of commands".encode())
				else:
					state = "mf"
					connectionSocket.send("500 Syntax error: command unrecognized".encode()) #not valid RCPT
			elif (input[:10] == "MAIL FROM:"):
					state = "mf"
					connectionSocket.send("503 Bad sequence of commands".encode()) 
			else:
				state = "mf"
				connectionSocket.send("500 Syntax error: command unrecognized".encode()) 

		elif (input[:4] == "DATA" and len(input) == 4): #have at least 1 to address
				rtCounter = 0
				state = "data" #move to data state
				connectionSocket.send("354 Start mail input; end with <CRLF>.<CRLF>".encode()) #okay to read in data
		elif (input[:4] == "DATA" and len(input) > 4): #something after DATA
			if(input[4] == " " or input[4] == "\t"):
				if (dataFunction(input)): #call the data function
					state = "data"
				else:
					state = "mf"
					toAddress = [] #clear to address
			else: 
				state = "mf"
				toAddress = [] #clear to address
				connectionSocket.send("500 Syntax error: command unrecognized".encode())
		else:
			rtCounter = 0
			if (input[:10] == "MAIL FROM:"):
				state = "mf"
				toAddress = []
				connectionSocket.send("503 Bad sequence of commands".encode()) 
			else:
				state = "mf"
				toAddress = []
				connectionSocket.send("500 Syntax error: command unrecognized".encode())
goBack = False
#checking data 
def dataState(string):
	global fileText
	global state
	global connectionSocket
	global goBack # go back to main while loop to close
	stringList = []
	stringS = ""
	i = 0
	goBack = False

	stringS = stringS + string
	try:
		stringS = stringS + connectionSocket.recv(1024) #reads in input
	except:
		goBack = True #not valid recv
		return

	stringList = stringS.split("\n")
	string = stringList[i]

	while string != ".":
		fileText = fileText + string + "\n" #add data to file
		i = i + 1
		string = stringList[i] 
	fileText = fileText[:len(fileText)] #putting all the file lines together
	fileText = fileText[:-1] #get rid of last new line
	connectionSocket.send("250 OK".encode())
	state = "mf" #return to mf for new input

state = "mf" #always return state to mf (mailFrom) if there ais an error 
index = 0 #keeps track of where i am in the string, is updated throughout
fileText = "" #this is where i store the email message 
numRCPT = 0 #make sure we have at least one TO address 
begIndex = 0 #keep track of beginning of address
endIndex = 0 #for end of address
rtCounter = 0 #reset counter
fromAddress = "" #store from address
toAddress = [] #store to address

while True:
	global connectionSocket
	#socket handshake protocol
	try: #make sure you can connect to server
		connectionSocket, addr = serverSocket.accept()
		
		firstGreeting = "220 snapper.cs.unc.edu"
		connectionSocket.send(firstGreeting.encode())
		theResponse = connectionSocket.recv(1024)
		theResponse = theResponse.decode()

		theResponseList = theResponse.split(" ") #check if include tab

		if (theResponseList[0] != "HELO"):
			connectionSocket.close() #if not correct, close socket
			print ("Invalid HELO command") 
			continue
		
		else:
			secondGreeting = "250 Hello classroom.cs.unc.edu, pleased to meet you"
			connectionSocket.send(secondGreeting.encode())
	except (KeyboardInterrupt): #if there is a keyboard interupt, exit
		print ("Exited from console")
		connectionSocket.close()
		exit()
	except:
		print ("Can't connect to Client")
		connectionSocket.close()
		continue

	while True:
		#this is where the program runs through the states and actually executes 
		index = 0
		#receive lines of data to check
		try:
			input = connectionSocket.recv(1024)
		except:
			print ("Cannot connect to Client")
			connectionSocket.close()
			break

		if (state == "mf"):
			mailFromState(input)
			continue

		if(state == "rt"):
			rtState(input)
			continue
		if(state == "data"):
			dataState(input)
			if (goBack == True): #if you need to go back close the socket, listen now
				connectionSocket.close()
				continue

			#write the file to linux
			domainList = [] #keep track of domains to not have duplicate messages
			for rcpt in toAddress:
				rcpt = rcpt.split("@")
				rcpt = rcpt[1] #title for forward file
				if (rcpt not in domainList):
					domainList.append(rcpt) #add domain to list

					file = open("forward/" + rcpt, "a+")
					file.write("From: <" + fromAddress + ">" + "\n")

					for rcpt2 in toAddress:
						file.write("To: <" + rcpt2 +  ">" +"\n")
					file.write(fileText + "\n") #add all the data
					file.close()

			#reset for next input	
			fileText = ""
			toAddress = []
			fromAddress = ""

		connectionSocket.close()
		break

exit() #end the program


		


