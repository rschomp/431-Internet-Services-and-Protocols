#validate incoming message, send to server to create file 
#necessary to send the contents of the mail messages in the forward-file to a 
#destination SMTP server

#variables to track the addresses and data
toAddress = []
fromAddress = ""
mailData = []
import sys
from socket import *

#requests user input and echos the message specific to 250
def command250():
	global clientSocket
	try:
		userInput = clientSocket.recv(1024)  #here is the problem 
	except:
		clientSocket.close()
		print ("Cannot receive from server")
		exit()
	if (userInput == ""):
		print ("Cannot be empty")
		clientSocket.close() 
		exit()
	inputList = userInput.split()
	if (inputList[0] != "250"):
		print ("This was not a 250 command")
		clientSocket.close()
		exit()

#handles the mail from address 
def mailFrom():
	global clientSocket
	clientSocket.send(("MAIL FROM: " + fromAddress).encode()) 
	command250()

#handles the one or more to addresses
def rcptTo():
	global clientSocket
	for rcpt in toAddress:
		clientSocket.send("RCPT TO: " + rcpt.encode()) 
		command250()		

#handles the printing of the data and following format
def data():
	global clientSocket
	clientSocket.send("DATA".encode())

	#print 354, specific to data section
	try:
		userInput = clientSocket.recv(1024) #make sure you can receive
	except:
		clientSocket.close()
		print "Cannot receive from server"
		exit()

	if (userInput == ""):
		print ("Data cannot be empty")
		clientSocket.close()
		exit()
	inputList = userInput.split()
	if (inputList[0] != "354"):
		print ("This was not a 354")
		clientSocket.close()
		exit()
	for dataText in mailData: 
		clientSocket.send(dataText.encode()) #sends the data lines in order
	clientSocket.send("\n.".encode())

	try:
		userInput = clientSocket.recv(1024)
	except:
		clientSocket.close()
		print "Cannot receive from server"
		exit()

	if (userInput == ""):
		print ("Cannot be empty")
		clientSocket.close()
		exit()
	inputList = userInput.split(" ")
	if (inputList[0] != "250"):
		print ("This was not a 250")
		clientSocket.close()
		exit()

index = 0 #keeps track of where i am in the string, is updated throughout

#checks to make sure there is only one @ sign, or else it is not valid
def atSign(string):
	global index
	at = 0
	for y in range (index,len(string)):
		if (string[y] == "@"):
			at = at + 1		
	if (at != 1): # if it doesn't have exactly one, throw mailbox error
		print "ERROR -- mailbox"
		return False
	return True

#checks to make sure there are exactly 2 angle brackets
def angleBrackets(string):
	global index
	twoSigns = 0
	for z in range (index,len(string)):
		if (string[z] == ">" or string[z] == "<"):
			twoSigns = twoSigns + 1		
	if (twoSigns != 2): # if not 2 angle brackets, throw path error
		print "ERROR -- path"
		return False
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

index = 0
#checks to make sure user input is valid before sending it
def checker(string):
	global index
	index = 0
	extraAtEnd = 0 
	
	#this chunk is where I actually run the methods
	if(atSign(string) == False):
		return False
	if(angleBrackets(string) == False):
		return False
	if(reversePath(string) == False):
		return False
	#make sure only whitespace at end of command
	for x in range (index,len(string)):
		if (string[x] != " " and string[x] != "\t"):
			print "ERROR -- mail-from-cmd"
			extraAtEnd = extraAtEnd + 1
			return False
	if (extraAtEnd == 0):
		return True

#main method to handle the socket and calling the specific methods
def main():
	global fromAddress
	global toAddress
	global mailData
	global clientSocket

	toInputFileText = []
	while True:
		fromInput = ""
		toInputAddress = ""
		subjectInput = ""
		messageInput = ""
		try:
			fromInput = raw_input('From: ') #make sure you get a from 
		except (EOFError): #if you reach end of file, exit
			print "End of File reached"
			exit()
		fromInput = "<" + fromInput + ">" 

		if (checker(fromInput) == False):
			print ("Enter valid From:")
			continue
		
		didItFail = True
		while didItFail: #validating To: addresses
			try:
				toInput = raw_input('To: ')
			except (EOFError):
				print "End of File reached"
				exit()
			
			toInputList = toInput.split(',') #get individual addresses
			
			for toInputAddress in toInputList:
				toInputAddress = toInputAddress.lstrip() #get rid of whitespace
				toInputAddress = "<" + toInputAddress + ">"
				if (checker(toInputAddress) == False): #validate
					print ("Enter valid To:")
					didItFail = True
					break
				else:
					didItFail = False
				
				toInputFileText.append(toInputAddress) #add address

			if (didItFail): #get more input
				continue
			didItFail = False #allows to break out
		if (didItFail == False): #break out of loop
			break

	try:
		subjectInput = raw_input('Subject: ') #get subject from user
	except (EOFError):
		print "End of File reached"
		exit()

	print "Message:" #ask for message
	try:
		messageInput = raw_input() #get message from user 
	except (EOFError):
		print "End of File reached"
		exit()
	
	messageInputList = []

	while messageInput != ".": #while not on last line of .
		messageInputList.append(messageInput + "\n")
		try:
			messageInput = raw_input() #get message from user 
		except (EOFError):
			print "End of File reached"
			exit() 
	
	#client socket
	try: #make sure you connect ot socket
		serverName = sys.argv[1]
		serverPort = int(sys.argv[2])

		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect((serverName,serverPort))

		sentence = clientSocket.recv(1024)
		sentence = sentence.decode()

		sentenceList = sentence.split(" ")

		if (sentenceList[0] == "220"):
			greeting = "HELO classroom.cs.unc.edu"
			clientSocket.send(greeting.encode())
			theResponse = clientSocket.recv(1024)
			theResponse = theResponse.decode()
		else:
			clientSocket.close()
			print ("Error response code")
			exit()
	except:
		clientSocket.close()
		print ("Cannot connect to server")
		exit()

	newSentence = theResponse
	newSentenceList = newSentence.split(" ")

	if (newSentenceList[0] != "250"): #make sure what you get back starts with 250
		clientSocket.close()
		print ("Error response code")
		exit()

	fromAddress = fromInput
	mailFrom()

	toAddress = toInputFileText
	rcptTo()

	mailData.append("From: " + fromInput + "\n") #add from address to data
	
	for slots in toInputFileText:
		mailData.append("To: " + slots + "\n")	#add to

	mailData.append("Subject: " + subjectInput)
	mailData.append("\n" + "\n") #add new line

	for messageLine in messageInputList:
		mailData.append(messageLine)
	lastOne = ""
	lastOneList = []
	lastOne = mailData[-1]
	lastOneList = lastOne.split("\n")
	mailData.remove(mailData[-1])
	mailData.append(lastOneList[0])

	data() #call data to validate 

main() #call to main function 




