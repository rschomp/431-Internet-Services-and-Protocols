#read a forward-file and generate and write to standard output the SMTP commands 
#necessary to send the contents of the mail messages in the forward-file to a 
#destination SMTP server

#variables to track the addresses and data
toAddress = []
fromAddress = ""
mailData = []
import sys

#requests user input and echos the message specific to 250
def command250():
	userInput = raw_input()
	if (userInput == ""):
		print "\nQUIT"
		exit()
	inputList = userInput.split()
	if (inputList[0] == "250"):
		sys.stderr.write(userInput)
	else: #if invalid command250, print quit and exit
		sys.stderr.write(userInput)
		print "\nQUIT"
		exit()

#handles the mail from address 
def mailFrom():
	print "MAIL FROM: " + fromAddress
	command250()

#handles the one or more to addresses
def rcptTo():
	for rcpt in toAddress:
		print "\nRCPT TO: " + rcpt
		command250()		

#handles the printing of the data and following format
def data():
	print "\nDATA"

	#print 354, specific to data section
	userInput = raw_input()
	if (userInput == ""):
		print "\nQUIT"
		exit()
	inputList = userInput.split()
	if (inputList[0] == "354"):
		sys.stderr.write(userInput)
		print
	else:
		sys.stderr.write(userInput)
		print "\nQUIT"
		exit()
	for dataText in mailData: 
		print dataText, #prints the data lines in order
	print "."
	
	#requests and echos 250 once data section is done
	#if invalid, exit
	userInput = raw_input()
	if (userInput == ""):
		print "\nQUIT"
		exit()
	inputList = userInput.split()
	if (inputList[0] == "250"):
		sys.stderr.write(userInput)
		print
	else:
		sys.stderr.write(userInput)
		print "\nQUIT"
		exit()

#main method to handle the reading of the file and calling the specific methods
def main():
	file = open(sys.argv[1], "r") #open the file by name 
	fileLines = file.readlines() #store each line in the list fileLines
	lineIndex = 0 #keeps track of which line you are at
	global fromAddress
	global toAddress
	global mailData

	while True: #reading while there is data in file
		if (not fileLines[lineIndex][:6] == "From: "): #make sure file begins with From:
			print "QUIT"
			exit()
		else:
			fromAddress = fileLines[lineIndex][6:-1] #if first word is From:, save the from address
			mailFrom()
			lineIndex = lineIndex + 1 #index line number up by 1
		
		while (fileLines[lineIndex][:4] == "To: "): #if current line begins with To: save that data
			toAddress.append(fileLines[lineIndex][4:-1])
			lineIndex = lineIndex + 1
		rcptTo()

		while lineIndex != len(fileLines): #check if data is blank and next line is another mail message
			if (len(fileLines[lineIndex]) >= 5 and fileLines[lineIndex][:5] == "From:"):
				break
			else:
				mailData.append(fileLines[lineIndex])
				lineIndex = lineIndex + 1 
		data()
		
		if (lineIndex == len(fileLines)): #if at end of file quit
			print "QUIT"
			exit()

		if (fileLines[lineIndex][:6] == "From: "): #check for new From:, start over
			#reset for next input	
			toAddress = []
			fromAddress = ""
			mailData = []
main() #call to main function 




