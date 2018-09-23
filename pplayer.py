import socket
from phand import PokerHand
from pprotocol import PokerProtocol
import jsonpickle
import curses

class PokerPlayer:
	# State of player
	isPlaying = None
	# Player hand
	hand = []
	# Port of the dealer
	dPort = 0
	# Port of the player
	pPort = 0
	# Sending socket of the player
	sSocket = None

	def __init__(self, dPort, pPort, sSocket):
		self.dPort = dPort
		self.pPort = pPort
		self.sSocket = sSocket

	def resolve(self, jsonObj):
		# Play response
		if jsonObj.messageCode == "PLRP":
			self.isPlaying = True
		# Play wait response
		if jsonObj.messageCode == "PLWR":
			self.isPlaying = False
		# 
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