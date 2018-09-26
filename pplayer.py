import socket
from phand import PokerHand
from pprotocol import PokerProtocol
import jsonpickle

class PokerPlayer:
	# State of player
	isPlaying = None
	# Player hand
	hand = []
	# Port of the dealer
	dPort = 0
	# Port of the player
	pPort = 0
	# Host
	host = 0
	# Sending socket of the player
	sSocket = None
	# Number of winners received
	wCount = 0

	def __init__(self, dPort, pPort, host, sSocket):
		self.dPort = dPort
		self.pPort = pPort
		self.host = host
		self.sSocket = sSocket
		playReq = PokerProtocol("PLRQ", self.pPort)
		self.sSocket.send(jsonpickle.encode(playReq).encode())
		self.sSocket.close()
		self.sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def resolve(self, jsonObj):
		# Play response
		if jsonObj.messageCode == "PLRP":
			self.isPlaying = True
			print("I am playing in this round")
		# Send card
		if jsonObj.messageCode == "SNCD":
			self.receiveCard(jsonObj)
		# Check hand
		if jsonObj.messageCode == "CHRQ":
			self.checkHandResponse()
		# Notify players of the winner:
		if jsonObj.messageCode == "NTGR":
			self.printWinner(jsonObj)
			self.wCount += 1
			if self.wCount == jsonObj.quantityOfMessages:
				self.sendEndOfGame()
			

	def receiveCard(self, jsonObj):
		self.hand.append((jsonObj.cardValue, jsonObj.cardNipe))
		print((jsonObj.cardValue, jsonObj.cardNipe))
		if len(self.hand) == jsonObj.quantityOfMessages:
			self.sendCardAck()

	def sendCardAck(self):
		cardAck = PokerProtocol("SNCA",self.pPort)
		self.sSocket.connect((self.host,self.dPort))
		self.sSocket.send(jsonpickle.encode(cardAck).encode())
		self.sSocket.close()
		self.sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def checkHandResponse(self):
		for card in self.hand:
			(value, nipe) = card
			checkHandResp = PokerProtocol("CHRP",self.pPort,value,nipe,"",5)
			self.sSocket.connect((self.host,self.dPort))
			self.sSocket.send(jsonpickle.encode(checkHandResp).encode())
			self.sSocket.close()
			self.sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def printWinner(self, jsonObj):
		print("The winner was: " + str(jsonObj.winningProcessNumber))

	def sendEndOfGame(self):
		endOfGame = PokerProtocol("EOGM",self.pPort)
		self.sSocket.connect((self.host,self.dPort))
		self.sSocket.send(jsonpickle.encode(endOfGame).encode())
		self.sSocket.close()
		self.sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)