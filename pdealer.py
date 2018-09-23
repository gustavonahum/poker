import socket
from phand import PokerHand
from pprotocol import PokerProtocol
import jsonpickle
from random import shuffle

class PokerDealer:
	# State of the game
	state = ""
	# Deck of cards
	deck = []
	# List of players of this round
	players = []
	# List of players that are waiting to play in the next round
	waitingPlayers = []
	# Send card acknowledges
	sendCardAcks = []
	# Port of the dealer
	dPort = 0
	# Sending socket of the dealer
	sSocket = None

	def __init__(self, dPort, sSocket):
		self.state = "before-game"
		self.initializeDeck()
		self.dPort = dPort
		self.sSocket = sSocket

	def resolve(self, jsonObj):
		# Play request
		if jsonObj.messageCode == "PLRQ":
			if state == "before-game":
				self.sendPlayResponse(jsonObj.sendingProcessNumber)
			else:
				self.sendWaitResponse(jsonObj.sendingProcessNumber)
		# Start now request
		elif jsonObj.messageCode == "SNRQ":
			# Game still hasn't started
			if state == "before-game":
				# If there are enough players, start now
				if len(players) >= 2:
					self.state = "on-game"
					self.sendCards()
				# Else, wait a little more
				else:
					self.sendStartNowResponse(jsonObj.sendingProcessNumber)
			# Game has already started: ignore
			else:
				pass
		# Send card acknowledge
		elif jsonObj.messageCode == "SNCA":
			sendCardAcks.append(jsonObj.sendingProcessNumber)
			# If dealer has received all acks
			if len(sendCardAcks) == len(players):
				self.checkHandsRequest()
			# Else, wait a little more
			else:
				pass




	def sendPlayResponse(self, player):
		playResp = PokerProtocol("PLRP", self.dPort)
		sSocket.connect((host,player))
		sSocket.send(jsonpickle.encode(playResp).encode())
		players.append(player)

	def sendWaitResponse(self, player):
		playWaitResp = PokerProtocol("PLWR", self.dPort)
		sSocket.connect((host,player))
		sSocket.send(jsonpickle.encode(playWaitResp).encode())
		waitingPlayers.append(player)

	def sendStartNowResponse(self, player):
		startNowRespo = PokerProtocol("STRP", self.dPort)
		sSocket.connect((host,player))
		sSocket.send(jsonpickle.encode(startNowRespo).encode())

	def sendCards(self):
		for c in range(5):
			for player in players:
				sendCardToPlayer(self.deck.pop(),player)

	def sendCardToPlayer(self, card, player):
		(value,nipe) = card
		sendCard = PokerProtocol("SNCD", self.dPort, value, nipe, "", 5)
		sSocket.connect((host,player))
		sSocket.send(jsonpickle.encode(sendCard).encode())

	def checkHandsRequest(self):
		for player in players:
			checkHandReq = PokerProtocol("CHRQ", self.dPort)
			sSocket.connect((host,player))
			sSocket.send(jsonpickle.encode(checkHandReq).encode())



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
		print(self.deck)


p = PokerDealer(1,2)