import socket
from phand import PokerHand
from pprotocol import PokerProtocol
import jsonpickle
from random import shuffle
import time
from collections import defaultdict

def nop():
	pass

class PokerDealer:
	# State of the game
	state = ""
	# Deck of cards
	deck = []
	# Number of players
	nPlayers = 0
	# Number of cards for each player
	nCards = 5
	# List of players of this round
	players = []
	# List of players that are waiting to play in the next round
	waitingPlayers = []
	# Send card acknowledges
	sendCardAcks = []
	# Hands of players
	hands = None
	# Port of the dealer
	dPort = 0
	# Host
	host = 0
	# Sending socket of the dealer
	sSocket = None

	def __init__(self, nPlayers, host, dPort, sSocket):
		self.state = "before-game"
		self.initializeDeck()
		self.nPlayers = nPlayers
		self.host = host
		self.dPort = dPort
		self.sSocket = sSocket
		self.hands = defaultdict(list)

	def resolve(self, jsonObj):
		# Play request
		if jsonObj.messageCode == "PLRQ":
			if self.state == "before-game":
				self.sendPlayResponse(jsonObj.sendingProcessNumber)
			else:
				self.sendWaitResponse(jsonObj.sendingProcessNumber)
		# Send card acknowledge
		elif jsonObj.messageCode == "SNCA":
			sendCardAcks.append(jsonObj.sendingProcessNumber)
			# If dealer has received all acks
			if len(sendCardAcks) == len(self.players):
				self.checkHandsRequest()
			# Else, wait a little more
			else:
			 	time.sleep(1)
		# Check hand response
		elif jsonObj.messageCode == "CHRP":
			self.storePlayerHand(jsonObj)




	def sendPlayResponse(self, player):
		playResp = PokerProtocol("PLRP", self.dPort)
		print(player)
		self.sSocket.connect((self.host,player))
		self.sSocket.send(jsonpickle.encode(playResp).encode())
		self.sSocket.close()
		self.sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.players.append(player)
		self.checkIfGameCanStart()

	def sendWaitResponse(self, player):
		playWaitResp = PokerProtocol("PLWR", self.dPort)
		self.sSocket.connect((self.host,player))
		self.sSocket.send(jsonpickle.encode(playWaitResp).encode())
		self.sSocket.close()
		self.sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		waitingPlayers.append(player)

	def checkIfGameCanStart(self):
		if len(self.players) == self.nPlayers:
			print(True)
			self.state = "on-game"
			self.sendCards()

	def sendCards(self):
		for c in range(self.nCards):
			for player in self.players:
				self.sendCardToPlayer(self.deck.pop(),player)
				time.sleep(1)

	def sendCardToPlayer(self, card, player):
		(value,nipe) = card
		sendCard = PokerProtocol("SNCD", self.dPort, value, nipe, "", self.nCards)
		self.sSocket.connect((self.host,player))
		self.sSocket.send(jsonpickle.encode(sendCard).encode())
		self.sSocket.close()
		self.sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def checkHandsRequest(self):
		for player in self.players:
			checkHandReq = PokerProtocol("CHRQ", self.dPort)
			self.sSocket.connect((self.host,player))
			self.sSocket.send(jsonpickle.encode(checkHandReq).encode())
			self.sSocket.close()
			self.sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def storePlayerHand(self,jsonObj):
		self.hands[jsonObj.sendingProcessNumber].append((jsonObj.cardValue,jsonObj.cardNipe))
		self.checkHandsReceived()

	def checkHandsReceived(self):
		if len(self.hands == len(self.players)):
			for hand in self.hands:
				if len(hand) < self.nCards:
					return
			self.checkWinner()

	def checkWinner(self):
		pass



	"""Auxiliary methods"""
	def initializeDeck(self):
		# From "2" to "A"
		values = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
		# "Paus", "Copas", "Espadas", "Ouros"
		nipes = ["P","C","E","O"]
		for v in values:
			for n in nipes:
				self.deck.append((v,n))
		self.shuffleDeck()

	def shuffleDeck(self):
		shuffle(self.deck)


