class PokerHand:
	hand = []
	values = ["7","8","9","10","J","Q","K","A"]

	def __init__(self, hand):
		self.hand = hand


	"""Main functions"""
	def isRoyalFlush(self):
		# Evaluates if hand is Royal Flush
		if self.isStraightFlush() and self.highestValue() == "A":
			return True
		return False

	def isStraightFlush(self):
		# Evaluates if hand is Straight Flush
		if self.isStraight() and self.isFlush():
			return True
		return False

	def isFourOfAKind(self):
		# Evaluates if hand is Four of a Kind
		if self.repetitionsInHand(4):
			return True
		return False

	def isFullHouse(self):
		# Evaluates if hand is Full House
		if self.repetitionsInHand(3,2):
			return True
		return False

	def isFlush(self):
		# Evaluates if hand is Flush
		if self.sameNipe():
			return True
		return False

	def isStraight(self):
		# Evaluates if hand is Straight
		if self.inSequence():
			return True
		return False

	def isThreeOfAKind(self):
		# Evaluates if hand is Three of a Kind
		if self.repetitionsInHand(3):
			return True
		return False

	def isTwoPair(self):
		# Evaluates if hand is Two Pair
		if self.repetitionsInHand(2,2):
			return True
		return False

	def isOnePair(self):
		# Evaluates if hand is One Pair
		if self.repetitionsInHand(2):
			return True
		return False


	"""Auxiliary functions"""
	def repetitionsInHand(self, num1, num2=0):
		# Evaluates if there are num1 (and, eventually, num2) repetitions of a given value
		if num2 == 0:
			for (value, nipe) in self.hand:
				if self.valueRepeats(value, num1):
					return True
			return False
		else:
			for (value1, nipe1) in self.hand:
				for (value2, nipe2) in self.hand:
					if self.valueRepeats(value1, num1) and self.valueRepeats(value2, num2):
						return True
			return False

	def valueRepeats(self, value, num):
		# Evaluates if there are "num" instances of "value" in the hand
		total = 0
		for (v, n) in self.hand:
			if v == value:
				total+=1
		return total == num

	def inSequence(self):
		# Evaluates if the values form a complete sequence
		currValue = self.lowestValueInHand()
		for (v, n) in self.hand:
			if self.valueInHand(currValue):
				currValue = self.nextValue(currValue)
			else:
				return False
		return True

	def lowestValueInHand(self):
		# Returns the lowest value in the hand
		for v in self.values:
			if self.valueInHand(v):
				return v
		return None

	def valueInHand(self, value):
		# Evaluates if "value" exists in the hand
		for (v, n) in self.hand:
			if value == v:
				return True
		return False

	def nextValue(self, value):
		# Returns the next value in the poker sequence
		# E.g.: nextValue("J") = "Q", nextValue("7") = "8", etc.
		if value == "A":
			return None
		currIndex = self.values.index(value)
		return self.values[currIndex + 1]

	def sameNipe(self):
		# Evaluates if all cards in hand are of a same nipe
		(value, nipe) = self.hand[0]
		for (v, n) in self.hand:
			if n != nipe:
				return False
		return True

	def highestValue(self):
		# Returns the highest value in the hand
		(value, nipe) = self.hand[0]
		highest = value
		for (v, n) in self.hand:
			if self.values.index(v) > self.values.index(highest):
				highest = v
		return highest
