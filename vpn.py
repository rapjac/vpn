#!/usr/bin/python
from socket import *
from select import select
from Tkinter import *
from hashlib import *
from Crypto import Random
from Crypto.Cipher import AES

class Application(Tk):

	BLOCK_SIZE = 16
	def __init__(self,parent):
		Tk.__init__(self,parent)
		self.parent = parent

		self.mode = 0
		self.key = ""
		self.generator = 2
		self.prime = 23

		self.serverPort = 0
		self.serverSocket = 0
		self.connection = 0
		self.clientSocket = 0
		self.hostname = 0

		self.initialize()

	def initialize(self):

		self.grid()

		# create radio buttons for selecting mode
		self.radioVariable = IntVar()
		
		self.R1 = Radiobutton(self, text="Server Mode", variable=self.radioVariable, value=1)
		self.R1.grid(column=0,row=0)

		self.R2 = Radiobutton(self, text="Client Mode", variable=self.radioVariable, value=2)
		self.R2.grid(column=1,row=0)


		# create "OK" button to select mode
		self.modeButton = Button(self,text=u"         OK        ",command=self.onSelectMode)
		self.modeButton.grid(column=2,row=0,columnspan=1)

		self.grid_columnconfigure(0,weight=1)

		# create the label that shows which mode was selected
		self.modeLabelVar = StringVar()
		label = Label(self,textvariable=self.modeLabelVar,anchor="w",fg="blue",bg="white")
		label.grid(column=0,row=1,columnspan=7,sticky='EW')

		# create labels to prompt for server port # and hostname
		label = Label(self,text="Server Port #:",anchor="w",fg="black",bg="white")
		label.grid(column=0,row=2,columnspan=1,sticky='EW')

		label = Label(self,text="Host Name:",anchor="w",fg="black",bg="white")
		label.grid(column=2,row=2,columnspan=1,sticky='EW')

		label = Label(self,text="Shared Secret Value:",anchor="w",fg="black",bg="white")
		label.grid(column=4,row=2,columnspan=1,sticky='EW')

		# create entry fields to allow user input for server port # and hostname
		self.portNumberVar = StringVar()
		self.portNumberEntry = Entry(self,textvariable=self.portNumberVar,state="disabled")
		self.portNumberEntry.grid(column=1,row=2,sticky='EW')
		self.portNumberVar.set(u"12000")		

		self.hostnameVar = StringVar()
		self.hostnameEntry = Entry(self,textvariable=self.hostnameVar,state="disabled")
		self.hostnameEntry.grid(column=3,row=2,sticky='NE')
		self.hostnameVar.set(u"localhost")		

		self.ssvVar = StringVar()
		self.ssvEntry = Entry(self,textvariable=self.ssvVar,state="disabled")
		self.ssvEntry.grid(column=5,row=2,sticky='EW')
		self.ssvVar.set(u"Input SSV here")		

		# create a Connect button
		self.connectButton = Button(self,text=u"Connect",command=self.onConnect, state="disabled")
		self.connectButton.grid(column=6,row=2,columnspan=1)

		# create a label that shows connection status
		self.connectLabelVar = StringVar()
		label = Label(self,textvariable=self.connectLabelVar,anchor="w",fg="blue",bg="white")
		label.grid(column=0,row=3,columnspan=7,sticky='EW')

		# create labels that prompt for sent and received messages
		label = Label(self,text="Send msg: ",anchor="w",fg="black",bg="white")
		label.grid(column=0,row=4,columnspan=2,sticky='NW')

		label = Label(self,text="Received msg: ",anchor="w",fg="black",bg="white")
		label.grid(column=3,row=4,columnspan=2,sticky='NE')		

		# create text areas that display sent and received messages
		self.sentText = Text(self,height=5,width=32)
		self.sentText.grid(column=1,row=4, columnspan=2,sticky='EW')
		self.sentText.insert(INSERT, "Input the text to be sent here.")

		self.receivedText = Text(self,height=5,width=32)
		self.receivedText.grid(column=5,row=4, columnspan=2,sticky='EW')
		self.receivedText.insert(INSERT, "Received text will appear here.")

		# create send and receive buttons
		self.sendMsgButton = Button(self,text=u"Send",command=self.onSendMessage, state="disabled")
		self.sendMsgButton.grid(column=1,row=5,columnspan=2,sticky='EW')

		self.receiveMsgButton = Button(self,text=u"Receive",command=self.onReceiveMessage, state="disabled")
		self.receiveMsgButton.grid(column=5,row=5,columnspan=2,sticky='EW')
		
		# extra padding
		label = Label(self,text=" ",anchor="w",fg="black",bg="white")
		label.grid(column=0,row=6,columnspan=7,sticky='NE')		

		# create label to indicate raw text
		label = Label(self,text="Raw message: ",anchor="w",fg="black",bg="white")
		label.grid(column=0,row=7,columnspan=2,sticky='NW')

		# create text area to display the raw message
		self.rawMessageText = Text(self,height=5)
		self.rawMessageText.grid(column=1,row=7, columnspan=6,sticky='EW')
		self.rawMessageText.insert(INSERT, "Raw messages received will appear here.")

	def onSelectMode(self):

		# store the selected mode from the radio buttons
		self.mode = self.radioVariable.get()

		# server mode behaviour
		if self.mode == 1:
			self.modeLabelVar.set("You have selected Server Mode")

			# enable the corresponding fields and buttons
			self.portNumberEntry.configure(state="normal")
			self.hostnameEntry.configure(state="normal")
			self.connectButton.configure(state="normal")
			self.ssvEntry.configure(state="normal")
			self.connectLabelVar.set("Note: After pressing Connect, this window will pause and wait for the client's connection before resuming.")

		# client mode behaviour
		elif self.mode == 2:
			self.modeLabelVar.set("You have selected Client Mode")

			# enable the corresponding fields and buttons
			self.portNumberEntry.configure(state="normal")
			self.hostnameEntry.configure(state="normal")
			self.connectButton.configure(state="normal")
			self.ssvEntry.configure(state="normal")

		else:
			self.modeLabelVar.set("Undefined mode...")

		self.R1.configure(state="disabled")
		self.R2.configure(state="disabled")
		self.modeButton.configure(state="disabled")

	def onConnect(self):
		# server mode behaviour
		self.Key = self.ssvEntry.get()

		if self.mode == 1:

			# enable/disable the corresponding fields and buttons
			self.portNumberEntry.configure(state="disabled")
			self.connectButton.configure(state="disabled")
			self.sendMsgButton.configure(state="normal")
			self.receiveMsgButton.configure(state="normal")

			# ***** INSERT CODE TO SETUP SERVER CONNECTION HERE *****
			# I assume this also includes the mutual authentication / key establishment

			serverPort = int(self.portNumberEntry.get())
			self.serverSocket = socket(AF_INET,SOCK_STREAM)
			self.serverSocket.setblocking(0)
			serverHost = self.hostnameEntry.get()

			self.serverSocket.bind((serverHost,serverPort)) 
			self.serverSocket.listen(1) 

			#sockets we expect to read from
			inputs = [self.serverSocket]
			#sockets we expect to write to
			outputs = []

			readable, writable, exceptional = select(inputs, outputs, inputs)

			for s in readable:
				if s is self.serverSocket:
					# A "readable" server socket is ready to accept a connection
					self.connection, client_address = s.accept()

					self.connection.setblocking(0)
					inputs.append(self.connection)
					outputs.append(self.connection)

					# update connection status in UI
					connectMsg = "The server is ready to communicate with clients using port " + self.portNumberVar.get()
					self.connectLabelVar.set(connectMsg)


		# client mode behaviour
		elif self.mode == 2:

			# enable/disable the corresponding fields and buttons
			self.portNumberEntry.configure(state="disabled")
			self.hostnameEntry.configure(state="disabled")
			self.connectButton.configure(state="disabled")
			self.sendMsgButton.configure(state="normal")
			self.receiveMsgButton.configure(state="normal")

			# ***** INSERT CODE TO SETUP CLIENT CONNECTION HERE *****
			# I assume this also includes the mutual authentication / key establishment

			serverName = self.hostnameEntry.get()
			serverPort = int(self.portNumberEntry.get())

			self.clientSocket = socket(AF_INET, SOCK_STREAM) 
			self.clientSocket.connect((serverName,serverPort)) 

			# update connection status in UI
			connectMsg = "The server is ready to communicate with host " + self.hostnameVar.get() + " using port " + self.portNumberVar.get()
			self.connectLabelVar.set(connectMsg)

		else:
			self.connectLabelVar.set("Undefined mode...")
		
	def onSendMessage(self):
		message = self.sentText.get(1.0, END)

		print 'sent "%s"' % (message)
		sendText(message)

	def onReceiveMessage(self):
		message = receivedText()

		if message:
			 # A readable client socket has data
			print 'received "%s"' % (message)

			self.rawMessageText.delete(1.0, END)
			self.receivedText.delete(1.0, END)

			self.rawMessageText.insert(1.0, self.decrypt(str(message)))
			self.receivedText.insert(1.0, self.decrypt(str(message)))

	def pad(self, text):
		x = BLOCK_SIZE - len(text)%BLOCK_SIZE
		return text.zfill(x)

	def encrypt(self, plaintext):
		plaintext = pad(plaintext)
		iv = Random.new().read(AES.BLOCK_SIZE)
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return base64.b64encode(iv + cipher.encrypt(plaintext))

	def decrypt(self, ciphertext):
		return ciphertext

	def sendText(self, text):
		if self.mode == 1:
			self.connection.send(text)

		elif self.mode == 2:
			self.clientSocket.send(text)

	def receiveText(self):
		if self.mode == 1:
			text = self.connection.recv(1024)
		elif self.mode == 2:
			text = self.clientSocket.recv(1024)
		else:
			text = ''

		return text

	def authenticate(self):
		hashSeed = os.urandom(8)
		hash_object = hashlib.sha1(b(hashSeed))
		# returns a string of length 40
		nonce = hash_object.hexdigest()

		sendText(nonce)
		response = receiveText()

		x = len(response)
		# Response excluding nonce
		encMessage = response[41:x]

		authMessage = decrypt(encMessage)
		if authMessage[:6] == "server"
			authResponse = "client" + response[:40] + pow(self.generator, , self.prime)


if __name__ == "__main__":
	app = Application(None)
	app.title('VPN')
	app.mainloop()