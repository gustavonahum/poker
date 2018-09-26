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
	dealerPort = 0
	# Port of the player
	playerPort = 0
	# Host
	host = 0
	# Number of winners received
	wCount = 0

	def __init__(self, dealerPort, playerPort, host):
		self.dealerPort = dealerPort
		self.playerPort = playerPort
		self.host = host
		playReq = PokerProtocol("PLRQ", self.playerPort)
		self.sendMessage(playReq)

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
		cardAck = PokerProtocol("SNCA",self.playerPort)
		self.sendMessage(cardAck)

	def checkHandResponse(self):
		for card in self.hand:
			(value, nipe) = card
			checkHandResp = PokerProtocol("CHRP",self.playerPort,value,nipe,"",5)
			self.sendMessage(checkHandResp)

	def printWinner(self, jsonObj):
		print("The winner was: " + str(jsonObj.winningProcessNumber))

	def sendEndOfGame(self):
		endOfGame = PokerProtocol("EOGM",self.playerPort)
		self.sendMessage(endOfGame)

	def sendMessage(self,msgObj):
		sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sSocket.connect((self.host,self.dealerPort))
		sSocket.send(jsonpickle.encode(msgObj).encode())
		sSocket.close()