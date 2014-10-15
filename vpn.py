#!/usr/bin/python
from socket import *
from select import select
from Tkinter import *

class Application(Tk):

	def __init__(self,parent):
		Tk.__init__(self,parent)
		self.parent = parent

		self.mode = 0
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
		self.modeButton = Button(self,text=u"OK",command=self.onSelectMode)
		self.modeButton.grid(column=0,row=1,columnspan=2)

		self.grid_columnconfigure(0,weight=1)

		# create the label that shows which mode was selected
		self.modeLabelVar = StringVar()
		label = Label(self,textvariable=self.modeLabelVar,anchor="w",fg="blue",bg="white")
		label.grid(column=0,row=2,columnspan=2,sticky='EW')

		# create labels to prompt for server port # and hostname
		label = Label(self,text="Server Port #",anchor="w",fg="black",bg="white")
		label.grid(column=0,row=3,columnspan=2,sticky='EW')

		label = Label(self,text="Host Name",anchor="w",fg="black",bg="white")
		label.grid(column=0,row=4,columnspan=2,sticky='EW')


		# create entry fields to allow user input for server port # and hostname
		self.portNumberVar = StringVar()
		self.portNumberEntry = Entry(self,textvariable=self.portNumberVar,state="disabled")
		self.portNumberEntry.grid(column=1,row=3,sticky='EW')
		self.portNumberVar.set(u"12000")		

		self.hostnameVar = StringVar()
		self.hostnameEntry = Entry(self,textvariable=self.hostnameVar,state="disabled")
		self.hostnameEntry.grid(column=1,row=4,sticky='EW')
		self.hostnameVar.set(u"localhost")		

		# create a Connect button
		self.connectButton = Button(self,text=u"Connect",command=self.onConnect, state="disabled")
		self.connectButton.grid(column=0,row=5,columnspan=2)

		# create a label that shows connection status
		self.connectLabelVar = StringVar()
		label = Label(self,textvariable=self.connectLabelVar,anchor="w",fg="black",bg="white")
		label.grid(column=0,row=6,columnspan=2,sticky='EW')

		# create labels that prompt for sent and received messages
		label = Label(self,text="Sent msg: ",anchor="w",fg="black",bg="white")
		label.grid(column=0,row=7,columnspan=2,sticky='EW')

		label = Label(self,text="Received msg: ",anchor="w",fg="black",bg="white")
		label.grid(column=0,row=8,columnspan=2,sticky='EW')

		# create entry fields that display sent and received messages
		self.sentMsgVar = StringVar()
		self.sentMsgEntry = Entry(self,textvariable=self.sentMsgVar,state="disabled",width=30)
		self.sentMsgEntry.grid(column=1,row=7,sticky='EW')
		self.sentMsgVar.set(u"")	

		self.receivedMsgVar = StringVar()
		self.receivedMsgEntry = Entry(self,textvariable=self.receivedMsgVar,state="disabled",width=30)
		self.receivedMsgEntry.grid(column=1,row=8,sticky='EW')
		self.receivedMsgVar.set(u"")			

		# create send and receive buttons
		self.sendMsgButton = Button(self,text=u"Send",command=self.onSendMessage, state="disabled")
		self.sendMsgButton.grid(column=3,row=7,columnspan=2)

		self.receiveMsgButton = Button(self,text=u"Receive",command=self.onReceiveMessage, state="disabled")
		self.receiveMsgButton.grid(column=3,row=8,columnspan=2)

		# create label that indicate intermediary messages
		label = Label(self,text="Other msgs: ",anchor="w",fg="black",bg="white")
		label.grid(column=0,row=9,columnspan=1,sticky='EW')

		# create field for intermediary messages
		self.otherMsgVar = StringVar()
		self.otherMsgEntry = Entry(self,textvariable=self.otherMsgVar,state="normal",width=30)
		self.otherMsgEntry.grid(column=1,row=9,sticky='EW')
		self.otherMsgVar.set(u"")	

		# create continue button
		self.continueButton = Button(self,text=u"Continue",command=self.onContinue, state="normal")
		self.continueButton.grid(column=3,row=9,columnspan=2)

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

		# client mode behaviour
		elif self.mode == 2:
			self.modeLabelVar.set("You have selected Client Mode")

			# enable the corresponding fields and buttons
			self.portNumberEntry.configure(state="normal")
			self.hostnameEntry.configure(state="normal")
			self.connectButton.configure(state="normal")

		else:
			self.modeLabelVar.set("Undefined mode...")

		self.R1.configure(state="disabled")
		self.R2.configure(state="disabled")
		self.modeButton.configure(state="disabled")

	def onConnect(self):
		# server mode behaviour
		if self.mode == 1:

			# enable/disable the corresponding fields and buttons
			self.portNumberEntry.configure(state="disabled")
			self.connectButton.configure(state="disabled")
			self.sentMsgEntry.configure(state="normal")
			self.receivedMsgEntry.configure(state="normal")
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
			self.sentMsgEntry.configure(state="normal")
			self.receivedMsgEntry.configure(state="normal")
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
		if self.mode == 1:
			msgToBeSent = self.sentMsgVar.get()
			self.connection.send(msgToBeSent)

		elif self.mode == 2:
			msgToBeSent = self.sentMsgVar.get()
			self.clientSocket.send(msgToBeSent)

	def onReceiveMessage(self):

		# ***** INSERT FUNCTIONALITY FOR RECEIVING MESSAGE HERE *****
		if self.mode == 1:
			data = self.connection.recv(1024)
			if data:
				 # A readable client socket has data
				print 'received "%s"' % (data)
		elif self.mode == 2:
			data = self.clientSocket.recv(1024)
			if data:
				 # A readable client socket has data
				print 'received "%s"' % (data)

	def onContinue(self):

		# The purpose of this button is to step through messages one step at a time (as per instructions)
		# The corresponding field is supposed to show those intermediary messages for encoding etc.
		# Just a placeholder for now
		pass

if __name__ == "__main__":
	app = Application(None)
	app.title('VPN')
	app.mainloop()