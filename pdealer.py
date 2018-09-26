import socket
from phand import PokerHand
from pprotocol import PokerProtocol
import jsonpickle
from random import shuffle
import time
from collections import defaultdict
from chands import CompareHands


class PokerDealer:
	# State of the game
	state = ""
	# Deck of cards
	deck = []
	# Number of players
	nPlayers = 0
	# List of players of this round
	players = []
	# Send card acknowledges
	sendCardAcks = []
	# Hands of players
	hands = None
	# Port of the dealer
	dPort = 0
	# Host
	host = 0

	def __init__(self, nPlayers, host, dPort):
		self.state = "before-game"
		self.initializeDeck()
		self.nPlayers = nPlayers
		self.host = host
		self.dPort = dPort
		self.hands = defaultdict(list)

	def resolve(self, jsonObj):
		# Play request
		if jsonObj.messageCode == "PLRQ":
			if self.state == "before-game":
				self.sendPlayResponse(jsonObj.sendingProcessNumber)
			else:
				self.sendRefuseResponse(jsonObj.sendingProcessNumber)
		# Send card acknowledge
		elif jsonObj.messageCode == "SNCA":
			self.sendCardAcks.append(jsonObj.sendingProcessNumber)
			# If dealer has received all acks
			if len(self.sendCardAcks) == len(self.players):
				self.checkHandsRequest()
			# Else, wait a little more
			else:
			 	time.sleep(1)
		# Check hand response
		elif jsonObj.messageCode == "CHRP":
			self.storePlayerHand(jsonObj)



	def sendPlayResponse(self, player):
		playResp = PokerProtocol("PLRP", self.dPort)
		self.sendMessage(player,playResp)
		print("New player in this round: " + str(player))
		self.players.append(player)
		self.checkIfGameCanStart()

	def sendRefuseResponse(self, player):
		playRefuseResp = PokerProtocol("PLRR", self.dPort)
		self.sendMessage(player,playRefuseResp)

	def checkIfGameCanStart(self):
		if len(self.players) == self.nPlayers:
			self.state = "on-game"
			self.sendCards()

	def sendCards(self):
		for c in range(5):
			for player in self.players:
				self.sendCardToPlayer(self.deck.pop(),player)
				time.sleep(1)

	def sendCardToPlayer(self, card, player):
		(value,nipe) = card
		sendCard = PokerProtocol("SNCD", self.dPort, value, nipe, "", 5)
		self.sendMessage(player,sendCard)

	def checkHandsRequest(self):
		for player in self.players:
			checkHandReq = PokerProtocol("CHRQ", self.dPort)
			self.sendMessage(player,checkHandReq)

	def storePlayerHand(self,jsonObj):
		self.hands[jsonObj.sendingProcessNumber].append((jsonObj.cardValue,jsonObj.cardNipe))
		self.checkHandsReceived()

	def checkHandsReceived(self):
		if len(self.hands) == len(self.players):
			for hand in self.hands:
				if len(self.hands[hand]) < 5:
					return
			self.evaluateWinner()

	def evaluateWinner(self):
		cHandObj = CompareHands(self.hands)
		winningHands = cHandObj.resolveBestHand()

		for hand in winningHands:
			for player in self.players:
				winner = self.findWinner(hand)
				notifyGameResult = PokerProtocol("NTGR", self.dPort, "", "", winner, len(winningHands))
				self.sendMessage(player,notifyGameResult)
		self.state = "before-game"



	"""Auxiliary methods"""
	def initializeDeck(self):
		# From "2" to "A"
		values = ["7","8","9","10","J","Q","K","A"]
		# "Paus", "Copas", "Espadas", "Ouros"
		nipes = ["P","C","E","O"]
		for v in values:
			for n in nipes:
				self.deck.append((v,n))
		self.shuffleDeck()

	def shuffleDeck(self):
		shuffle(self.deck)

	def findWinner(self, hand):
		for player in self.players:
			if self.hands[player] == hand:
				return player

	def sendMessage(self,player,msgObj):
		sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sSocket.connect((self.host,player))
		sSocket.send(jsonpickle.encode(msgObj).encode())
		sSocket.close()
